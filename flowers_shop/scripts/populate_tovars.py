import os
import django

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers_shop.settings')
django.setup()

from flowers_shop.main.models import Tovar, Tip_Tovara, Kat_Tovara


def populate_tovars():
    # Создание типов и категорий товаров
    tip1 = Tip_Tovara.objects.create(Tip='Цветы')
    tip2 = Tip_Tovara.objects.create(Tip='Букеты')

    kat1 = Kat_Tovara.objects.create(Kategoriya='Розы')
    kat2 = Kat_Tovara.objects.create(Kategoriya='Тюльпаны')
    kat3 = Kat_Tovara.objects.create(Kategoriya='Лилии')

    # Создание товаров
    Tovar.objects.create(Nazvanie='Роза красная', Cena=100.00, Image='products/roza_krasnaya.jpg', Reiting=4.5,
                         Opisanie='Красная роза', ID_TipTovara=tip1, ID_KetegorTovara=kat1)
    Tovar.objects.create(Nazvanie='Тюльпан желтый', Cena=70.00, Image='products/tyulpan_zheltyj.jpg', Reiting=4.0,
                         Opisanie='Желтый тюльпан', ID_TipTovara=tip1, ID_KetegorTovara=kat2)
    Tovar.objects.create(Nazvanie='Лилия белая', Cena=120.00, Image='products/liliya_belaya.jpg', Reiting=4.7,
                         Opisanie='Белая лилия', ID_TipTovara=tip1, ID_KetegorTovara=kat3)
    Tovar.objects.create(Nazvanie='Букет роз', Cena=1500.00, Image='products/buket_roz.jpg', Reiting=4.8,
                         Opisanie='Букет красных роз', ID_TipTovara=tip2, ID_KetegorTovara=kat1)


if __name__ == '__main__':
    populate_tovars()
    print('Тестовые товары успешно добавлены.')
