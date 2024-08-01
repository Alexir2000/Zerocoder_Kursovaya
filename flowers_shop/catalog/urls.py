# flowers_shop/catalog/urls.py

from django.urls import path
from .views import catalog_view, add_to_cart

urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('add_to_cart/<int:tovar_id>/', add_to_cart, name='add_to_cart'),
]
