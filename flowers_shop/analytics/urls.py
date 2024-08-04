# analytics/urls.py

from django.urls import path
from .views import manager_kabinet, update_order_status, zakaz_podrobno

urlpatterns = [
    path('', manager_kabinet, name='manager_kabinet'),
    path('update_order_status/', update_order_status, name='update_order_status'),
    path('zakaz_podrobno/<int:order_id>/', zakaz_podrobno, name='zakaz_podrobno'),
]
