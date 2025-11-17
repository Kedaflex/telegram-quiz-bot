import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", 0))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///quiz_bot.db")
    
    # Таймауты и задержки
    QUIZ_PAUSE_SECONDS = 3