import asyncio
import random
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import os

# Токен вашего бота
BOT_TOKEN = "8986306032:AAFES6EzJIUAZm9ZLbqmcbv4clzfkDEAB0c"

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_random_quote():
    """Функция для чтения Excel с автоматическим определением колонок"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "quotes_portfolio.xlsx")

        # Читаем файл
        df = pd.read_excel(file_path)

        if df.empty:
            return "База данных пуста. Сначала запустите парсер!"

        # Выбираем одну случайную строку
        random_row = df.sample(n=1).iloc[0]

        # Умный поиск нужных колонок (поддерживает и русский, и английский языки)
        # Ищем колонку с текстом цитаты
        text_col = next((c for c in df.columns if c.lower() in ['цитата', 'text', 'quote']), df.columns[0])
        # Ищем колонку с автором
        author_col = next((c for c in df.columns if c.lower() in ['автор', 'author']), df.columns[1])
        # Ищем колонку с тегами
        tags_col = next((c for c in df.columns if c.lower() in ['теги', 'tags']), df.columns[2])

        # Извлекаем данные по найденным именам колонок
        text = random_row[text_col]
        author = random_row[author_col]
        tags = random_row[tags_col]

        quote_text = f"💬 «{text}»\n\n✍️ Автор: {author}\n🏷 Теги: {tags}"
        return quote_text

    except FileNotFoundError:
        return f"⚠️ Ошибка! Файл не найден по пути:\n{file_path}"
    except Exception as e:
        return f"Произошла ошибка при анализе Excel-файла: {e}"


# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Создаем удобную кнопку для пользователя
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🎯 Получить случайную цитату"))

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        f"Я бот-портфолио. Я умею читать Excel-таблицу, которую собрал наш парсер, и выдавать оттуда цитаты.",
        reply_markup=builder.as_markup(resize_keyboard=True)  # Показываем кнопку
    )


# Обработчик нажатия на кнопку или любого текстового сообщения
@dp.message()
async def send_quote(message: types.Message):
    if message.text == "🎯 Получить случайную цитату":
        # Получаем текст цитаты из функции
        text_response = get_random_quote()
        await message.answer(text_response)
    else:
        # Если пользователь пишет что-то другое, принудительно возвращаем ему кнопку
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="🎯 Получить случайную цитату"))
        await message.answer("Нажмите на кнопку ниже, чтобы получить цитату 👇",
                             reply_markup=builder.as_markup(resize_keyboard=True))


# Главная функция запуска бота
async def main():
    print("=== Бот успешно запущен и готов к работе! ===")
    # Удаляем вебхуки и запускаем постоянный опрос сервера (Polling)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
