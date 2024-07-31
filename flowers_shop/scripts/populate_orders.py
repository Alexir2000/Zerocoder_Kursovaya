import os
import django
import random
import sys

# Убедитесь, что путь к корневой папке проекта добавлен в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers_shop.settings')
django.setup()

from main.models import BaseOtziv, Users, Tovar

def populate_reviews():
    users = list(Users.objects.all())
    tovars = list(Tovar.objects.all())

    if not users or not tovars:
        print('Пожалуйста, сначала заполните базу данных пользователями и товарами.')
        return

    reviews_texts = [
        'Отличный товар, очень понравился!',
        'Товар хороший, но доставка задержалась.',
        'Не совсем доволен качеством.',
        'Замечательный продукт! Рекомендую всем.',
        'Приемлемое качество за эту цену.',
        'Очень быстрый сервис и хорошее качество.',
        'Превзошел все ожидания. Спасибо!'
    ]

    # Создание 10 отзывов
    for _ in range(10):
        user = random.choice(users)
        tovar = random.choice(tovars)
        text = random.choice(reviews_texts)
        rating = random.randint(1, 5)
        BaseOtziv.objects.create(
            ID_User=user,
            ID_Tovar=tovar,
            Otziv=text,
            ReitingTovara=rating
        )

if __name__ == '__main__':
    populate_reviews()
    print('Тестовые отзывы успешно добавлены.')
