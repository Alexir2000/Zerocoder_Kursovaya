from django.shortcuts import render, redirect, get_object_or_404
from main.models import Tovar

from .forms import TovarSearchForm
from orders.models import CartItem
from django.http import JsonResponse
from django.template.loader import render_to_string

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

    cart_items = CartItem.objects.all()
    return render(request, 'catalog/catalog.html', {'tovars': tovars, 'form': form, 'cart_items': cart_items})

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
    return redirect('catalog')  # Изменено на перенаправление обратно на страницу каталога

def cart_detail(request):
    cart_items = CartItem.objects.all()
    return render(request, 'orders/cart_detail.html', {'cart_items': cart_items})
