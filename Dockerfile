FROM python:3.11

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY . .

CMD ["db", "5432", "python", "manage.py", "runserver", "0.0.0.0:8000"]