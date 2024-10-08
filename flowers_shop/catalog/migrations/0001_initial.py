# Generated by Django 5.0.7 on 2024-07-28 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('ID_KetegorTovara', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.kat_tovara')),
                ('ID_TipTovara', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.tip_tovara')),
            ],
        ),
    ]
