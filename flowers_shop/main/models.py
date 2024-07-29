from django.db import models
from django.contrib.auth.models import User

# Статусы доступа пользователей
class StatusDostupa(models.Model):
    ID = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=255)
    Opisanie_Dostupa = models.TextField(default="")  # Новое поле для описания статуса доступа

    def __str__(self):
        return self.Status

# Пользователи системы
class Users(models.Model):
    ID = models.AutoField(primary_key=True)
    StatusID = models.ForeignKey(StatusDostupa, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    telefon = models.CharField(max_length=20)
    adres = models.TextField()
    Primechanie = models.TextField(null=True, blank=True)
    ID_vnutr = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)  # Новое поле для пароля

    def __str__(self):
        return self.email

# Типы товаров
class Tip_Tovara(models.Model):
    ID = models.AutoField(primary_key=True)
    Tip = models.CharField(max_length=255)

    def __str__(self):
        return self.Tip

# Категории товаров
class Kat_Tovara(models.Model):
    ID = models.AutoField(primary_key=True)
    Kategoriya = models.CharField(max_length=255)

    def __str__(self):
        return self.Kategoriya

# Товары
class Tovar(models.Model):
    ID = models.AutoField(primary_key=True)
    Nazvanie = models.CharField(max_length=255)
    Cena = models.DecimalField(max_digits=10, decimal_places=2)
    Image = models.ImageField(upload_to='products/')
    Reiting = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    Opisanie = models.TextField()
    ID_TipTovara = models.ForeignKey(Tip_Tovara, on_delete=models.CASCADE)
    ID_KetegorTovara = models.ForeignKey(Kat_Tovara, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nazvanie

# Статусы заказов
class StatusZakaza(models.Model):
    ID = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=255)

    def __str__(self):
        return self.Status

# Заказы
class Zakaz(models.Model):
    ID = models.AutoField(primary_key=True)
    ID_TipZakaza = models.CharField(max_length=255)
    ID_User = models.ForeignKey(Users, on_delete=models.CASCADE)
    ID_Tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    Kolichestvo = models.PositiveIntegerField()
    DataZakaza = models.DateTimeField(auto_now_add=True)
    DataDostavki = models.DateTimeField()
    Polucheno = models.BooleanField(default=False)
    ID_Status = models.ForeignKey(StatusZakaza, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order {self.ID} by {self.ID_User.email}'

# Отзывы
class BaseOtziv(models.Model):
    ID = models.AutoField(primary_key=True)
    ID_User = models.ForeignKey(Users, on_delete=models.CASCADE)
    ID_Tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    Otziv = models.CharField(max_length=500)
    ReitingTovara = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f'Review by {self.ID_User.email} for {self.ID_Tovar.Nazvanie}'

# Отчеты
class Otchet(models.Model):
    ID = models.AutoField(primary_key=True)
    Data = models.DateField()
    ID_Zakaz = models.ForeignKey(Zakaz, on_delete=models.CASCADE)
    Itogo = models.DecimalField(max_digits=10, decimal_places=2)
    Rashod = models.DecimalField(max_digits=10, decimal_places=2)
    Dohod = models.DecimalField(max_digits=10, decimal_places=2)
    Retab = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Otchet for {self.Data} - Order {self.ID_Zakaz.ID}'
