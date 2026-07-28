import asyncio
import random
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Вставьте сюда токен, который выдал @BotFather
BOT_TOKEN = "ВВЕДИТЕ ВАШ ТОКЕН"

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_random_quote():
    """Функция для чтения Excel и выбора случайной цитаты"""
    try:
        # Читаем наш Excel-файл, созданный парсером
        df = pd.read_excel("all_quotes_portfolio.xlsx")
        
        # Если файл пустой, возвращаем заглушку
        if df.empty:
            return "База данных пуста. Сначала запустите парсер!"
            
        # Выбираем случайную строку из таблицы
        random_row = df.sample().iloc[0]
        
        # Собираем красивый текст сообщения
        quote_text = f"💬 «{random_row['Цитата']}»\n\n✍️ Автор: {random_row['Автор']}\n🏷 Теги: {random_row['Теги']}"
        return quote_text
    except FileNotFoundError:
        return "⚠️ Ошибка: Файл 'all_quotes_portfolio.xlsx' не найден! Запустите scraper.py, чтобы создать его."
    except Exception as e:
        return f"Произошла ошибка при чтении данных: {e}"

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Создаем удобную кнопку для пользователя
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🎯 Получить случайную цитату"))
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        f"Я бот-портфолио. Я умею читать Excel-таблицу, которую собрал наш парсер, и выдавать оттуда цитаты.",
        reply_markup=builder.as_markup(resize_keyboard=True) # Показываем кнопку
    )

# Обработчик нажатия на кнопку или любого текстового сообщения
@dp.message()
async def send_quote(message: types.Message):
    if message.text == "🎯 Получить случайную цитату":
        # Получаем текст цитаты из функции
        text_response = get_random_quote()
        await message.answer(text_response)
    else:
        await message.answer("Нажмите на кнопку ниже, чтобы получить цитату 👇")

# Главная функция запуска бота
async def main():
    print("=== Бот успешно запущен и готов к работе! ===")
    # Удаляем вебхуки и запускаем постоянный опрос сервера (Polling)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запуск асинхронного движка aiogram
    asyncio.run(main())
