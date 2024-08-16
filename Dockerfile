# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем зависимости для работы с PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY . .

# Указываем команду для запуска приложения
CMD ["python", "app.py"]
