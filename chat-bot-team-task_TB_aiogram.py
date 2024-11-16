import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import State, Dispatcher
from aiogram.utils import executor

API_TOKEN = 'YOUR_API_TOKEN'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Словарь для хранения задач
schedule = {}

# Состояния
class Form(StatesGroup):
    waiting_for_name = State()
    waiting_for_command = State()
    waiting_for_colleague_name = State()
    waiting_for_task = State()

# Команда /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Как тебя зовут?")
    await Form.waiting_for_name.set()

# Обработка имени пользователя
@dp.message_handler(state=Form.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.reply(f"Привет, {name}!\nЯ твой бот-помощник.\n"
                         "Я буду хранить данные о твоих задачах на день.\n"
                         "Для управления мной, используй команды:\n"
                         "1. Вывести все задачи\n"
                         "2. Вывести задачи по одному из коллег\n"
                         "3. Добавить новую задачу\n"
                         "4. Добавить нового коллегу\n"
                         "5. Завершить работу бота")
    await Form.waiting_for_command.set()

# Обработка команд
@dp.message_handler(state=Form.waiting_for_command)
async def process_command(message: types.Message, state: FSMContext):
    command = message.text
    data = await state.get_data()
    name = data.get('name')

    if command == '1':
        response = "Список дел на сегодня:\n"
        for colleague, tasks in schedule.items():
            response += f"{colleague}:\n{tasks}\n"
        await message.reply(response)

    elif command == '2':
        await message.reply("Введите имя коллеги:")
        await Form.waiting_for_colleague_name.set()

    elif command == '3':
        await message.reply("Введите имя коллеги:")
        await Form.waiting_for_colleague_name.set()

    elif command == '4':
        await message.reply("Введите имя нового коллеги:")
        await Form.waiting_for_colleague_name.set()

    elif command == '5':
        await message.reply("Завершение работы")
        await state.finish()
        await bot.close()

# Обработка имени коллеги
@dp.message_handler(state=Form.waiting_for_colleague_name)
async def process_colleague_name(message: types.Message, state: FSMContext):
    colleague_name = message.text
    data = await state.get_data()

    if 'task_mode' not in data or data['task_mode'] == 'add_task':
        await state.update_data(colleague_name=colleague_name)
        await message.reply("Введите задачу:")
        await Form.waiting_for_task.set()
    else:
        # Вывести задачи по коллеге
        if colleague_name in schedule:
            response = f'Список дел по коллеге {colleague_name}:\n'
            response += '\n'.join(schedule[colleague_name])
            await message.reply(response)
        else:
            await message.reply(f"Нет такого коллеги: {colleague_name}")

        await Form.waiting_for_command.set()

# Обработка задачи
@dp.message_handler(state=Form.waiting_for_task)
async def process_task(message: types.Message, state: FSMContext):
    task = message.text
    data = await state.get_data()
    colleague_name = data.get('colleague_name')

    if colleague_name not in schedule:
        schedule[colleague_name] = []
    
    schedule[colleague_name].append(task)

    await message.reply("Задача добавлена!")
    await process_command(message, state)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
