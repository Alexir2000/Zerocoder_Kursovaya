# TG06. Разработка чат-бота
# Закрепим материалы по Telegram-ботам на примере кейса «Финансовый бот-помощник»
#функционал нашего бота. Бот будет иметь несколько возможностей:
# -регистрация пользователя в Telegram;
# -просмотр курса валют с помощью API или парсинга;
# -получение советов по экономии в виде текста;
# -ведение учёта личных финансов по трём категориям.

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

from tg_bot.config import TOKEN
import sqlite3
import aiohttp
import logging
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

url_site = "http://127.0.0.1:8000/catalog/"
url_site = "https://www.mebelhit.ru/"

button_registr = KeyboardButton(text="Регистрация в телеграм-боте")
button_exchange_rates = KeyboardButton(text="Курс валют")
button_run_flowers_shop = KeyboardButton(text="Магазин цветов", web_app=WebAppInfo(url=url_site))


keyboard = ReplyKeyboardMarkup(keyboard=[
    [button_registr, button_exchange_rates],
    [button_run_flowers_shop]
], resize_keyboard=True)


Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=True)
    category1 = Column(String, nullable=True)
    category2 = Column(String, nullable=True)
    category3 = Column(String, nullable=True)
    expenses1 = Column(Float, nullable=True)
    expenses2 = Column(Float, nullable=True)
    expenses3 = Column(Float, nullable=True)
# Движок и сессия вне функции, чтобы использовать их повторно
engine_bot = create_engine('sqlite:///user.db', echo=True)
Session_bot = sessionmaker(bind=engine_bot)


def print_db():
    # Создание сессии
    session = Session_bot()
    try:
        # Получение всех записей из таблицы users
        users = session.query(User).all()
        # Печать каждой записи
        for user in users:
            print("\n\n Печать результатов \n\n")
            print(f"ID: {user.id},\n Telegram ID: {user.telegram_id}, Name: {user.name}, "
                  f"Category1: {user.category1}, Category2: {user.category2}, Category3: {user.category3}, "
                  f"Expenses1: {user.expenses1}, Expenses2: {user.expenses2}, Expenses3: {user.expenses3}\n")
            print("\n\n завершение печати \n\n")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрытие сессии
        session.close()

def init_db_bot():
    # Создаем таблицы, если они не существуют
    Base.metadata.create_all(engine_bot)


# ++++++++++++++++++++++++++++=================++++++++++++++++++++++
# Функции БОТА
@dp.message(Command(commands=['start']))
async def start_command(message: Message):
   await message.answer("Привет! Выберите кнопку с действием", reply_markup=keyboard)

@dp.message(Command(commands=['help']))
async def help_command(message: Message):
   await message.answer("Тут помощь. Есть такие команды: \n "
                        "/del_registr - удалить регистрацию \n ")

# @dp.message(F.text == "Магазин цветов")
# async def run_flowers_shop_button(message: Message):
#     url_site = "http://127.0.0.1:8000/catalog/"
#     url_site = "https://www.mebelhit.ru/"
#     print("\n\n\n\nЗапуск магазина цветов\n\n\n\n")
#     await message.answer("Запуск магазина цветов",
#                          reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
#                              text="Открыть магазин",
#                              web_app=WebAppInfo(url=url_site)
#                          )))








@dp.message(F.text == "Регистрация в телеграм-боте")
async def registration(message: Message):
    session = Session_bot()
    try:
        telegram_id = message.from_user.id
        name = message.from_user.full_name
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            await message.answer("Вы уже зарегистрированы!")
        else:
            new_user = User(telegram_id=telegram_id, name=name)
            session.add(new_user)
            session.commit()
            await message.answer("Вы успешно зарегистрированы!")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        session.close()

@dp.message(Command(commands=['del_registr']))
async def del_registr(message: Message):
    session = Session_bot()
    try:
        telegram_id = message.from_user.id
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            session.delete(user)
            session.commit()
            await message.answer("Ваша регистрация была удалена.")
        else:
            await message.answer("Вы не зарегистрированы.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        session.close()

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