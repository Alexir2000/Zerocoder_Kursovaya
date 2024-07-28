from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import CartItem
from flowers_shop.main.models import Tovar
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, tovar_id):
    tovar = Tovar.objects.get(id=tovar_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, tovar=tovar)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'orders/cart_detail.html', {'cart_items': cart_items})
