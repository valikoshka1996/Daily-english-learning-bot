import random
from flask import request, jsonify
import json
import requests
import os
import json
import re
from googletrans import Translator
from datetime import datetime
import time
import threading
import os

# Ваші настройки бота
TOKEN = os.getenv('TOKEN')  # Токен з оточення
CHAT_ID = os.getenv('CHAT_ID')  # Замініть на ваш chat_id

translator = Translator()

# Шлях до файлу зі словами
WORDS_FILE_PATH = "words_alpha.txt"
API_KEY = os.getenv('API_KEY')
# Список перекладених слів
translated_words = []

# Функція для перекладу через MyMemory API
def translate_text(text, src_lang='en', dest_lang='uk', api_key=API_KEY):
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={src_lang}|{dest_lang}&key={api_key}"
    response = requests.get(url)
    result = response.json()
    return result['responseData']['translatedText']

# Функція для перевірки, чи містить перекладене слово англійські літери
def is_translation_successful(translated):
    # Перевіряємо, чи містить перекладене слово англійські літери
    if re.search(r'[a-zA-Z]', translated):
        return False
    return True

# Функція для вибору 5 випадкових слів та їх перекладу
def get_random_words():
    with open(WORDS_FILE_PATH, 'r', encoding='utf-8') as f:
        words = f.readlines()

    # Видаляємо зайві пробіли та порожні рядки
    words = [word.strip() for word in words if word.strip()]

    # Вибираємо 5 випадкових слів, які ще не перекладені
    remaining_words = list(set(words) - set(translated_words))
    
    # Якщо залишилося менше 5 слів, вибираємо стільки, скільки є
    random_words = random.sample(remaining_words, min(5, len(remaining_words)))

    translations = []
    
    # Перекладемо слова та перевіримо їх
    for word in random_words:
        translated = translate_text(word, src_lang='en', dest_lang='uk', api_key=API_KEY)

        # Виводимо результат перекладу, щоб побачити, що ми отримуємо
        print(f"Слово: '{word}', Переклад: '{translated}'")

        # Перевіряємо, чи переклад успішний
        if is_translation_successful(translated):
            translations.append((word, translated))
            translated_words.append(word)  # Додаємо перекладене слово до списку
        else:
            print(f"Слово '{word}' не перекладено успішно, вибираємо нове слово.")
            # Якщо не перекладено, вибираємо нове слово для перекладу
            if remaining_words:
                new_word = random.choice(remaining_words)
                remaining_words.remove(new_word)
                random_words.append(new_word)  # Додаємо нове слово до вибірки
            continue

    # Якщо всі слова перекладені, скидаємо список
    if len(translated_words) == len(words):
        translated_words.clear()

    return translations


# Функція для відправки повідомлення в Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

# Функція для відправки перекладених слів
def send_words():
    translations = get_random_words()

    # Формуємо повідомлення з перекладеними словами
    message = "Ось 5 нових слів для вивчення:\n\n"
    for word, translated in translations:
        message += f"{word} - {translated}\n"

    # Відправляємо повідомлення в Telegram
    send_to_telegram(message)

# Функція для запуску бота, який працюватиме раз на день
def run_daily():
    # Виконувати раз на день в 15:00
    while True:
        now = datetime.now()
        # Перевіряємо, чи зараз 15:00
        if now.hour == 15 and now.minute == 0:
            send_words()
            # Чекаємо 60 секунд, щоб не відправити більше одного повідомлення за хвилину
            time.sleep(60)
        else:
            time.sleep(30)  # Чекаємо 30 секунд, щоб перевірити знову

# Функція для обробки POST-запиту
def handle_post_request():
    data = json.loads(request.data)
    if data.get("action") == "translate":
        send_words()

# Створюємо потік для запуску бота, який буде перевіряти час і відправляти повідомлення
bot_thread = threading.Thread(target=run_daily)
bot_thread.start()

# Для того щоб працював Flask-сервер для POST-запиту
from flask import Flask, request
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    handle_post_request()
    return "OK"

@app.route('/translate', methods=['POST'])
def translate_word():
    try:
        # Отримуємо дані з тіла запиту
        data = request.get_json()
        if data.get('action') != 'translate' or 'word' not in data:
            return jsonify({"error": "Invalid request format"}), 400

        word = data['word']

        # Перевіряємо, чи є слово в файлі
        with open(WORDS_FILE_PATH, 'r', encoding='utf-8') as f:
            words = f.readlines()

        words = [w.strip() for w in words if w.strip()]
        
        # Якщо слово є в списку, перекладаємо його
        if word in words:
            translated = translate_text(word, src_lang='en', dest_lang='uk', api_key=API_KEY)

            # Перевіряємо, чи переклад успішний
            if is_translation_successful(translated):
                return jsonify({"word": word, "translation": translated})
            else:
                return jsonify({"error": "Translation failed"}), 500
        else:
            return jsonify({"error": "Word does not exist"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Запускаємо Flask-сервер
    app.run(host='0.0.0.0', port=5233)


