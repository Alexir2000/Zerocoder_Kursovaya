# flowers_shop/catalog/views.py

from django.shortcuts import render, redirect
from main.models import Tovar, Kat_Tovara, Tip_Tovara
from .forms import TovarSearchForm
from orders.models import CartItem

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

    return render(request, 'catalog/catalog.html', {'tovars': tovars, 'form': form})

def add_to_cart(request, tovar_id):
    tovar = Tovar.objects.get(ID=tovar_id)  # Используем ID для идентификатора
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(tovar=tovar)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return redirect('cart_detail')