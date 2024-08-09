# tg_bot/tg_bot_main.py

import logging
import requests
from datetime import datetime, timedelta
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tg_bot_manager.config import (TOKEN, URL_API_GET_ZAKAZ, URL_API_OK_PUT_RESPONSE,
                                   URL_API_GET_ZHURNAL_STATUS, URL_API_OK_PUT_ZHURNAL_RESPONSE,
                                   URL_API_GET_ANALITICS)


bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

button_get_zakaz = KeyboardButton(text="Получить заказ")
button_get_zhurnal_status = KeyboardButton(text="Получить журнал статусов")
button_start_auto_requests = KeyboardButton(text="Запуск авто-запросов")
button_stop_auto_requests = KeyboardButton(text="Остановка авто-запросов")
button_get_analytics = KeyboardButton(text="Получить аналитику")
button_set_analytics_period = KeyboardButton(text="Ввод периода аналитики")


keyboard = ReplyKeyboardMarkup(keyboard=[
    [button_get_zakaz, button_get_zhurnal_status],
    [button_start_auto_requests, button_stop_auto_requests],
    [button_get_analytics, button_set_analytics_period]
], resize_keyboard=True)

auto_request_task = None

start_date = (datetime.now() - timedelta(days=7)).strftime("%d.%m.%Y")
end_date = datetime.now().strftime("%d.%m.%Y")

# Создайте класс состояния для ввода дат
class AnalyticsPeriod(StatesGroup):
    waiting_for_start_date = State()
    waiting_for_end_date = State()

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

def parse_custom_date(date_str):
    """
    Парсит дату из строки в различных форматах (дд.мм.гггг, дд/мм/гггг, дд.мм, дд/мм)
    и возвращает дату в формате дд.мм.гггг.
    """
    current_year = datetime.now().year
    formats = ["%d.%m.%Y", "%d/%m/%Y", "%d.%m", "%d/%m"]
    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt)
            if fmt in ["%d.%m", "%d/%m"]:
                date = date.replace(year=current_year)
            return date.strftime("%d.%m.%Y")
        except ValueError:
            continue
    return None

# Функция для получения аналитики
async def get_analytics(message: Message):
    url = URL_API_GET_ANALITICS
    global start_date, end_date
    if not start_date or not end_date:
        await message.answer("Период аналитики не установлен. Пожалуйста, используйте команду 'Ввод периода аналитики' для установки периода.")
        return

    try:
        response = requests.get(url, params={'start_date': start_date, 'end_date': end_date})
        data = response.json()
        if 'error' in data:
            await message.answer("Ошибка получения аналитики")
            return

        response_message = (
            f"Период с {data['date_s']} по {data['date_po']}:\n"
            f"Общая сумма заказов: {data['total_sum']} руб.\n"
            f"Общее количество заказов: {data['total_orders']}\n"
            f"Общая сумма затрат: {data['total_rashod']} руб.\n"
            f"Общая сумма прибыли: {data['total_profit']} руб.\n"
            f"Средний чек: {data['average_order_value']} руб."
        )
        await message.answer(response_message)
    except Exception as e:
        logging.error(f"Произошла ошибка при получении данных: {str(e)}")
        await message.answer("Произошла ошибка при получении аналитики")


async def auto_request_zakaz():
    while True:
        await fetch_zakaz()
        await fetch_zhurnal_status()
        await asyncio.sleep(2)

async def fetch_zakaz():
    url = URL_API_GET_ZAKAZ
    ok_put_response_url = URL_API_OK_PUT_RESPONSE
    try:
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            return
        response_message = (
            f"Вид Отправки: {data['Vid_Put']}\n"
            f"ID Заказа: {data['ID']}\n"
            f"Дата: {data['Data']}\n"
            f"Адрес доставки: {data['Adres']}\n"
            f"Контактное лицо: {data['Kontakt']}\n"
            f"Телефон: {data['Telefon']}\n"
            f"Примечание: {data['Primechanie']}\n"
            f"Товары:\n"
        )
        for item in data['Tovary']:
            response_message += f"  - {item['Nazvanie']}: {item['Cena']} руб. x {item['Kolichestvo']}\n"
        response_message += f"Общая стоимость: {data['Obshaya_Stoimost']} руб."
        await bot.send_message(chat_id, response_message)
        confirm_response = requests.post(ok_put_response_url, json={'ID': data['ID']})
        confirm_data = confirm_response.json()
        if confirm_data.get('Status') == 'Put_OK':
            await bot.send_message(chat_id, f"Заказ ID {data['ID']} подтвержден.")
        else:
            await bot.send_message(chat_id, f"Ошибка подтверждения заказа ID {data['ID']}.")
    except Exception as e:
        logging.error(f"Произошла ошибка при получении данных: {str(e)}")

# Проверка журнала  на обновление статусов заказов
async def fetch_zhurnal_status():
    url = URL_API_GET_ZHURNAL_STATUS
    ok_put_response_url = URL_API_OK_PUT_ZHURNAL_RESPONSE
    try:
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            return
        date_str = data.get('Date')
        date_obj = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        response_message = (
            f"Произошло изменение статуса заказа номер {data.get('ID_Zakaza')}. "
            f"Дата изменения - {date_obj:%d.%m.%Y %H:%M}\n"
            f"Поле изменения: {data.get('pole_izm')}\n"
            f"Состояние статуса: {data.get('Izmenenie')}\n"

        )
        await bot.send_message(chat_id, response_message)
        confirm_response = requests.post(ok_put_response_url, json={'ID': data['ID']})
        confirm_data = confirm_response.json()
        if confirm_data.get('Status') == 'Put_OK':
            pass # await bot.send_message(chat_id, f"Запись ID {data['ID']} подтверждена.")
        else:
            await bot.send_message(chat_id, f"Ошибка подтверждения записи ID {data['ID']}.")
    except Exception as e:
        pass  # Обработка исключений без логирования



@dp.message(F.text == "Ввод периода аналитики")
async def set_analytics_period(message: Message, state: FSMContext):
    await message.answer("Введите дату окончания периода в формате дд.мм.гггг или дд/мм/гггг или дд.мм или дд/мм")
    await state.set_state(AnalyticsPeriod.waiting_for_start_date)

@dp.message(AnalyticsPeriod.waiting_for_start_date)
async def process_start_date(message: Message, state: FSMContext):
    global start_date
    parsed_date = parse_custom_date(message.text)
    if parsed_date:
        start_date = parsed_date
        await message.answer("Введите дату окончания периода в формате дд.мм.гггг или дд/мм/гггг или дд.мм или дд/мм")
        await state.set_state(AnalyticsPeriod.waiting_for_end_date)
    else:
        await message.answer("Неправильный формат даты. Введите дату в формате дд.мм.гггг, дд/мм/гггг, дд.мм или дд/мм")


@dp.message(AnalyticsPeriod.waiting_for_end_date)
async def process_end_date(message: Message, state: FSMContext):
    global end_date
    parsed_end_date = parse_custom_date(message.text)
    if parsed_end_date:
        end_date = parsed_end_date
    else:
        end_date = start_date
        await message.answer(f"Дата окончания введена некорректно и была приравнена к дате начала: {start_date}",
                             reply_markup=keyboard)

    start_date_dt = datetime.strptime(start_date, "%d.%m.%Y")
    end_date_dt = datetime.strptime(end_date, "%d.%m.%Y")
    if end_date_dt < start_date_dt:
        end_date = start_date
        await message.answer(f"Дата окончания введена некорректно и была приравнена к дате начала: {start_date}",
                             reply_markup=keyboard)

    await message.answer(f"Период аналитики установлен с {start_date} по {end_date}", reply_markup=keyboard)
    await state.clear()


@dp.message(F.text == "Получить аналитику")
async def get_analytics_command(message: Message):
    await get_analytics(message)

@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    global chat_id
    chat_id = message.chat.id
    await message.answer("Привет! Выберите кнопку с действием", reply_markup=keyboard)

@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer("Тут помощь. Есть такие команды: \n "
                         "/del_registr - удалить регистрацию \n ")

@dp.message(F.text == "Получить заказ")
async def get_zakaz_from_site(message: Message):
    await fetch_zakaz()

@dp.message(F.text == "Получить журнал статусов")
async def get_zhurnal_status_from_site(message: Message):
    await fetch_zhurnal_status()

@dp.message(F.text == "Запуск авто-запросов")
async def start_auto_requests(message: Message):
    global auto_request_task
    if auto_request_task is None:
        auto_request_task = asyncio.create_task(auto_request_zakaz())
        await message.answer("Автоматические запросы запущены.")
    else:
        await message.answer("Автоматические запросы уже запущены.")

@dp.message(F.text == "Остановка авто-запросов")
async def stop_auto_requests(message: Message):
    global auto_request_task
    if auto_request_task:
        auto_request_task.cancel()
        auto_request_task = None
        await message.answer("Автоматические запросы остановлены.")
    else:
        await message.answer("Автоматические запросы не запущены.")

# ++++++++++++++++++++++++++++=================++++++++++++++++++++++

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

