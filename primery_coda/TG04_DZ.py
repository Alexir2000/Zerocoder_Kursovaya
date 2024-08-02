 # TG04. Реализация меню и кнопок. Работа с интерфейсом
 #Научимся реализовывать клавиатуры и кнопки.
 
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging
import keyboards_dz as kb

from keyboards_dz import main_kb,  main_inline_kb, main_inline_kb2 # импортируем нашу клавиатуру

from config import TOKEN, API_POGODA

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)



# ++++++++++++++++++++++++++++=================++++++++++++++++++++++
# Функции для бота
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(f'нажата команда start.', reply_markup=main_kb)

@dp.message(Command(commands=['help']))
async def help(message: Message, state: FSMContext):
    await message.answer(f'Тут будет помощь \n тут будет описание команд которые выполняет бот')

@dp.message(Command(commands=['links']))
async def links(message: Message, state: FSMContext):
    await message.answer(f'выберите действие:',reply_markup=main_inline_kb)

@dp.message(F.text == "Привет")
async def privet(message: Message):
   await message.answer(f'Привет, {message.from_user.full_name}')

@dp.message(F.text == "Пока")
async def poka(message: Message):
   await message.answer(f'Пока, {message.from_user.full_name}')

@dp.message(Command(commands=['dynamic']))
async def dynam(message: Message, state: FSMContext):
    await message.answer(f' Больше? ',reply_markup=main_inline_kb2)

@dp.callback_query(F.data == 'show_more')
async def news(callback: CallbackQuery):
   await callback.answer("формируем ответ")
   await callback.message.edit_text(f' выберите опцию:',reply_markup=await kb.test_keyboard())

@dp.callback_query(F.data == 'Команда 1')
async def comm1(callback: CallbackQuery):
   await callback.answer("формируем ответ")
   await callback.message.edit_text(f'Нажата кнопка {kb.test_kb_command[0][0]}')

@dp.callback_query(F.data == 'Команда 2')
async def comm2(callback: CallbackQuery):
   await callback.answer("формируем ответ")
   await callback.message.edit_text(f'Нажата кнопка {kb.test_kb_command[1][0]}')
# ++++++++++++++++++++++++++++=================++++++++++++++++++++++


# начало работы.

if __name__ == '__main__':
    asyncio.run(main())




