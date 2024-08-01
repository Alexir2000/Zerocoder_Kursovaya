from django.urls import path
from .views import add_to_cart, cart_detail, checkout, order_success, clear_cart

urlpatterns = [
    path('add_to_cart/<int:tovar_id>/', add_to_cart, name='add_to_cart'),
    path('cart_detail/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('order_success/', order_success, name='order_success'),
    path('clear_cart/', clear_cart, name='clear_cart'),
]
