from django.urls import path
from .views import add_review, tovar_reviews

urlpatterns = [
    path('add/<int:tovar_id>/', add_review, name='add_review'),
    path('<int:tovar_id>/', tovar_reviews, name='tovar_reviews'),
]
