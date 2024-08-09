# analytics/urls.py

from django.urls import path
from .views import (manager_kabinet, update_order_status, zakaz_podrobno,
    tovar_edit, clear_zhurnal, analytics_view, tovar_create)
from . import views

urlpatterns = [
    path('', manager_kabinet, name='manager_kabinet'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('zakaz_podrobno/<int:order_id>/', zakaz_podrobno, name='zakaz_podrobno'),
    path('clear_zhurnal/', clear_zhurnal, name='clear_zhurnal'),  # Добавлен новый путь
    path('analytics/', analytics_view, name='analytics_view'),  # Маршрут для страницы аналитики
    path('tovar_edit/<int:pk>/', tovar_edit, name='tovar_edit'),  # маршрут для редактирования товара
    path('tovar_create/', tovar_create, name='tovar_create'),  # Новый маршрут для создания товара
    path('put_analytics', views.put_analytics, name='put_analytics'),
]
