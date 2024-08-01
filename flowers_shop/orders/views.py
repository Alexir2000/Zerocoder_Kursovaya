from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from main.models import Tovar
from .forms import OrderForm
from datetime import timezone

def add_to_cart(request, tovar_id):
    if request.method == "POST":
        tovar = get_object_or_404(Tovar, ID=tovar_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(tovar=tovar)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
    return redirect('catalog')

def cart_detail(request):
    cart_items = CartItem.objects.all()
    return render(request, 'orders/cart_detail.html', {'cart_items': cart_items})

def checkout(request):
    cart_items = CartItem.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = sum(item.tovar.Cena * item.quantity for item in cart_items)
            order.save()
            cart_items.delete()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'orders/checkout.html', {'form': form, 'cart_items': cart_items})

def order_success(request):
    return render(request, 'orders/order_success.html')

def clear_cart(request):
    if request.method == 'POST':
        CartItem.objects.all().delete()
    return redirect('cart_detail')
