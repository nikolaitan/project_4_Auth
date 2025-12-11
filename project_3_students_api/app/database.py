from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv  # Загрузка .env
import os

# Загрузка переменных из .env
load_dotenv()

# URL БД из переменных окружения
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Создание движка БД (подключение)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Фабрика сессий (для работы с БД)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()