import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database.base import SessionLocal
from database.models import User, Question, UserAnswer
from config import Config
import logging

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Проверка регистрации
    with SessionLocal() as session:
        if not session.get(User, user_id):
            await update.message.reply_text("Сначала нужно зарегистрироваться через /start")
            return

        # Получаем все вопросы
        questions = session.query(Question).all()
        if not questions:
            await update.message.reply_text("В базе пока нет вопросов.")
            return
        
        # Сохраняем список ID вопросов в context
        context.user_data['quiz_q_ids'] = [q.question_id for q in questions]
        context.user_data['quiz_index'] = 0
        context.user_data['score'] = 0
    
    await update.message.reply_text(f"Начинаем тест! Всего вопросов: {len(context.user_data['quiz_q_ids'])}")
    await send_next_question(update, context)

async def send_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q_ids = context.user_data.get('quiz_q_ids')
    index = context.user_data.get('quiz_index')

    if index >= len(q_ids):
        # Тест завершен
        score = context.user_data.get('score')
        total = len(q_ids)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"🏁 **Тест завершен!**\nВаш результат: {score} из {total} верных ответов.",
            parse_mode='Markdown'
        )
        # Очистка данных
        context.user_data.pop('quiz_q_ids', None)
        return

    q_id = q_ids[index]
    
    with SessionLocal() as session:
        question = session.get(Question, q_id)
        
        # Формируем кнопки
        keyboard = [
            [InlineKeyboardButton(question.option_1, callback_data=f"ans_{q_id}_1")],
            [InlineKeyboardButton(question.option_2, callback_data=f"ans_{q_id}_2")],
            [InlineKeyboardButton(question.option_3, callback_data=f"ans_{q_id}_3")],
            [InlineKeyboardButton(question.option_4, callback_data=f"ans_{q_id}_4")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"❓ **Вопрос {index + 1}/{len(q_ids)}**\n\n{question.question_text}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Убираем часики загрузки

    data = query.data.split('_') # ans_{q_id}_{option}
    if len(data) != 3 or data[0] != 'ans':
        return

    q_id = int(data[1])
    chosen_option = int(data[2])
    user_id = query.from_user.id

    # Запись ответа и проверка
    with SessionLocal() as session:
        question = session.get(Question, q_id)
        is_correct = (question.correct_option == chosen_option)
        
        # Запись в БД
        answer_record = UserAnswer(
            user_id=user_id,
            question_id=q_id,
            chosen_option=chosen_option,
            is_correct=is_correct
        )
        session.add(answer_record)
        session.commit()
        
        # Текст ответа
        correct_text_attr = getattr(question, f"option_{question.correct_option}")
        
    # Визуальная обратная связь
    if is_correct:
        context.user_data['score'] += 1
        result_text = f"✅ **Верно!**\nВаш ответ правильный."
    else:
        result_text = f"❌ **Неверно.**\nПравильный ответ: {correct_text_attr}"

    # Редактируем сообщение (убираем кнопки, пишем результат)
    await query.edit_message_text(
        text=f"{query.message.text_markdown}\n\n{result_text}",
        parse_mode='Markdown'
    )

    # Пауза перед следующим вопросом
    context.user_data['quiz_index'] += 1
    await asyncio.sleep(Config.QUIZ_PAUSE_SECONDS)
    await send_next_question(update, context)

quiz_handler = CommandHandler("test", start_test)
answer_handler = CallbackQueryHandler(handle_answer, pattern="^ans_")