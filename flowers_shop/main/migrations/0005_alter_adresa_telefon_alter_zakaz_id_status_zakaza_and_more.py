# Generated by Django 5.0.7 on 2024-08-04 18:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_adresa_rename_id_status_zakaz_id_status_zakaza_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adresa',
            name='telefon',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='zakaz',
            name='ID_Status_zakaza',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.statuszakaza'),
        ),
        migrations.CreateModel(
            name='Zhurnal_status_Zakaza',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Izmenenie', models.CharField(max_length=255)),
                ('pole_izm', models.CharField(blank=True, max_length=255, null=True)),
                ('json_str', models.CharField(max_length=600)),
                ('ID_Zakaza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.zakaz')),
            ],
        ),
    ]
