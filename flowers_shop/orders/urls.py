from django.urls import path
from .views import add_to_cart, cart_detail, checkout, admin_order_list, change_order_status

urlpatterns = [
    path('add/<int:tovar_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
    path('admin/orders/', admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/status/', change_order_status, name='change_order_status'),
]
