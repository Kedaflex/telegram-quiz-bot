from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True) # Telegram ID
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship("UserAnswer", back_populates="user")

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    option_1 = Column(String, nullable=False)
    option_2 = Column(String, nullable=False)
    option_3 = Column(String, nullable=False)
    option_4 = Column(String, nullable=False)
    correct_option = Column(Integer, nullable=False) # 1-4

    answers = relationship("UserAnswer", back_populates="question")

class UserAnswer(Base):
    __tablename__ = "user_answers"

    answer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    chosen_option = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="user")
    question = relationship("Question", back_populates="answers")