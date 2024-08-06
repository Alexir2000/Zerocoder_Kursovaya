# catalog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import TovarSearchForm
from orders.models import CartItem
from main.models import Tovar, Zakaz, Adresa, Otgruzka, Zhurnal_status_Zakaza
import json


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