import os
import django
from django.contrib.auth.hashers import make_password

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers_shop.settings')
django.setup()

from flowers_shop.main.models import Users, StatusDostupa

def populate_users():
    status_admin = StatusDostupa.objects.create(Status='Администратор', Opisanie_Dostupa='Полный доступ')
    status_user = StatusDostupa.objects.create(Status='Пользователь', Opisanie_Dostupa='Ограниченный доступ')

    Users.objects.create(
        email='admin@example.com',
        telefon='+1234567890',
        adres='Адрес администратора',
        Primechanie='Примечание администратора',
        StatusID=status_admin,
        password=make_password('admin_password')  # Пароль администратора
    )

    for i in range(1, 11):
        Users.objects.create(
            email=f'user{i}@example.com',
            telefon=f'+123456789{i}',
            adres=f'Адрес пользователя {i}',
            Primechanie=f'Примечание пользователя {i}',
            StatusID=status_user,
            password=None  # Пользователи без пароля
        )

if __name__ == '__main__':
    populate_users()
    print('Тестовые пользователи успешно добавлены.')
