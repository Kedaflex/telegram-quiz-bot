from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from config import Config
from database.base import SessionLocal
from database.models import User, UserAnswer
from utils.helpers import generate_stats_csv
import logging

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != Config.ADMIN_CHAT_ID:
        # Игнорируем не админов
        return

    await update.message.reply_text("⏳ Собираю статистику...")

    with SessionLocal() as session:
        total_users = session.query(User).count()
        total_answers = session.query(UserAnswer).count()
        # Средняя успеваемость (упрощенно)
        correct_answers = session.query(UserAnswer).filter(UserAnswer.is_correct == True).count()
        avg_accuracy = round((correct_answers / total_answers * 100), 1) if total_answers > 0 else 0

    summary = (
        f"📊 **Краткая статистика**\n"
        f"👥 Пользователей: {total_users}\n"
        f"📝 Всего ответов: {total_answers}\n"
        f"🎯 Общая точность: {avg_accuracy}%"
    )
    
    await update.message.reply_text(summary, parse_mode='Markdown')
    
    # Генерация и отправка CSV
    try:
        csv_file = generate_stats_csv()
        # Преобразуем StringIO в bytes для отправки
        document = csv_file.getvalue().encode('utf-8-sig') # utf-8-sig для Excel
        
        await update.message.reply_document(
            document=document,
            filename="quiz_stats.csv",
            caption="Подробный отчет по всем пользователям."
        )
    except Exception as e:
        logging.error(f"Ошибка генерации CSV: {e}")
        await update.message.reply_text("Ошибка при создании файла отчета.")

stats_handler = CommandHandler("stats", admin_stats)