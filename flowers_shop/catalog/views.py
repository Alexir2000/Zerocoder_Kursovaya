from django.shortcuts import render, redirect, get_object_or_404
from .forms import TovarSearchForm
from orders.models import CartItem
from main.models import Tovar

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
