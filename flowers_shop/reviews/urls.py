from django.urls import path
from .views import add_review, tovar_reviews, reviews_list

urlpatterns = [
    path('add/<int:tovar_id>/', add_review, name='add_review'),
    path('tovar/<int:tovar_id>/', tovar_reviews, name='tovar_reviews'),
    path('', reviews_list, name='reviews_list'),  # Новый URL для списка отзывов
]
