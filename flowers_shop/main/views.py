# flowers_shop/main/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .models import Adresa, Otgruzka, Zakaz
from orders.models import CartItem

def link_cart_to_user(session_id, user):
    if session_id:
        cart_items = CartItem.objects.filter(session_id=session_id, is_registered=False)
        for item in cart_items:
            item.user = user
            item.is_registered = True
            item.save()


def register(request):
    session_id = request.session.session_key
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            link_cart_to_user(session_id, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    next_page = 'index'  # Перенаправление на главную страницу после успешного входа

    def form_valid(self, form):
        session_id = self.request.session.session_key
        response = super().form_valid(form)
        link_cart_to_user(session_id, self.request.user)
        return response

def index(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.save()
        session_id = request.session.session_key

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_registered=True)
    else:
        cart_items = CartItem.objects.filter(session_id=session_id, is_registered=False)

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'main/index.html', context)

def custom_logout_view(request):
    logout(request)
    return redirect('index')  # Перенаправление на главную страницу

@login_required
def user_kabinet(request):
    # Получение заказов пользователя
    user_orders = Zakaz.objects.filter(ID_User=request.user).order_by('-DataZakaza')
    orders_info = []

    for order in user_orders:
        try:
            adresa = Adresa.objects.get(ID=order.ID_adres_id)
        except Adresa.DoesNotExist:
            adresa = None
        otgruzki = Otgruzka.objects.filter(ID_Zakaz=order)
        total_price = sum(item.cena * item.quantity for item in otgruzki)

        orders_info.append({
            'order': order,
            'adresa': adresa,
            'otgruzki': otgruzki,
            'total_price': total_price
        })

    # Получение данных корзины (как в каталоге)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_registered=True)
    else:
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id, is_registered=False)

    total_cart_price = sum(item.cena * item.quantity for item in cart_items)

    context = {
        'orders_info': orders_info,
        'cart_items': cart_items,  # Добавление данных корзины в контекст
        'total_price': total_cart_price  # Общая стоимость товаров в корзине
    }
    return render(request, 'main/user_kabinet.html', context)


@login_required
def repeat_order(request, order_id):
    order = get_object_or_404(Zakaz, ID=order_id, ID_User=request.user)
    otgruzki = Otgruzka.objects.filter(ID_Zakaz=order)

    for item in otgruzki:
        cart_item, created = CartItem.objects.get_or_create(tovar=item.tovar_id, user=request.user, is_registered=True)
        if not created:
            cart_item.quantity += item.quantity
        else:
            cart_item.quantity = item.quantity
        cart_item.cena = item.cena
        cart_item.save()

    return redirect('cart_detail')
