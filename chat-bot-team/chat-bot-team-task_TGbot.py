import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '7528963854:AAGLegRWedP3Wg4Q9ny07GKksOo01ebDo70'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, contact_id INTEGER, task TEXT, date TEXT, time TEXT,
                 FOREIGN KEY(contact_id) REFERENCES contacts(id))''')
    conn.commit()
    conn.close()


init_db()


# Определение состояний
class Form(StatesGroup):
    waiting_for_contact = State()
    waiting_for_task = State()
    waiting_for_date = State()
    waiting_for_time = State()


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Список контактов"))
    markup.add(KeyboardButton("Добавить контакт"), KeyboardButton("Удалить контакт"))
    markup.add(KeyboardButton("Добавить задачу"), KeyboardButton("Удалить задачу"))
    await message.answer("Привет! Я твой ежедневник. Чем могу помочь?", reply_markup=markup)


# Функция для отображения списка контактов
async def show_contacts(message: types.Message):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    await conn.close()

    if contacts:
        response = "Список контактов:\n" + '\n'.join([f"{contact[0]}: {contact[1]}" for contact in contacts])
    else:
        response = "Контакты не найдены."

    await message.answer(response)


# Функция для добавления контакта
@dp.message_handler(lambda message: message.text == "Добавить контакт")
async def add_contact(message: types.Message):
    await Form.waiting_for_contact.set()
    await message.answer("Введите имя контакта:")


@dp.message_handler(state=Form.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext):
    contact_name = message.text
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name) VALUES (?)", (contact_name,))
    conn.commit()
    await conn.close()
    await state.finish()
    await message.answer(f"Контакт '{contact_name}' добавлен!")


# Функция для удаления контакта
@dp.message_handler(lambda message: message.text == "Удалить контакт")
async def delete_contact(message: types.Message):
    await show_contacts(message)
    await Form.waiting_for_contact.set()
    await message.answer("Введите ID контакта для удаления:")


@dp.message_handler(state=Form.waiting_for_contact)
async def process_delete_contact(message: types.Message, state: FSMContext):
    contact_id = message.text
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    await conn.close()
    await state.finish()
    await message.answer(f"Контакт с ID '{contact_id}' удален!")


# Функция для добавления задачи
@dp.message_handler(lambda message: message.text == "Добавить задачу")
async def add_task(message: types.Message):
    await Form.waiting_for_task.set()
    await message.answer("Введите текст задачи:")


@dp.message_handler(state=Form.waiting_for_task)
async def process_task(message: types.Message, state: FSMContext):
    task_text = message.text
    await state.update_data(task=task_text)
    await Form.waiting_for_date.set()
    await message.answer("Введите дату задачи (в формате ГГГГ-ММ-ДД):")


@dp.message_handler(state=Form.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext):
    task_date = message.text
    await state.update_data(date=task_date)
    await Form.waiting_for_time.set()
    await message.answer("Введите время задачи (в формате ЧЧ:ММ):")


@dp.message_handler(state=Form.waiting_for_time)
async def process_time(message: types.Message, state: FSMContext):
    task_time = message.text
    user_data = await state.get_data()
    task_text = user_data['task']
    task_date = user_data['date']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, date, time) VALUES (?, ?, ?)", (task_text, task_date, task_time))
    conn.commit()
    await conn.close()
    await state.finish()
    await message.answer(f"Задача добавлена: {task_text} на {task_date} в {task_time}")


# Обработка ошибок
@dp.errors_handler()
async def error_handler(update, exception):
    print(f"Ошибка: {exception}")
    return True  # Ошибка обработана


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
