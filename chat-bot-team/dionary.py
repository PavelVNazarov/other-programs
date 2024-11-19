import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#API_TOKEN = 'YOUR_API_TOKEN_HERE'
API_TOKEN = '7528963854:AAGLegRWedP3Wg4Q9ny07GKksOo01ebDo70'

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task TEXT,
            due_date TEXT,
            due_time TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    adding_task = State()
    deleting_task = State()

# Начальное приветствие
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")
    await show_main_menu(message.chat.id)

async def show_main_menu(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Список задач", callback_data='show_tasks'))
    keyboard.add(InlineKeyboardButton("Добавить задачу", callback_data='add_task'))
    keyboard.add(InlineKeyboardButton("Удалить задачу", callback_data='delete_task'))
    keyboard.add(InlineKeyboardButton("Просмотр задач по дате", callback_data='view_by_date'))
    await bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)

# Обработка выборов в меню
@dp.callback_query_handler(lambda c: c.data in ['show_tasks', 'add_task', 'delete_task', 'view_by_date'])
async def process_menu_selection(callback_query: types.CallbackQuery):
    if callback_query.data == 'show_tasks':
        await show_tasks(callback_query.from_user.id)
    elif callback_query.data == 'add_task':
        await Form.adding_task.set()
        await bot.send_message(callback_query.from_user.id, "Введите текст задачи:")
    elif callback_query.data == 'delete_task':
        await Form.deleting_task.set()
        await bot.send_message(callback_query.from_user.id, "Введите ID задачи для удаления:")
    elif callback_query.data == 'view_by_date':
        await bot.send_message(callback_query.from_user.id, "Введите дату в формате ГГГГ-ММ-ДД:")

@dp.message_handler(state=Form.adding_task)
async def add_task(message: types.Message, state: FSMContext):
    task_text = message.text
    await state.finish()  # Сбрасываем состояние

    # Здесь Вы можете добавить логику для добавления задачи в базу данных
    await message.answer(f"Задача '{task_text}' добавлена.")

    # Возвращаемся в главное меню
    await show_main_menu(message.chat.id)

@dp.message_handler(state=Form.deleting_task)
async def delete_task(message: types.Message, state: FSMContext):
    task_id = message.text
    await state.finish()  # Сбрасываем состояние

    # Логика удаления задачи из базы данных по task_id
    await message.answer(f"Задача с ID {task_id} удалена.")

    # Возвращаемся в главное меню
    await show_main_menu(message.chat.id)

async def show_tasks(user_id):
    # Здесь Вы можете добавить логику для извлечения задач из базы данных
    await bot.send_message(user_id, "Здесь будут Ваши задачи.")

# Обработка ошибок
@dp.message_handler()
async def handle_errors(message: types.Message):
    await message.answer("Пожалуйста, введите правильную команду.")

if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
