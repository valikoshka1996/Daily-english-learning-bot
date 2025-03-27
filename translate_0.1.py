import nltk
from nltk.corpus import words
import random
import requests
import json
import re
from googletrans import Translator
from datetime import datetime
import time
import threading
from flask import Flask, request, jsonify
import os

TOKEN = os.getenv('TOKEN')  # Токен з оточення
CHAT_ID = os.getenv('CHAT_ID')  # Замініть на ваш chat_id
API_KEY = os.getenv('API_KEY')

translator = Translator()

nltk.download("words")
word_list = set(words.words())
translated_words = set()

def translate_text(text, src_lang='en', dest_lang='uk', api_key=API_KEY):
    url = f"https://api.mymemory.translated.net/get?q={text}&langpair={src_lang}|{dest_lang}&key={api_key}"
    response = requests.get(url)
    result = response.json()
    return result['responseData']['translatedText']

def is_translation_successful(translated):
    return not re.search(r'[a-zA-Z]', translated)

def get_random_words():
    selected_words = []
    translations = []
    
    while len(translations) < 5:
        remaining_words = list(word_list - translated_words)
        if not remaining_words:
            translated_words.clear()
            remaining_words = list(word_list)
        
        random.shuffle(remaining_words)
        
        for word in remaining_words:
            translated = translate_text(word)
            print(f"Слово: '{word}', Переклад: '{translated}'")
            if is_translation_successful(translated):
                selected_words.append(word)
                translations.append((word, translated))
                translated_words.add(word)
            if len(translations) == 5:
                break
    
    return translations

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

def send_words():
    translations = get_random_words()
    if len(translations) == 5:
        message = "Ось 5 нових слів для вивчення:\n\n" + "\n".join([f"{w} - {t}" for w, t in translations])
        send_to_telegram(message)

def run_daily():
    while True:
        now = datetime.now()
        if now.hour == 15 and now.minute == 0:
            send_words()
            time.sleep(60)
        else:
            time.sleep(30)

def handle_post_request():
    data = json.loads(request.data)
    if data.get("action") == "translate":
        send_words()

bot_thread = threading.Thread(target=run_daily)
bot_thread.start()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    handle_post_request()
    return "OK"

@app.route('/translate', methods=['POST'])
def translate_word():
    try:
        data = request.get_json()
        word = data.get('word')
        if not word or word not in word_list:
            return jsonify({"error": "Invalid word"}), 400
        
        translated = translate_text(word)
        print(f"Слово: '{word}', Переклад: '{translated}'")
        if is_translation_successful(translated):
            return jsonify({"word": word, "translation": translated})
        return jsonify({"error": "Translation failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/getwords', methods=['GET'])
def get_words():
    return jsonify(list(word_list)), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5233)



