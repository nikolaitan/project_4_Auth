# Базовый образ: Python 3.10 (легковесный)
FROM python:3.10-slim

# Установка рабочей директории
WORKDIR /app

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # Установка без кэша

# Копирование всех файлов проекта
COPY . .

# Команда запуска: Uvicorn для FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]