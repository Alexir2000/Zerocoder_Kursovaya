# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from main.models import Tovar
from .forms import OrderForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime
from main.models import StatusZakaza, Adresa, Zakaz, Otgruzka


def add_to_cart(request, tovar_id):
    if request.method == "POST":
        tovar = get_object_or_404(Tovar, ID=tovar_id)
        quantity = int(request.POST.get('quantity', 1))
        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(tovar=tovar, user=request.user, is_registered=True)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            cart_item, created = CartItem.objects.get_or_create(tovar=tovar, session_id=session_id, is_registered=False)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            cart_item.cena = tovar.Cena  # Сохранить цену товара при добавлении
        cart_item.save()
    return redirect('catalog')

def cart_detail(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_registered=True)
    else:
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id, is_registered=False)
    total_price = sum(item.cena * item.quantity for item in cart_items)  # Вычисление общей суммы
    return render(request, 'orders/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user, is_registered=True)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            adresa = Adresa.objects.create(
                ID_User=request.user.id,
                Gorod=form.cleaned_data['gorod'],
                adres=form.cleaned_data['adres'],
                kontakt=form.cleaned_data['kontakt'],
                telefon=form.cleaned_data['telefon']
            )
            zakaz = Zakaz.objects.create(
                ID_TipZakaza="Тип заказа",  # Укажите нужное значение
                ID_User=request.user,
                ID_adres=adresa,
                Kolichestvo_klon=sum(item.quantity for item in cart_items),
                Primechanie=form.cleaned_data['primechanie'],
                DataZakaza=timezone.now(),
                DataDostavki=timezone.now(),  # Установка даты доставки на текущий момент
                ID_Status_zakaza=StatusZakaza.objects.get(ID=1),  # Укажите нужный статус
                Zakaz_oplachen=False,
                Zakaz_dostavlen=False,
                Zakaz_Poluchen=False,
                Zakaz_zakryt=False
            )
            for item in cart_items:
                Otgruzka.objects.create(
                    ID_Zakaz=zakaz,
                    tovar_id=item.tovar,
                    quantity=item.quantity,
                    cena=item.cena
                )
            cart_items.delete()
            return redirect('order_success')
    else:
        form = OrderForm()
    current_time = datetime.datetime.now()
    total_price = sum(item.cena * item.quantity for item in cart_items)
    context = {
        'form': form,
        'cart_items': cart_items,
        'user_name': request.user.username,
        'user_email': request.user.email,
        'user_phone': request.user.telefon,
        'current_date': current_time.date,
        'current_time': current_time.time,
        'total_price': total_price
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request):
    # Получение последнего заказа пользователя
    zakaz = Zakaz.objects.filter(ID_User=request.user).order_by('-DataZakaza').first()
    otgruzki = Otgruzka.objects.filter(ID_Zakaz=zakaz)

    total_price = sum(item.cena * item.quantity for item in otgruzki)

    context = {
        'zakaz': zakaz,
        'otgruzki': otgruzki,
        'total_price': total_price,
    }
    return render(request, 'orders/order_success.html', context)

def clear_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            CartItem.objects.filter(user=request.user, is_registered=True).delete()
        else:
            session_id = request.session.session_key
            CartItem.objects.filter(session_id=session_id, is_registered=False).delete()
    return redirect('cart_detail')
