# Generated by Django 5.0.7 on 2024-07-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusdostupa',
            name='Opisanie_Dostupa',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
