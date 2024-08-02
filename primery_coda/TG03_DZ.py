# TG03. Интеграция баз данных
# Рассмотрим интеграцию баз данных, подключим SQLite и реализуем основные операции с данными.
# Создайте Телеграм-бота, который запрашивает у пользователя имя, возраст и класс (grade), в 
# котором он учится. Сделайте так чтоб бот сохранял введенные данные в таблицу students базы
# данных school_data.db.

import sqlite3

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging

from config import TOKEN, API_POGODA

# Создаем базовый класс для моделей вне функции, чтобы использовать его повторно
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
# Движок и сессия вне функции, чтобы использовать их повторно
engine_bot = create_engine('sqlite:///user_data.db', echo=True)
Session_bot = sessionmaker(bind=engine_bot)

def init_db_bot():
    # Создаем таблицы, если они не существуют
    Base.metadata.create_all(engine_bot)
    # Создаем и возвращаем сессию
    session_bot = Session_bot()
    return session_bot

# Пример использования
# session_bot = init_db_bot()

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def save_data_to_db(data):

    user = User(name=data['name'], age=data['age'], city=data['city'])
    session = Session_bot()  # Создаем новую сессию
    session.add(user)
    session.commit()
    session.close()  # Закрываем сессию

def get_pogoda(gorod):
    api_key = API_POGODA
    lang = "ru"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={gorod}&appid={api_key}&units=metric&lang={lang}"
    resp = requests.get(url)
    pogoda = resp.json()
    return round(pogoda["main"]["temp"])

async def main():
    await dp.start_polling(bot)



# ++++++++++++++++++++++++++++=================++++++++++++++++++++++
# Функции для бота
@dp.message(Command(commands=['pogoda']))
async def pogoda(message: Message):
    gorod = 'Москва'
    data = get_pogoda(gorod)
    Pogoda = 'Сейчас погода в Москве '+str(data)+' гр.'
    await message.answer(Pogoda) #.from_user.full_name()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(f'Привет, Как тебя зовут ? ')    # {message.from_user.full_name}!
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f'Сколько тебе лет ? ')
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(f'В каком городе живёшь ? ')
    await state.set_state(Form.city)

@dp.message(Form.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    save_data_to_db(data)
    name = data.get('name')
    age = data.get('age')
    city = data.get('city')
    await message.answer(f'Пользователь: {name}, {age}, {city}')
    async with aiohttp.ClientSession() as session:
        api_key = API_POGODA
        lang = "ru"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang={lang}"
        async with session.get(url) as resp:
            if resp.status == 200:
                pogoda_data = await resp.json()
                # pogoda = round(pogoda["main"]["temp"])
                main = pogoda_data["main"]
                temp_city = main["temp"]
                vlazhnost = main["humidity"]
                pogoda = pogoda_data["weather"][0]
                description = pogoda_data["weather"][0]["description"]
                pogoda_str = (f'Сейчас погода в городе '+city+':\n '
                              f'Температура: {temp_city} гр. \n '
                              f'Влажность: {vlazhnost} % \n '
                              f'Описание: {description} \n')
                await message.answer(pogoda_str)
            else:
                await message.answer(f'Погода в городе {city} не найдена')
    await state.clear()

# ++++++++++++++++++++++++++++=================++++++++++++++++++++++


# начало работы.

# Инициализируем базу
# session_bot = init_db_bot() только один раз инициализируем или когда меняем структуру базы

# Инициализируем базу напрямую через sqLite3
# conn = sqlite3.connect('user_data.db')
# cur = conn.cursor()
# пока не используем

if __name__ == '__main__':
    asyncio.run(main())




