import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            contact_id INTEGER,
            task TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES contacts (id)
        )
    ''')
    conn.commit()
    conn.close()

# Инициализация бота и диспетчера
#API_TOKEN = 'YOUR_API_TOKEN'
API_TOKEN = '7528963854:AAGLegRWedP3Wg4Q9ny07GKksOo01ebDo70'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создание состояний
class Form(StatesGroup):
    waiting_for_contact = State()
    waiting_for_task = State()
    waiting_for_date = State()
    waiting_for_time = State()

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать! Используйте клавиатуру для управления.")

# Клавиатура
async def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Список контактов"),
               KeyboardButton("Добавить контакт"),
               KeyboardButton("Удалить контакт"),
               KeyboardButton("Добавить задачу"),
               KeyboardButton("Просмотр задач"),
               KeyboardButton("Удалить задачу"))
    return markup

# Функция для добавления контакта
@dp.message_handler(lambda message: message.text == "Добавить контакт")
async def add_contact(message: types.Message):
    await Form.waiting_for_contact.set()
    await message.reply("Введите имя контакта:")

@dp.message_handler(state=Form.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name) VALUES (?)", (message.text,))
    conn.commit()
    conn.close()
    await state.finish()
    await message.reply("Контакт добавлен.", reply_markup=await main_menu())

# Функция для удаления контакта
@dp.message_handler(lambda message: message.text == "Удалить контакт")
async def delete_contact(message: types.Message):
    await Form.waiting_for_contact.set()
    await message.reply("Введите имя контакта для удаления:")

@dp.message_handler(state=Form.waiting_for_contact)
async def process_delete_contact(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (message.text,))
    conn.commit()
    conn.close()
    await state.finish()
    await message.reply("Контакт удалён.", reply_markup=await main_menu())

# Функция для добавления задачи
@dp.message_handler(lambda message: message.text == "Добавить задачу")
async def add_task(message: types.Message):
    await Form.waiting_for_task.set()
    await message.reply("Введите текст задачи:")

@dp.message_handler(state=Form.waiting_for_task)
async def process_task(message: types.Message, state: FSMContext):
    await state.update_data(task=message.text)
    await Form.waiting_for_date.set()
    await message.reply("Введите дату задачи (в формате ГГГГ-ММ-ДД):")

@dp.message_handler(state=Form.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await Form.waiting_for_time.set()
    await message.reply("Введите время задачи (в формате ЧЧ:ММ):")

@dp.message_handler(state=Form.waiting_for_time)
async def process_time(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    task = user_data['task']
    date = user_data['date']
    time = message.text

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, date, time) VALUES (?, ?, ?)", (task, date, time))
    conn.commit()
    conn.close()
    await state.finish()
    await message.reply("Задача добавлена.", reply_markup=await main_menu())

# Функция для просмотра задач
@dp.message_handler(lambda message: message.text == "Просмотр задач")
async def view_tasks(message: types.Message):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        response = "\n".join([f"Задача: {t[1]}, Дата: {t[2]}, Время: {t[3]}" for t in tasks])
    else:
        response = "Нет запланированных задач."

    await message.reply(response, reply_markup=await main_menu())

# Запускаем бота
if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
