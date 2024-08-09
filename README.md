# Flower Shop

## Описание проекта

Проект "Flower Shop" представляет собой веб-приложение для заказа цветов с интеграцией через Telegram-бота. Пользователи могут регистрироваться, просматривать каталог товаров, добавлять товары в корзину, оформлять заказы, оставлять отзывы и получать аналитику по заказам. Администраторы могут управлять заказами и просматривать аналитические данные. Проект реализован на Django и использует Telegram-бота на базе Aiogram для взаимодействия с пользователями.

## Содержание

- [Требования](#требования)
- [Установка](#установка)
- [Настройка](#настройка)
- [Архитектура проекта](#архитектура-проекта)
- [Документация проекта](#документация-проекта)
- [Функционал и особенности проекта](#функционал-и-особенности-проекта)
- [Административный функционал проекта](#административный-функционал-проекта)
- [Технические особенности реализации проекта](#технические-особенности-реализации-проекта)
- [Авторы и благодарности](#авторы-и-благодарности)

## Требования

Для работы проекта "Flower Shop" необходимы следующие зависимости и окружение:

- **Python 3.8+**: Основной язык программирования, на котором написан проект.
- **Django**: Веб-фреймворк, используемый для реализации сайта.
- **Aiogram**: Библиотека для создания Telegram-бота.
- **SQLite**: Используется в качестве базы данных по умолчанию.
- **Библиотеки Python**: Все необходимые библиотеки и их версии перечислены в файле `requirements.txt`.

## Установка

Для установки проекта выполните следующие шаги:

1. **Клонируйте репозиторий**:
   git clone https://github.com/Alexir2000/Zerocoder_Kursovaya
   cd flowers_shop

2. **Создайте виртуальное окружение**:
   python3 -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate

3. **Установите зависимости**:
   pip install -r requirements.txt

4. **Выполните миграции базы данных**:
   python manage.py migrate

5. **Запустите сервер разработки**:
   python manage.py runserver

6. **Настройка Telegram-бота**:
   - Перейдите в раздел "Настройка" для получения инструкций по настройке Telegram-бота и API.

## Настройка

для доступа на сайт в качестве superuser введите 

login Alex password 123

для доступа на сайт в качестве менеджера-администратора введите

login Manager1 password 123

Перед запуском проекта необходимо настроить следующие параметры:

1. **Рабочие часы магазина**:
   - Откройте файл `flowers_shop/settings.py` и установите рабочие часы магазина:
     - TIME_WORK_ON = "8:00:00"
     - TIME_WORK_OFF = "23:00:00"

2. **Настройка API для Telegram-бота**:
   - Откройте файл `tg_bot/tg_bot_manager/config.py` и измените пути к API на актуальные:
     - URL_BASE = "http://example.com"
     - URL_API_GET_ZAKAZ = "http://example.com/catalog/catalog_put_zakaz"
     - URL_API_OK_PUT_RESPONSE = "http://example.com/catalog/Ok_put_response"
     - URL_API_GET_ZHURNAL_STATUS = "http://example.com/catalog/put_zhurnal_status"
     - URL_API_OK_PUT_ZHURNAL_RESPONSE = "http://example.com/catalog/Ok_put_zhurnal_response"
     - URL_API_GET_ANALITICS = "http://example.com/analytics/put_analytics"

   - Вставьте актуальный ключ Telegram-бота в переменную `TOKEN`:
     - TOKEN = 'Ваш токен бота телеграм'

3. **Дополнительные настройки**:
   - Проверьте все остальные параметры конфигурации в файлах `settings.py` и `config.py` на соответствие вашему окружению и измените их при необходимости.

4. **Загрузка актуальных файлов конфигурации и базы данных**:

   - Скачайте актуальные файлы `config.py` и `db.sqlite3` из облака по [этой ссылке](https://disk.yandex.ru/d/o0Cdw7thEwBfgg).
   
   - Поместите файл `config.py` в папку `/tg_bot/tg_bot_manager/`
   - Поместите файл db.sqlite3 в корневую папку проекта flowers_shop/



## Архитектура проекта

Для просмотра структуры проекта перейдите по [ссылке на актуальное дерево файлов проекта](TZ_Documentation/Актуальное%20дерево%20файлов%20проекта.md).

## Документация проекта

- [Описание и структура проекта](TZ_Documentation/Описание%20и%20структура%20проекта.txt)
- [Описание моделей баз данных проекта](TZ_Documentation/Описание%20моделей%20Баз%20данных%20проекта.txt)
- [Техническое задание проекта](TZ_Documentation/Техзадание%20проекта%20Expert.txt)

## Функционал и особенности проекта

для доступа на сайт в качестве superuser введите 
login Alex password 123

для доступа на сайт в качестве менеджера-администратора введите
login Manager1 password 123

Подробное описание функционала проекта доступно [здесь](TZ_Documentation/Функционал%20и%20особенности%20проекта.md).

## Административный функционал проекта

Подробное описание административного функционала проекта доступно [здесь](TZ_Documentation/Административный%20функционал%20проекта.md).

## Технические особенности реализации проекта

Подробное описание технических особенностей реализации проекта доступно [здесь](TZ_Documentation/Технические%20особенности%20реализации%20проекта.md).

## Авторы и благодарности

- **Автор:** Булавин Алексей
- **Благодарности:** Коллективу школы Zerocoder за всестороннее и глубокое обучение и раскрытие темы.
