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

##How to run vie Docker and Docker Compose:

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
