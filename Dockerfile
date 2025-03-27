# Використовуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо requirements.txt файл (якщо він є) або безпосередньо залежності
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо файли проекту до робочої директорії
COPY translate_0.1.py .
COPY words_alpha.txt .

# Відкриваємо порт 5000 для Flask сервера
EXPOSE 5233

# Встановлюємо команду для запуску вашого бота
CMD ["python", "translate_0.1.py"]
