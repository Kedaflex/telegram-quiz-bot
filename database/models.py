from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)

    # Связь с UserAnswer. Обрати внимание: тут back_populates="user"
    # Это ссылается на поле 'user' в классе UserAnswer (ниже)
    answers = relationship("UserAnswer", back_populates="user")

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    option_1 = Column(String, nullable=False)
    option_2 = Column(String, nullable=False)
    option_3 = Column(String, nullable=False)
    option_4 = Column(String, nullable=False)
    correct_option = Column(Integer, nullable=False)

    # Связь с UserAnswer.
    answers = relationship("UserAnswer", back_populates="question")

class UserAnswer(Base):
    __tablename__ = "user_answers"

    answer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    chosen_option = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)

    # !!! ВОТ ЗДЕСЬ БЫЛА ОШИБКА !!!
    # back_populates должен указывать на поле 'answers' в классе User (вверху)
    user = relationship("User", back_populates="answers")
    
    question = relationship("Question", back_populates="answers")from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)

    # Связь с UserAnswer. Обрати внимание: тут back_populates="user"
    # Это ссылается на поле 'user' в классе UserAnswer (ниже)
    answers = relationship("UserAnswer", back_populates="user")

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    option_1 = Column(String, nullable=False)
    option_2 = Column(String, nullable=False)
    option_3 = Column(String, nullable=False)
    option_4 = Column(String, nullable=False)
    correct_option = Column(Integer, nullable=False)

    # Связь с UserAnswer.
    answers = relationship("UserAnswer", back_populates="question")

class UserAnswer(Base):
    __tablename__ = "user_answers"

    answer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    chosen_option = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)

    # !!! ВОТ ЗДЕСЬ БЫЛА ОШИБКА !!!
    # back_populates должен указывать на поле 'answers' в классе User (вверху)
    user = relationship("User", back_populates="answers")
    
    question = relationship("Question", back_populates="answers")
