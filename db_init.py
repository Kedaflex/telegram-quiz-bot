from database.base import Base, engine, SessionLocal
from database.models import Question

def init_db():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    
    # Проверяем, есть ли вопросы, если нет - добавляем
    if session.query(Question).count() == 0:
        questions = [
            Question(
                question_text="Какой тип данных используется для хранения целых чисел в Python?",
                option_1="float", option_2="int", option_3="str", option_4="bool",
                correct_option=2
            ),
            Question(
                question_text="Что выведет print(2 ** 3)?",
                option_1="6", option_2="5", option_3="8", option_4="9",
                correct_option=3
            ),
            Question(
                question_text="Ключевое слово для определения функции?",
                option_1="def", option_2="func", option_3="define", option_4="function",
                correct_option=1
            ),
            Question(
                question_text="Какая библиотека используется для Telegram ботов в этом проекте?",
                option_1="aiogram", option_2="telebot", option_3="python-telegram-bot", option_4="discord.py",
                correct_option=3
            ),
             Question(
                question_text="Как создать виртуальное окружение?",
                option_1="python -m venv venv", option_2="pip install venv", option_3="venv start", option_4="make venv",
                correct_option=1
            ),
        ]
        session.add_all(questions)
        session.commit()
        print("База данных инициализирована и вопросы добавлены.")
    else:
        print("База данных уже содержит вопросы.")
    
    session.close()

if __name__ == "__main__":
    init_db()