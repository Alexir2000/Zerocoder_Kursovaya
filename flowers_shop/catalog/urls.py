# flowers_shop/catalog/urls.py

from django.urls import path
from .views import catalog_view, karta_tovara, otzyv_na_tovar
from . import views

urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('karta_tovara/', karta_tovara, name='karta_tovara'),
    path('karta_tovara/<int:pk>/', karta_tovara, name='karta_tovara'),
    path('otzyv_na_tovar/<int:pk>/', otzyv_na_tovar, name='otzyv_na_tovar'),
    path('catalog_put_zakaz', views.catalog_put_zakaz, name='catalog_put_zakaz'),
    path('Ok_put_response', views.ok_put_response, name='ok_put_response'),
    path('put_zhurnal_status', views.put_zhurnal_status, name='put_zhurnal_status'),
    path('Ok_put_zhurnal_response', views.ok_put_zhurnal_response, name='ok_put_zhurnal_response'),
]
