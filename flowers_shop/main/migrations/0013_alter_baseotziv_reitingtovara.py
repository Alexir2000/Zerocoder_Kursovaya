# Generated by Django 5.0.7 on 2024-08-08 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_baseotziv_reitingtovara'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseotziv',
            name='ReitingTovara',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]
