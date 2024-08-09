# orders/models.py
from django.db import models
from django.conf import settings
from main.models import Tovar

class CartItem(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    is_registered = models.BooleanField(default=False)
    cena = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.tovar.Nazvanie} ({self.quantity})"
