from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import asyncio

API_TOKEN = '7528963854:AAGLegRWedP3Wg4Q9ny07GKksOo01ebDo70'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Настройка базы данных
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER,
            task TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (contact_id) REFERENCES contacts (id)
        )
    ''')
    conn.commit()
    conn.close()


init_db()


class Form(StatesGroup):
    add_contact = State()
    add_task = State()
    delete_task = State()
    show_tasks = State()


# Команда /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой бот-ежедневник. Используй команды для управления задачами.")


# Команда для добавления контакта
@dp.message_handler(commands=['add_contact'])
async def add_contact(message: types.Message):
    await Form.add_contact.set()
    await message.answer("Введите имя контакта:")


@dp.message_handler(state=Form.add_contact)
async def process_add_contact(message: types.Message, state: FSMContext):
    name = message.text
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    await state.finish()
    await message.answer(f"Контакт {name} добавлен!")


# Команда для добавления задачи
@dp.message_handler(commands=['add_task'])
async def add_task(message: types.Message):
    await Form.add_task.set()
    await message.answer("Введите задачу:")


@dp.message_handler(state=Form.add_task)
async def process_add_task(message: types.Message, state: FSMContext):
    task_details = message.text.split(';')
    if len(task_details) != 3:
        await message.answer(
            "Пожалуйста, укажите задачу в формате: 'задача;имя_контакта;дата_и_время' (где дата и время указываются в формате YYYY-MM-DD HH:MM)")
        return

    task, contact_name, date_time = task_details
    date, time = date_time.split()  # отдельные дата и время
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM contacts WHERE name=?", (contact_name,))
    contact_id = cursor.fetchone()

    if contact_id:
        cursor.execute("INSERT INTO tasks (contact_id, task, date, time) VALUES (?, ?, ?, ?)",
                       (contact_id[0], task, date, time))
        conn.commit()
        await message.answer(f"Задача '{task}' добавлена для контакта '{contact_name}' на {date} в {time}.")
    else:
        await message.answer(f"Контакт {contact_name} не найден.")

    conn.close()
    await state.finish()


# Команда для просмотра задач
@dp.message_handler(commands=['show_tasks'])
async def show_tasks(message: types.Message):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT task, date, time FROM tasks")
    tasks = cursor.fetchall()

    if tasks:
        response = "Список задач:\n"
        for task, date, time in tasks:
            response += f"- {task} (Дата: {date}, Время: {time})\n"
    else:
        response = "Задач нет."

    await message.answer(response)
    conn.close()


# Команда для удаления задачи
@dp.message_handler(commands=['delete_task'])
async def delete_task(message: types.Message):
    await Form.delete_task.set()
    await message.answer("Введите ID задачи для удаления:")


@dp.message_handler(state=Form.delete_task)
async def process_delete_task(message: types.Message, state: FSMContext):
    task_id = message.text
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    if cursor.rowcount:
        await message.answer(f"Задача с ID {task_id} удалена.")
    else:
        await message.answer(f"Задача с ID {task_id} не найдена.")

    conn.commit()
    conn.close()
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
