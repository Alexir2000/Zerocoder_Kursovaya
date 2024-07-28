from django.db import models
from main.models import Users, Tovar

class CartItem(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.tovar.Nazvanie} (x{self.quantity})'
