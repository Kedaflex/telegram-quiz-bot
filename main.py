import logging
from telegram.ext import ApplicationBuilder
from config import Config
from handlers.registration import registration_handler
from handlers.quiz import quiz_handler, answer_handler
from handlers.admin import stats_handler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    if not Config.BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не найден в .env")
        return

    application = ApplicationBuilder().token(Config.BOT_TOKEN).build()

    # Регистрация хендлеров
    application.add_handler(registration_handler) # /start и диалог
    application.add_handler(quiz_handler)         # /test
    application.add_handler(answer_handler)       # Нажатие кнопок
    application.add_handler(stats_handler)        # /stats

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()