import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#API_TOKEN = 'YOUR_API_TOKEN'
API_TOKEN = '7528963854:AAGLegRWedP3Wg4Q9ny07GKksOo01ebDo70'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
schedule = {}
contacts = {}


class Form(StatesGroup):
    main_menu = State()
    waiting_for_contact_name = State()
    waiting_for_task = State()


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Список контактов", callback_data='contacts'),
                 InlineKeyboardButton("Дела на сегодня", callback_data='today_tasks'))
    return keyboard


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот-помощник.\n"
                        "Выбери пункт меню:", reply_markup=main_menu_keyboard())
    await Form.main_menu.set()


@dp.callback_query_handler(state=Form.main_menu)
async def process_main_menu(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'contacts':
        await show_contacts(callback.message)
    elif callback.data == 'today_tasks':
        await show_today_tasks(callback.message)


async def show_contacts(message):
    if contacts:
        response = "Список контактов:\n" + "\n".join(contacts.keys())
    else:
        response = "Контакты отсутствуют."

    await message.answer(response)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Добавить контакт", callback_data='add_contact'),
                 InlineKeyboardButton("На главную", callback_data='main_menu'))
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'add_contact', state=Form.main_menu)
async def add_contact(callback: types.CallbackQuery):
    await callback.message.answer("Введите имя нового контакта:")
    await Form.waiting_for_contact_name.set()


@dp.message_handler(state=Form.waiting_for_contact_name)
async def process_contact_name(message: types.Message, state: FSMContext):
    contact_name = message.text
    contacts[contact_name] = []
    await message.reply(f"Контакт '{contact_name}' добавлен!")
    await state.finish()
    await message.answer("Выберите пункт меню:", reply_markup=main_menu_keyboard())


@dp.callback_query_handler(lambda c: c.data == 'main_menu', state=Form.main_menu)
async def return_to_main_menu(callback: types.CallbackQuery):
    await callback.message.answer("Выберите пункт меню:", reply_markup=main_menu_keyboard())


async def show_today_tasks(message):
    response = "Задачи на сегодня:\n"
    if schedule:
        for contact, tasks in schedule.items():
            response += f"{contact}:\n" + "\n".join(tasks) + "\n"
    else:
        response += "Задач на сегодня нет."

    await message.answer(response)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("Добавить задачу", callback_data='add_task'),
                 InlineKeyboardButton("На главную", callback_data='main_menu'))
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'add_task', state=Form.main_menu)
async def add_task(callback: types.CallbackQuery):
    await callback.message.answer("Введите имя контакта для добавления задачи:")
    await Form.waiting_for_contact_name.set()


@dp.message_handler(state=Form.waiting_for_contact_name)
async def process_task_name(message: types.Message, state: FSMContext):
    contact_name = message.text
    if contact_name in contacts:
        await message.answer("Введите задачу для этого контакта:")
        await Form.waiting_for_task.set()
        await state.update_data(contact_name=contact_name)
    else:
        await message.reply(f"Контакт '{contact_name}' не найден. Введите имя другого контакта:")


@dp.message_handler(state=Form.waiting_for_task)
async def process_task(message: types.Message, state: FSMContext):
    task = message.text
    data = await state.get_data()
    contact_name = data.get('contact_name')

    if contact_name not in schedule:
        schedule[contact_name] = []
    schedule[contact_name].append(task)
    await message.reply(f"Задача '{task}' добавлена для контакта '{contact_name}'.")
    await state.finish()
    await message.answer("Выберите пункт меню:", reply_markup=main_menu_keyboard())


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
