
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import CartItem
from main.models import Zakaz
from main.models import Tovar
from django.contrib.auth.decorators import login_required
from .models import CartItem
from .forms import OrderForm
from datetime import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from main.models import StatusZakaza

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

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Zakaz.objects.create(
                ID_User=request.user,
                ID_Tovar=cart_items[0].tovar,  # пример, для каждого товара нужен свой заказ
                Kolichestvo=cart_items[0].quantity,
                DataZakaza=timezone.now(),
                DataDostavki=form.cleaned_data['address'],
                Polucheno=False,
                ID_Status=1  # начальный статус
            )
            cart_items.delete()  # очищаем корзину
            return redirect('order_success')
    else:
        form = OrderForm(initial={'user': request.user})

    return render(request, 'orders/checkout.html', {'form': form, 'cart_items': cart_items})

@staff_member_required
def admin_order_list(request):
    orders = Zakaz.objects.all()
    return render(request, 'orders/admin_order_list.html', {'orders': orders})

@staff_member_required
def change_order_status(request, order_id):
    order = get_object_or_404(Zakaz, id=order_id)
    if request.method == 'POST':
        new_status_id = request.POST.get('status')
        new_status = get_object_or_404(StatusZakaza, id=new_status_id)
        order.ID_Status = new_status
        order.save()
        return redirect('admin_order_list')
    statuses = StatusZakaza.objects.all()
    return render(request, 'orders/change_order_status.html', {'order': order, 'statuses': statuses})
