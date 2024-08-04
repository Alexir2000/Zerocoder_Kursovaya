from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('tovar', 'quantity', 'user', 'session_id', 'is_registered', 'cena')
    search_fields = ('tovar__Nazvanie', 'user__username', 'session_id')
    list_filter = ('is_registered', 'user')