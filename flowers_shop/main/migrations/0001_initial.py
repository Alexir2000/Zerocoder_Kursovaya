# Generated by Django 5.0.7 on 2024-07-28 19:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kat_Tovara',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Kategoriya', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StatusDostupa',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Status', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StatusZakaza',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Status', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tip_Tovara',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Tip', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tovar',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Nazvanie', models.CharField(max_length=255)),
                ('Cena', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Image', models.ImageField(upload_to='products/')),
                ('Reiting', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('Opisanie', models.TextField()),
                ('ID_KetegorTovara', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.kat_tovara')),
                ('ID_TipTovara', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tip_tovara')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('telefon', models.CharField(max_length=20)),
                ('adres', models.TextField()),
                ('Primechanie', models.TextField(blank=True, null=True)),
                ('ID_vnutr', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('StatusID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.statusdostupa')),
            ],
        ),
        migrations.CreateModel(
            name='BaseOtziv',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Otziv', models.CharField(max_length=500)),
                ('ReitingTovara', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('ID_Tovar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tovar')),
                ('ID_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
            ],
        ),
        migrations.CreateModel(
            name='Zakaz',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('ID_TipZakaza', models.CharField(max_length=255)),
                ('Kolichestvo', models.PositiveIntegerField()),
                ('DataZakaza', models.DateTimeField(auto_now_add=True)),
                ('DataDostavki', models.DateTimeField()),
                ('Polucheno', models.BooleanField(default=False)),
                ('ID_Status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.statuszakaza')),
                ('ID_Tovar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tovar')),
                ('ID_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.users')),
            ],
        ),
        migrations.CreateModel(
            name='Otchet',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Data', models.DateField()),
                ('Itogo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Rashod', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Dohod', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Retab', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ID_Zakaz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.zakaz')),
            ],
        ),
    ]
