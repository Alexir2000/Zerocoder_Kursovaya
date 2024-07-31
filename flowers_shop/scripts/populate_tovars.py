import os
import django
import sys
import random

# Установка пути к проекту и настройка Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers_shop.settings')
django.setup()

from main.models import Tovar, Tip_Tovara, Kat_Tovara

def generate_random_description():
    words = [
        "Цветок", "красивый", "яркий", "весенний", "летний", "осенний", "зимний", "ароматный", "свежий", "прекрасный",
        "нежный", "изящный", "благородный", "неповторимый", "волшебный", "особенный", "необычный", "уникальный"
    ]
    return ' '.join(random.sample(words, random.randint(7, 10)))

def populate_tovars():
    # Создание типа товаров
    tip1 = Tip_Tovara.objects.create(Tip='Цветы')
    tip2 = Tip_Tovara.objects.create(Tip='Аксессуары')

    # Создание категорий товаров
    kat1 = Kat_Tovara.objects.create(Kategoriya='Свежие цветы')
    kat2 = Kat_Tovara.objects.create(Kategoriya='Букеты')
    kat3 = Kat_Tovara.objects.create(Kategoriya='Цветы в горшках')

    # Списки данных для товаров
    categories = [kat1, kat2, kat3]
    names = [
        'Красная роза', 'Желтый тюльпан', 'Белая лилия', 'Розовая гвоздика', 'Фиолетовая орхидея',
        'Белая хризантема', 'Синий ирис', 'Розовый пион', 'Лаванда', 'Нарцисс'
    ]
    prices = [100.00, 70.00, 120.00, 80.00, 200.00, 90.00, 110.00, 150.00, 60.00, 50.00]

    # Создание товаров
    for i in range(10):
        Tovar.objects.create(
            Nazvanie=names[i],
            Cena=prices[i],
            Opisanie=generate_random_description(),
            ID_TipTovara=tip1,
            ID_KategorTovara=categories[i % len(categories)]
        )

if __name__ == '__main__':
    populate_tovars()
    print('Товары успешно добавлены.')
