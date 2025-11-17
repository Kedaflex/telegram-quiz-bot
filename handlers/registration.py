from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from database.base import SessionLocal
from database.models import User
import logging

# Состояния
WAITING_FIO, WAITING_CLASS = range(2)

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Проверка: зарегистрирован ли уже пользователь
    with SessionLocal() as session:
        existing_user = session.get(User, user.id)
        if existing_user:
            await update.message.reply_text(
                f"Рад видеть снова, {existing_user.full_name}! 👋\n"
                "Вы уже зарегистрированы. Нажмите /test чтобы начать викторину."
            )
            return ConversationHandler.END

    await update.message.reply_text(
        "Привет! Я бот для проведения тестирования. 📝\n"
        "Для начала давай познакомимся. Напиши, пожалуйста, свои **Фамилию Имя Отчество**.",
        parse_mode='Markdown'
    )
    return WAITING_FIO

async def process_fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fio = update.message.text.strip()
    
    # Простая валидация
    if len(fio.split()) < 2 or any(char.isdigit() for char in fio):
        await update.message.reply_text("Пожалуйста, введите корректное ФИО (минимум 2 слова, без цифр).")
        return WAITING_FIO

    context.user_data['reg_fio'] = fio
    await update.message.reply_text("Отлично! Теперь укажи свой **класс** или **группу** (например, 11А).")
    return WAITING_CLASS

async def process_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    class_name = update.message.text.strip()
    fio = context.user_data.get('reg_fio')
    user = update.effective_user

    # Сохранение в БД
    try:
        with SessionLocal() as session:
            new_user = User(
                user_id=user.id,
                username=user.username,
                full_name=fio,
                class_name=class_name
            )
            session.add(new_user)
            session.commit()
            logging.info(f"Новый пользователь: {fio} ({user.id})")
            
        await update.message.reply_text(
            "Регистрация успешно завершена! ✅\n"
            "Теперь ты можешь пройти тест, набрав команду /test."
        )
    except Exception as e:
        logging.error(f"Ошибка БД: {e}")
        await update.message.reply_text("Произошла ошибка при регистрации. Попробуйте /start еще раз.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Экспорт хендлера
registration_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_registration)],
    states={
        WAITING_FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_fio)],
        WAITING_CLASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_class)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)