import sqlite3
import random
from aiogram.types import Message
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import WebAppInfo

from tg_bot_manager.config import (TOKEN, URL_API_GET_ZAKAZ, URL_API_OK_PUT_RESPONSE,
                                   URL_API_GET_ZHURNAL_STATUS, URL_API_OK_PUT_ZHURNAL_RESPONSE)
import sqlite3
import aiohttp
import logging
import requests
from datetime import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

button_exchange_rates = KeyboardButton(text="Курс валют")
button_get_zakaz = KeyboardButton(text="Получить заказ")
button_get_zhurnal_status = KeyboardButton(text="Получить журнал статуса")
button_start_auto_requests = KeyboardButton(text="Запуск авто-запросов")
button_stop_auto_requests = KeyboardButton(text="Остановка авто-запросов")

keyboard = ReplyKeyboardMarkup(keyboard=[
    [button_exchange_rates],
    [button_get_zakaz, button_get_zhurnal_status],
    [button_start_auto_requests, button_stop_auto_requests]
], resize_keyboard=True)

auto_request_task = None

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

@dp.message(F.text == "Получить журнал статуса")
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

@dp.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/e0fc67b410005d2ae9827b83/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Не удалось получить данные о курсе валют!")
            return
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']
        euro_to_rub = eur_to_usd * usd_to_rub
        await message.answer(f"1 USD - {usd_to_rub:.2f}  RUB\n"
                             f"1 EUR - {euro_to_rub:.2f}  RUB")
    except:
        await message.answer("Произошла ошибка")

# ++++++++++++++++++++++++++++=================++++++++++++++++++++++

# init_db_bot() # единовременный запуск создания базы. потом комментируем

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

# print_db() # функция печати содержимого базы для проверки.
