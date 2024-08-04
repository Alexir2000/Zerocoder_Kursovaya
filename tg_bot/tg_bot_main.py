
# документация по aiogram https://docs.aiogram.dev/en/dev-3.x/

import sqlite3
import random
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from aiogram.types import Message
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram. filters import CommandStart, Command
from aiogram. types import Message, FSInputFile
from aiogram. fsm. context import FSMContext
from aiogram. fsm.state import State, StatesGroup
from aiogram. fsm. storage. memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import WebAppInfo

from tg_bot_manager.config import TOKEN, URL_API_GET_KORZINA, URL_API_GET_ZAKAZ
import sqlite3
import aiohttp
import logging
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

url_site = "https://localhost:8000/catalog/"
url_site = "https://www.mebelhit.ru/"

button_exchange_rates = KeyboardButton(text="Курс валют")
button_get_korzina = KeyboardButton(text="Получить корзину")
button_get_zakaz = KeyboardButton(text="Получить заказ")
# button_run_flowers_shop = KeyboardButton(text="Магазин цветов", web_app=WebAppInfo(url=url_site))


keyboard = ReplyKeyboardMarkup(keyboard=[
    [ button_exchange_rates, button_get_korzina],
     [button_get_zakaz]
    # [button_run_flowers_shop]
], resize_keyboard=True)


# ++++++++++++++++++++++++++++=================++++++++++++++++++++++
# Функции БОТА
@dp.message(Command(commands=['start']))
async def start_command(message: Message):
   await message.answer("Привет! Выберите кнопку с действием", reply_markup=keyboard)

@dp.message(Command(commands=['help']))
async def help_command(message: Message):
   await message.answer("Тут помощь. Есть такие команды: \n "
                        "/del_registr - удалить регистрацию \n ")



@dp.message(F.text == "Получить корзину")
async def get_korzina_from_site(message: Message):
    url = URL_API_GET_KORZINA
    try:
        response = requests.get(url)
        data = response.json()
        # Форматирование и отправка сообщения с данными о корзине
        response_message = "\n".join([f"Товар: {item['tovar']}, Количество: {item['quantity']}" for item in data])
        await message.answer(response_message)
    except:
        await message.answer("Не удалось получить данные.")

@dp.message(F.text == "Получить заказ")
async def get_zakaz_from_site(message: Message):
    url = URL_API_GET_ZAKAZ
    try:
        response = requests.get(url)
        data = response.json()
    except:
        await message.answer("Произошла ошибка")







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