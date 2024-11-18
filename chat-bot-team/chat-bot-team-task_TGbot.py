import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram import Dispatcher, Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

API_TOKEN = 'YOUR_API_TOKEN_HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

schedule = {}

class Form:
    name = 'name'
    colleague_name = 'colleague_name'
    task = 'task'

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer("Как тебя зовут?")
    await Form.name.set()

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Вывести все задачи', callback_data='list_tasks'))
    keyboard.add(types.InlineKeyboardButton(text='Вывести задачи по коллеге', callback_data='list_colleague_tasks'))
    keyboard.add(types.InlineKeyboardButton(text='Добавить новую задачу', callback_data='add_task'))
    keyboard.add(types.InlineKeyboardButton(text='Добавить нового коллегу', callback_data='add_colleague'))
    keyboard.add(types.InlineKeyboardButton(text='Завершить работу', callback_data='finish'))

    await message.answer(f"Привет, {name}! Я твой бот-помощник.", reply_markup=keyboard)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'list_tasks')
async def list_tasks(callback_query: types.CallbackQuery):
    tasks = "\n".join([f"{name}: {tasks}" for name, tasks in schedule.items()])
    await bot.send_message(callback_query.from_user.id, f"Список дел на сегодня:\n{tasks or 'Нет задач'}")

@dp.callback_query_handler(lambda c: c.data == 'list_colleague_tasks')
async def list_colleague_tasks(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите имя коллеги:")
    await Form.colleague_name.set()

@dp.message_handler(state=Form.colleague_name)
async def process_colleague_name(message: types.Message, state: FSMContext):
    colleague_name = message.text
    tasks = schedule.get(colleague_name)
    await message.answer(f"Список дел по коллеге {colleague_name}:\n{tasks or 'Нет задач'}")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'add_task')
async def add_task(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите имя коллеги:")
    await Form.colleague_name.set()

@dp.message_handler(state=Form.colleague_name)
async def process_add_task_colleague_name(message: types.Message, state: FSMContext):
    colleague_name = message.text
    data = await state.get_data()
    name = data.get('name')

    await state.update_data(colleague_name=colleague_name)
    await bot.send_message(message.from_user.id, "Введите задачу:")
    await Form.task.set()

@dp.message_handler(state=Form.task)
async def process_task(message: types.Message, state: FSMContext):
    task = message.text
    data = await state.get_data()
    colleague_name = data.get('colleague_name')

    if colleague_name not in schedule:
        schedule[colleague_name] = []
    
    schedule[colleague_name].append(task)

    await message.answer(f"Задача добавлена для {colleague_name}.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'add_colleague')
async def add_colleague(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите имя нового коллеги:")
    await Form.colleague_name.set()

@dp.message_handler(state=Form.colleague_name)
async def process_add_colleague(message: types.Message, state: FSMContext):
    colleague_name = message.text
    schedule[colleague_name] = []  # Добавление нового коллеги с пустым списком задач

    await message.answer(f"Коллега {colleague_name} добавлен.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'finish')
async def finish(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Завершение работы.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
