# flowers_shop/main/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Статусы доступа пользователей
class StatusDostupa(models.Model):
    ID = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=255)
    Opisanie_Dostupa = models.TextField(default="")  # Новое поле для описания статуса доступа

    def __str__(self):
        return self.Status

# Пользователи системы - расширение внутренней базы данных
class CustomUser(AbstractUser):
    StatusID = models.ForeignKey(StatusDostupa, on_delete=models.SET_DEFAULT, default=2)
    telefon = models.CharField(max_length=20, blank=True, default="")
    Primechanie = models.TextField(blank=True, default="")
    tg_Chat_ID = models.CharField(max_length=255, null=True, blank=True)
    tg_User_ID = models.CharField(max_length=255, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Измените related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Измените related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return f"{self.username} ({self.email})"

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
    Img_url = models.URLField(max_length=255)
    Reiting = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    Opisanie = models.TextField()
    ID_TipTovara = models.ForeignKey(Tip_Tovara, on_delete=models.CASCADE)
    ID_KategorTovara = models.ForeignKey(Kat_Tovara, on_delete=models.CASCADE)
    kolich_otzyv = models.IntegerField(default=0)

    def __str__(self):
        return self.Nazvanie

# Статусы заказов
class StatusZakaza(models.Model):
    ID = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=255)

    def __str__(self):
        return self.Status


    def __str__(self):
        return f"Otgruzka {self.ID_Zakaz.id} - {self.tovar_id.Nazvanie}"

class Adresa(models.Model):
    ID = models.AutoField(primary_key=True)
    ID_Zakaz = models.IntegerField(null=True, blank=True)
    ID_User = models.IntegerField(null=True, blank=True)
    Gorod = models.CharField(max_length=255)
    adres = models.TextField(blank=True, default="")
    kontakt = models.CharField(max_length=255, blank=True, default="")
    telefon = models.CharField(max_length=40, blank=True, default="")
    adres_ediniy = models.BooleanField(default=False)
    Nazvanie_adresa = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.Nazvanie_adresa if self.Nazvanie_adresa else f"Adresa {self.id}"

# Заказы
class Zakaz(models.Model):
    ID = models.AutoField(primary_key=True)
    ID_TipZakaza = models.CharField(max_length=255)
    ID_User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Изменено с PROTECT на CASCADE
    ID_adres = models.ForeignKey(Adresa, on_delete=models.SET_NULL, null=True)
    Kolichestvo_klon = models.PositiveIntegerField(default=1)
    Primechanie = models.TextField(max_length=600, blank=True, default="")
    DataZakaza = models.DateTimeField(auto_now_add=True)
    Peredano_v_bot = models.BooleanField(default=False)
    Dostavka_nado = models.BooleanField(default=True)
    Sobrano = models.BooleanField(default=False)
    Data_sborki = models.DateTimeField(null=True, blank=True, default=None)
    Peredano_dostavka = models.BooleanField(default=False)
    Data_peredano_v_dostavku = models.DateTimeField(null=True, blank=True, default=None)
    Zakaz_oplachen = models.BooleanField(default=False)
    Data_Zakaz_oplachen = models.DateTimeField(null=True, blank=True, default=None)
    Zakaz_dostavlen = models.BooleanField(default=False)
    DataDostavki = models.DateTimeField(null=True, blank=True, default=None)
    Zakaz_Poluchen = models.BooleanField(default=False)
    Data_Zakaz_Poluchen = models.DateTimeField(null=True, blank=True, default=None)
    Zakaz_zakryt = models.BooleanField(default=False)
    Data_Zakaz_zakryt = models.DateTimeField(null=True, blank=True, default=None)
    Rashod = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Новое поле
    Profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Новое поле
    ID_Status_zakaza = models.ForeignKey(StatusZakaza, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'Order {self.ID} by {self.ID_User.username}'

class Otgruzka(models.Model):
    ID = models.AutoField(primary_key=True)
    ID_Zakaz = models.ForeignKey(Zakaz, on_delete=models.CASCADE)
    tovar_id = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)

# Отзывы
class BaseOtziv(models.Model):
    ID = models.AutoField(primary_key=True)
    ID_User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ID_Tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    Otziv = models.CharField(max_length=500)
    ReitingTovara = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    date_created =  models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        user_identifier = self.ID_User.email if self.ID_User.email else f"User ID: {self.ID_User.id}"
        return f'Review by {user_identifier} for {self.ID_Tovar.Nazvanie}'


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


class Zhurnal_status_Zakaza(models.Model):
    ID = models.AutoField(primary_key=True)
    ID_Zakaza = models.ForeignKey(Zakaz, on_delete=models.CASCADE)
    Izmenenie = models.CharField(max_length=255)
    pole_izm = models.CharField(max_length=255, blank=True, null=True)
    json_str = models.CharField(max_length=600)
    Date = models.DateTimeField(null=True, blank=True, default=None)
    peredano = models.BooleanField(default=False)
    def __str__(self):
        return f"Изменение {self.Izmenenie} для заказа {self.ID_Zakaza.ID}"
