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

from config import TOKEN
import sqlite3
import aiohttp
import logging
import requests

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


button_registr = KeyboardButton(text="Регистрация в телеграм-боте")
button_exchange_rates = KeyboardButton(text="Курс валют")
button_tips = KeyboardButton(text="Советы по экономии")
button_finances = KeyboardButton(text="Личные финансы")

keyboard = ReplyKeyboardMarkup(keyboard=[
    [button_registr, button_exchange_rates],
    [button_tips, button_finances]
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

class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()

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


@dp.message(F.text == "Советы по экономии")
async def send_tips(message: Message):
    tips = [
        "Совет 1: Ведите бюджет и следите за своими расходами.",
        "Совет 2: Откладывайте часть доходов на сбережения.",
        "Совет 3: Покупайте товары по скидкам и распродажам.",
        "Совет 4: Избегайте импульсивных покупок.",
        "Совет 5: Планируйте свои покупки заранее.",
        "Совет 6: Сравнивайте цены перед покупкой.",
        "Совет 7: Используйте общественный транспорт вместо такси.",
        "Совет 8: Готовьте еду дома вместо того, чтобы заказывать.",
        "Совет 9: Избегайте долгов и кредитов, если это возможно.",
        "Совет 10: Ищите бесплатные или недорогие развлечения.",
        "Совет 11: Регулярно проверяйте свои банковские выписки.",
        "Совет 12: Инвестируйте в свое образование и навыки."
    ]
    tip = random.choice(tips)
    await message.answer(tip)

@dp.message(F.text == "Личные финансы")
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.reply("Введите первую категорию расходов:")

@dp.message(FinancesForm.category1)
async def finances(message: Message, state: FSMContext):
   await state.update_data(category1 = message.text)
   await state.set_state(FinancesForm.expenses1)
   await message.reply("Введите расходы для категории 1:")

@dp.message(FinancesForm.expenses1)
async def finances(message: Message, state: FSMContext):
   await state.update_data(expenses1 = float(message.text))
   await state.set_state(FinancesForm.category2)
   await message.reply("Введите вторую категорию расходов:")

@dp.message(FinancesForm.category2)
async def finances(message: Message, state: FSMContext):
   await state.update_data(category2 = message.text)
   await state.set_state(FinancesForm.expenses2)
   await message.reply("Введите расходы для категории 2:")

@dp.message(FinancesForm.expenses2)
async def finances(message: Message, state: FSMContext):
   await state.update_data(expenses2 = float(message.text))
   await state.set_state(FinancesForm.category3)
   await message.reply("Введите третью категорию расходов:")

@dp.message(FinancesForm.category3)
async def finances(message: Message, state: FSMContext):
   await state.update_data(category3 = message.text)
   await state.set_state(FinancesForm.expenses3)
   await message.reply("Введите расходы для категории 3:")

@dp.message(FinancesForm.expenses3)
async def finances(message: Message, state: FSMContext):
    session = Session_bot()
    try:
        data = await state.get_data()
        telegram_id = message.from_user.id
        # Поиск пользователя по telegram_id
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            # Обновление данных пользователя
            user.category1 = data.get('category1')
            user.expenses1 = data.get('expenses1')
            user.category2 = data.get('category2')
            user.expenses2 = data.get('expenses2')
            user.category3 = data.get('category3')
            user.expenses3 = float(message.text)
            # Сохранение изменений
            session.commit()
            await message.answer("Категории и расходы сохранены!")
        else:
            await message.answer("Пользователь не найден.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
        session.rollback()
    finally:
        session.close()
    await state.clear()





# ++++++++++++++++++++++++++++=================++++++++++++++++++++++

# init_db_bot() # единовременный запуск создания базы. потом комментируем

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())

# print_db() # функция печати содержимого базы для проверки.