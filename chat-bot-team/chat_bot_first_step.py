№Вот адаптированный код для aiogram версии 3.15:

from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.fsm import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Создаем экземпляр бота и диспетчера
bot = Bot(token='YOUR_BOT_TOKEN')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определение состояний
class Form(StatesGroup):
    state1 = State()
    state2 = State()

# Пример команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Это бот на aiogram версии 3.15.")
    # Здесь можно добавить переключение состояния, если нужно

# Пример обработки состояния
@dp.message(F.text == "Начать")
async def process_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.state1)
    await message.answer("Вы находитесь в состоянии 1.")

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать")],
    ],
    resize_keyboard=True
)

# Отправляем ответ с клавиатурой
@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=keyboard)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# Основные изменения:
# Убрана поддержка aiogram.contrib. Используйте aiogram.fsm для реализации состояний.
# Изменены демонстрационные работы с состояниями, теперь они управляются через FSMContext.
# Импортирование и использование клавиатуры также изменилось.
# Этот код должен работать с aiogram версии 3.15. Заменить YOUR_BOT_TOKEN на свой токен и доработать дальнейшую логику.

