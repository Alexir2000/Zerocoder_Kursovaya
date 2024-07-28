from django.db import models

class Tip_Tovara(models.Model):
    ID = models.AutoField(primary_key=True)
    Tip = models.CharField(max_length=255)

    def __str__(self):
        return self.Tip

class Kat_Tovara(models.Model):
    ID = models.AutoField(primary_key=True)
    Kategoriya = models.CharField(max_length=255)

    def __str__(self):
        return self.Kategoriya

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
