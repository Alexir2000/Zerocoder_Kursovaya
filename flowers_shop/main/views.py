# flowers_shop/main/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView

from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .models import Adresa, Otgruzka, Zakaz


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  # Перенаправить на главную страницу после регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    next_page = 'index'  # Перенаправление на главную страницу после успешного входа

def index(request):
    return render(request, 'main/index.html')

def custom_logout_view(request):
    logout(request)
    return redirect('index')  # Перенаправление на главную страницу

@login_required
def user_kabinet(request):
    user_orders = Zakaz.objects.filter(ID_User=request.user).order_by('-DataZakaza')
    orders_info = []

    for order in user_orders:
        adresa = Adresa.objects.get(id=order.ID_adres_id)
        otgruzki = Otgruzka.objects.filter(ID_Zakaz=order)
        total_price = sum(item.cena * item.quantity for item in otgruzki)

        orders_info.append({
            'order': order,
            'adresa': adresa,
            'otgruzki': otgruzki,
            'total_price': total_price
        })
    context = {
        'orders_info': orders_info
    }
    return render(request, 'main/user_kabinet.html', context)
