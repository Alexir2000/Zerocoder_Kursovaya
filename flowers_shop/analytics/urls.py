# analytics/urls.py

from django.urls import path
from .views import manager_kabinet, update_order_status, zakaz_podrobno, clear_zhurnal, analytics_view
from . import views

urlpatterns = [
    path('', manager_kabinet, name='manager_kabinet'),
    path('update_order_status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('zakaz_podrobno/<int:order_id>/', zakaz_podrobno, name='zakaz_podrobno'),
    path('clear_zhurnal/', clear_zhurnal, name='clear_zhurnal'),  # Добавлен новый путь
    path('analytics/', analytics_view, name='analytics_view'),  # Маршрут для страницы аналитики
    path('put_analytics', views.put_analytics, name='put_analytics'),
]
