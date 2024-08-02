# TG05. Работа с внешними API
# Рассмотрим другие API. Научимся работать с THE CAT API и NASA API.
# Разработайте телеграм-бота со своим функционалом с использованием 
# разных сторонних api (ссылки выше)

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
from datetime import datetime, timedelta
from googletrans import Translator

from config import TOKEN, TOKEN_NASA, TOKEN_CAT

# ищем библиотеку gTTS и скачиваем ее
from gtts import gTTS
import os

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_random_apod():
   end_date = datetime.now()
   start_date = end_date - timedelta(days=365)
   random_date = start_date + (end_date - start_date) * random.random()
   date_str = random_date.strftime("%Y-%m-%d")

   url = f'https://api.nasa.gov/planetary/apod?api_key={TOKEN_NASA}&date={date_str}'
   response = requests.get(url)
   return response.json()


def get_fact():
   try:
      response = requests.get("http://numbersapi.com/random/trivia")
      if response.status_code == 200:
         return response.text
      else:
         return "Не удалось получить факт. Попробуйте позже."
   except requests.RequestException as e:
      return f"Произошла ошибка: {e}"


def fact_to_rus(fact):
   translator = Translator()
   try:
      translated = translator.translate(fact, src='en', dest='ru')
      return translated.text
   except Exception as e:
      return f"Ошибка при переводе: {e}"

# ++++++++++++++++++++++++++++=================++++++++++++++++++++++
# Функции БОТА
@dp.message(Command("start"))
async def start_command(message: Message):
   await message.answer("Привет!  \n Фото NASA пиши команду /random_apod \n Факт пиши команду /fact")

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
   apod = get_random_apod()
   photo_url = apod['url']
   title = apod['title']

   await message.answer_photo(photo=photo_url, caption=f"{title} \n\n")


@dp.message(Command("fact"))
async def fact(message: Message):
   fact = fact_to_rus(get_fact())
   await message.answer(fact)


# ++++++++++++++++++++++++++++=================++++++++++++++++++++++


async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())