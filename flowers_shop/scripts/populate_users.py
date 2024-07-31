import django
from django.contrib.auth.hashers import make_password
import os
import sys

# Убедитесь, что путь к корневой папке проекта добавлен в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers_shop.settings')
django.setup()

from main.models import Users, StatusDostupa

def populate_users():
    status_admin = StatusDostupa.objects.create(Status='admin', Opisanie_Dostupa='Полный доступ')
    status_user = StatusDostupa.objects.create(Status='user', Opisanie_Dostupa='Обычный доступ')
    status_manager = StatusDostupa.objects.create(Status='manager', Opisanie_Dostupa='Доступ к статистике')

    Users.objects.create(
        email='admin@admin.ru',
        telefon='+1234567890',
        adres='Адрес администратора',
        Primechanie='Примечание администратора',
        StatusID=status_admin,
        password=make_password('admin'),  # Пароль администратора
        Name="Иван",
        Family="Иванов"
    )
    names = [
        ('Иван', 'Иванов'),
        ('Анна', 'Смирнова'),
        ('Дмитрий', 'Кузнецов'),
        ('Елена', 'Попова'),
        ('Алексей', 'Лебедев'),
        ('Мария', 'Новикова'),
        ('Сергей', 'Козлов'),
        ('Ольга', 'Морозова'),
        ('Николай', 'Соколов'),
        ('Наталья', 'Волкова')
    ]

    for i in range(1, 10):
        Users.objects.create(
            email=f'user{i}@example.com',
            telefon=f'+123456789{i}',
            adres=f'Адрес пользователя {i}',
            Primechanie=f'Примечание пользователя {i}',
            StatusID=status_user,
            password=None,  # Пользователи без пароля
            Name = names[i - 1][0],
            Family = names[i - 1][1]
        )

if __name__ == '__main__':
    populate_users()
    print('Тестовые пользователи успешно добавлены.')
