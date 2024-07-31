# flowers_shop/catalog/views.py

from django.shortcuts import render
from main.models import Tovar, Kat_Tovara, Tip_Tovara
from .forms import TovarSearchForm

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
