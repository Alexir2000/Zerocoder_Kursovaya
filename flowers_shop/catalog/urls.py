# flowers_shop/catalog/urls.py

from django.urls import path
from .views import catalog_view
from . import views

urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('catalog_put_korzina', views.catalog_put_korzina, name='catalog_put_korzina'),
    path('catalog_put_zakaz', views.catalog_put_zakaz, name='catalog_put_zakaz'),
    path('Ok_put_response', views.ok_put_response, name='ok_put_response'),
]
