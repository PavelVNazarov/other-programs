from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

# Инициализируем бота и диспетчер
bot = Bot(token='YOUR_BOT_TOKEN')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Инициализация БД
def initiate_db():
    # Открытие подключения к SQLite БД
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Создание таблицы для задач
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, date TEXT, time TEXT, contact TEXT)''')
    conn.commit()
    conn.close()

# Определение состояний для машины состояний
class Form(StatesGroup):
    task_name = State()
    task_date = State()
    task_time = State()
    contact_name = State()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я твой бот-помощник. Выберите действие:", reply_markup=start_menu())

# Обработчик клавиатуры
def start_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Список контактов", callback_data='list_contacts'))
    keyboard.add(InlineKeyboardButton("Добавить контакт", callback_data='add_contact'))
    keyboard.add(InlineKeyboardButton("Удалить контакт", callback_data='delete_contact'))
    keyboard.add(InlineKeyboardButton("Добавить задачу", callback_data='add_task'))
    keyboard.add(InlineKeyboardButton("Просмотр задач", callback_data='view_tasks'))
    return keyboard

@dp.callback_query_handler(lambda c: c.data == 'add_task')
async def process_add_task(callback_query: types.CallbackQuery):
    await Form.task_name.set()
    await bot.send_message(callback_query.from_user.id, "Введите название задачи:")

@dp.message_handler(state=Form.task_name)
async def process_task_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task_name'] = message.text
    await Form.next()
    await message.reply("Введите дату задачи (YYYY-MM-DD):")

@dp.message_handler(state=Form.task_date)
async def process_task_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task_date'] = message.text
    await Form.next()
    await message.reply("Введите время задачи (HH:MM):")

@dp.message_handler(state=Form.task_time)
async def process_task_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task_time'] = message.text
        # Здесь можно добавить запись в БД
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, date, time) VALUES (?, ?, ?)", 
                       (data['task_name'], data['task_date'], data['task_time']))
        conn.commit()
        conn.close()
    await state.finish()
    await message.reply("Задача добавлена!", reply_markup=start_menu())

@dp.callback_query_handler(lambda c: c.data == 'view_tasks')
async def process_view_tasks(callback_query: types.CallbackQuery):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        tasks_message = "\n".join([f"{task[1]} (Дата: {task[2]}, Время: {task[3]})" for task in tasks])
        await bot.send_message(callback_query.from_user.id, f"Ваши задачи:\n{tasks_message}")
    else:
        await bot.send_message(callback_query.from_user.id, "Нет задач.", reply_markup=start_menu())

# Основной цикл
if __name__ == '__main__':
    initiate_db()
    executor.start_polling(dp, skip_updates=True)



# Пояснения по строкам кода:
# Импорт библиотек: Импортируются необходимые библиотеки для работы с Telegram Bot API, состояния (FSM), а также для работы с SQLite.
# Инициализация бота: Создается экземпляр Bot с переданным токеном, создается диспетчер для управления состояниями.
# initiate_db(): Функция для инициализации базы данных. Создаёт таблицу tasks, если она не существует.
# Определение состояний: Определяются состояния машины состояний с помощью StatesGroup для ввода названия задачи, даты и времени.
# Обработчик команды /start: Приветствие пользователя и вывод клавиатуры с возможными действиями.
# Функция start_menu(): Создаем inline-клавиатуру с кнопками для навигации по функциям бота.
# Обработчик добавления задачи: Устанавливает состояние для ввода названия задачи.
# Обработчик ввода названия задачи: Сохраняем название задачи и переходим к вводу даты.
# Обработчик ввода даты: Сохраняем дату и переходим к вводу времени.
# Обработчик ввода времени: Сохраняем время задачи, добавляем данные в базу и завершаем состояние.
# Обработчик просмотра задач: Извлекаем все задачи из БД и отправляем пользователю.
# Запуск бота: Инициализация базы данных и запуск бота.
    
