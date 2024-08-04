# catalog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import TovarSearchForm
from orders.models import CartItem
from main.models import Tovar


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