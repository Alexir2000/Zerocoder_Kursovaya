# catalog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
import json
from .forms import TovarSearchForm
from orders.models import CartItem
from main.models import Tovar, Zakaz, Adresa, Otgruzka, Zhurnal_status_Zakaza, BaseOtziv
from .forms import AddReviewForm

def catalog_view(request):
    form = TovarSearchForm(request.GET)
    tovars = Tovar.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        type = form.cleaned_data.get('type')

        if query:
            tovars = tovars.filter(Nazvanie__icontains=query)
        if category:
            tovars = tovars.filter(ID_KategorTovara=category)
        if type:
            tovars = tovars.filter(ID_TipTovara=type)

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_registered=True)
    else:
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id, is_registered=False)

    total_price = sum(item.cena * item.quantity for item in cart_items)  # Вычисление общей суммы
    return render(request, 'catalog/catalog.html',
                  {'tovars': tovars, 'form': form, 'cart_items': cart_items, 'total_price': total_price})


def karta_tovara(request, pk):
    tovar = get_object_or_404(Tovar, pk=pk)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_registered=True)
    else:
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id, is_registered=False)

    total_price = sum(item.cena * item.quantity for item in cart_items)  # Вычисление общей суммы
    otzyvy = BaseOtziv.objects.filter(ID_Tovar=tovar)

    return render(request, 'catalog/karta_tovara.html',
                  {'tovar': tovar, 'cart_items': cart_items, 'total_price': total_price, 'otzyvy': otzyvy})


@login_required
def otzyv_na_tovar(request, pk):
    tovar = get_object_or_404(Tovar, pk=pk)
    User = get_user_model()
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_registered=True)
    else:
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id, is_registered=False)

    total_price = sum(item.cena * item.quantity for item in cart_items)
    otzyvy = BaseOtziv.objects.filter(ID_Tovar=tovar).order_by('-date_created')  # Сортировка по дате создания

    # Проверка, оставлял ли пользователь отзыв на этот товар
    user_review_exists = BaseOtziv.objects.filter(ID_Tovar=tovar, ID_User=request.user).exists()

    if request.method == 'POST':
        if not user_review_exists:
            form = AddReviewForm(request.POST)
            if form.is_valid():
                current_user = request.user
                new_otzyv = BaseOtziv(
                    ID_User=current_user,
                    ID_Tovar=tovar,
                    ReitingTovara=form.cleaned_data['reiting'],
                    Otziv=form.cleaned_data['otzyv'],
                    date_created=timezone.now()  # Сохранение текущей даты и времени
                )
                new_otzyv.save()

                # Пересчет общего количества отзывов для товара
                total_reviews = BaseOtziv.objects.filter(ID_Tovar=tovar).count()
                tovar.kolich_otzyv = total_reviews

                # Пересчет среднего рейтинга для товара
                total_rating = BaseOtziv.objects.filter(ID_Tovar=tovar).aggregate(total=models.Sum('ReitingTovara'))['total']
                if total_reviews > 0:
                    average_rating = total_rating / total_reviews
                    tovar.Reiting = average_rating
                else:
                    tovar.Reiting = 0

                tovar.save()
                return redirect('otzyv_na_tovar', pk=tovar.pk)
    else:
        form = AddReviewForm()

    return render(request, 'catalog/otzyv_na_tovar.html',
                  {'tovar': tovar, 'cart_items': cart_items, 'total_price': total_price, 'otzyvy': otzyvy,
                   'form': form, 'user_review_exists': user_review_exists})






# +++++++++++++++++==================
# функции API

def catalog_put_korzina(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_registered=True)
    else:
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id, is_registered=False)
    cart_data = [
        {
            'tovar': item.tovar.Nazvanie,
            'quantity': item.quantity
        }
        for item in cart_items
    ]
    return JsonResponse(cart_data, safe=False)


def catalog_put_zakaz(request):
    zakaz = Zakaz.objects.filter(Peredano_v_bot=False).order_by('DataZakaza').first()

    if not zakaz:
        return JsonResponse({'error': 'Нет заказов для отправки'}, status=404)

    try:
        adresa = Adresa.objects.get(ID=zakaz.ID_adres_id)
    except Adresa.DoesNotExist:
        adresa = None

    otgruzki = Otgruzka.objects.filter(ID_Zakaz=zakaz)
    total_price = sum(item.cena * item.quantity for item in otgruzki)

    zakaz_data = {
        'Vid_Put': 'Zakaz',
        'ID': zakaz.ID,
        'Data': zakaz.DataZakaza.strftime("%d.%m.%Y %H:%M"),
        'Adres': f"{adresa.Gorod}, {adresa.adres}" if adresa else "не указан",
        'Kontakt': adresa.kontakt if adresa else "не указан",
        'Telefon': adresa.telefon if adresa else "не указан",
        'Primechanie': zakaz.Primechanie,
        'Tovary': [
            {
                'Nazvanie': item.tovar_id.Nazvanie,
                'Cena': item.cena,
                'Kolichestvo': item.quantity
            }
            for item in otgruzki
        ],
        'Obshaya_Stoimost': total_price
    }

    return JsonResponse(zakaz_data, safe=False)


@csrf_exempt
def ok_put_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            zakaz_id = data.get('ID')

            zakaz = Zakaz.objects.get(ID=zakaz_id)
            zakaz.Peredano_v_bot = True
            zakaz.save()

            return JsonResponse({'Status': 'Put_OK'})
        except Zakaz.DoesNotExist:
            return JsonResponse({'Status': 'Put_failed'}, status=404)
        except Exception as e:
            return JsonResponse({'Status': 'Put_failed', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'Status': 'Put_failed'}, status=405)

def put_zhurnal_status(request):
    zhurnal_status = Zhurnal_status_Zakaza.objects.filter(peredano=False).order_by('Date').first()

    if not zhurnal_status:
        return JsonResponse({'error': 'Нет записей для передачи'}, status=404)

    return JsonResponse(json.loads(zhurnal_status.json_str), safe=False)


@csrf_exempt
def ok_put_zhurnal_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            zhurnal_id = data.get('ID')

            zhurnal_status = Zhurnal_status_Zakaza.objects.filter(peredano=False).order_by('Date').first()
            if not zhurnal_status or zhurnal_status.ID != zhurnal_id:
                return JsonResponse({'Status': 'Put_failed', 'error': 'Запись не найдена или ID не совпадает'},
                                    status=404)

            zhurnal_status.peredano = True
            zhurnal_status.save()

            return JsonResponse({'Status': 'Put_OK'})
        except Zhurnal_status_Zakaza.DoesNotExist:
            return JsonResponse({'Status': 'Put_failed'}, status=404)
        except Exception as e:
            return JsonResponse({'Status': 'Put_failed', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'Status': 'Put_failed'}, status=405)