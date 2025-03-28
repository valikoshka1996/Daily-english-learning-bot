README.md:


# Word Filtering and Translation Tool

This project is a Python-based tool for filtering words from a predefined list and performing translation operations.

## Features
- **Word Filtering**: Uses a dictionary file (`words_alpha.txt`) to filter valid words.
- **Translation Processing**: Implements translation logic to manipulate or process text.
- **Efficient Searching**: Optimized search for words within the list.

## Requirements
- Python 3.x

## Installation
1. Clone the repository:
   ```sh
   git https://github.com/valikoshka1996/Daily-english-learning-bot
   cd your-repo
   ```
2. Ensure you have the required dependencies (if any).

## Usage
1. Run the script:
   ```sh
   python translate_0.1.py
   ```
2. Modify `words_alpha.txt` to include custom word lists.

## Files
- `translate_0.1.py` - Main script for filtering and processing words.
- `words_alpha.txt` - A dictionary containing a large list of words.

## License
This project is licensed under the MIT License.


Would you like me to include specific examples of how the script works?

## How to run via Docker and Docker Compose:

### Installation and Running the Container

### 1. Requirements
Before installation, make sure you have:
- Docker
- Docker Compose

### 2. Clone the Repository
```sh
git clone https://github.com/valikoshka1996/Daily-english-learning-bot
cd telegram-translate-bot
```

### 3. Create the `.env` File

Create a `.env` file in the root directory of the project and add the following variables:
```sh
TOKEN=TELEGRAM_TOKEN      # Your bot token
CHAT_ID=ID_CHAT           # Chat ID for interaction
API_KEY=mymemory_api_token # API key for MyMemory API (optional)
```

### 4. Build the Docker Image
```sh
docker build -t english-tg-01 .
```

### 5. Start the Container Using Docker Compose
```sh
docker-compose up -d
```

This command will start the container in the background.

### 6. Check Container Logs
To view the container logs, run the following command:
```sh
docker logs -f $(docker ps -q --filter ancestor=english-tg-01)
```

### 7. Stop the Container
```sh
docker-compose down
```

## Project Files

- `.env` – contains environment variables (bot token, chat ID, API key)
- `Dockerfile` – instructions for building the Docker image
- `docker-compose.yml` – configuration for running the container
- `requirements.txt` – list of Python dependencies

## License
This project is open-source and distributed under the MIT license.


# API Endpoints Documentation

This Flask-based application provides multiple endpoints for interacting with word translations and sending messages via Telegram. It uses `nltk` for word selection, Google Translate API for translations, and Telegram API for sending messages.

## Endpoints

### 1. `/webhook` [POST]
This endpoint is used to trigger the sending of a set of random translated words to Telegram.

#### Request:
- Body: JSON payload (ignored by this endpoint).

#### Response:
- Status: `200 OK`.

#### Description:
This endpoint is a webhook that is triggered by a POST request. It invokes the `send_words()` function to get 5 translated words and sends them to a specified Telegram chat.

### 2. `/translate` [POST]
This endpoint allows translation of a given word from English to Ukrainian.

#### Request:
- Body: JSON object with the following structure:
  ```json
  {
    "word": "example"
  }
  ```
- `word`: A string representing the word you want to translate. It must be an English word present in the word list.

#### Response:
- Success (`200 OK`):
  ```json
  {
    "word": "example",
    "translation": "приклад"
  }
  ```
- Error (`400 Bad Request`):
  If the word is not valid or not in the word list:
  ```json
  {
    "error": "Invalid word"
  }
  ```
- Error (`500 Internal Server Error`):
  If the translation failed:
  ```json
  {
    "error": "Translation failed"
  }
  ```

#### Description:
This endpoint accepts a POST request with a word to translate. It checks if the word is valid and available in the word list. Then it sends the word for translation and returns the translated word in the response.

### 3. `/getwords` [GET]
This endpoint retrieves a list of all available English words in the word list.

#### Request:
- No body required.

#### Response:
- Success (`200 OK`):
  ```json
  ["word1", "word2", "word3", ...]
  ```

#### Description:
This endpoint returns a list of all the words available in the `nltk` word list that can be used for translation.

### 4. `/translated` [GET]
This endpoint retrieves a list of all the words that have been successfully translated.

#### Request:
- No body required.

#### Response:
- Success (`200 OK`):
  ```json
  ["word1", "word2", "word3", ...]
  ```

#### Description:
This endpoint returns a list of all the words that have been translated successfully. These words are stored in `translated_words`.

---

## Background Services

### Daily Word Sending
A background service runs every day at 15:00 to automatically send 5 random translated words to the Telegram chat. It operates by checking the current time and calling the `send_words()` function if the time is exactly 15:00.

### Telegram Notifications
When new words are translated, they are sent to a specified Telegram chat via the Telegram Bot API. You need to set the `TOKEN` and `CHAT_ID` environment variables to use the Telegram functionality.

---

## Environment Variables
Ensure the following environment variables are set for the application to function:

- `TOKEN`: The Telegram bot API token.
- `CHAT_ID`: The ID of the Telegram chat to send the messages to.
- `API_KEY`: The API key for MyMemory Translation API.

---

## Running the Application
To run this application, make sure you have installed the required dependencies (`flask`, `nltk`, `googletrans`, `requests`).

Run the Flask application:
```bash
python app.py
```

The application will start on `0.0.0.0:5233`, and you can interact with the endpoints using HTTP requests.

---
```

This README.md provides detailed information on how to interact with the API endpoints, the background services, and required configurations.