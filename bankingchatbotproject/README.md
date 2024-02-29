
# Django BankingChatbot

This project serves as the backend for a web application that utilizes speech recognition, text processing, and text-to-speech capabilities to provide aid to the customers by leveraging the power of speech.

## Technologies Used

- Django: Backend framework for building web applications.
- Vosk: Speech recognition library.
- JavaScript: Frontend scripting language.
- SendOlama API: External API for processing text data.
- Piper: Tool for text-to-speech conversion.

## Installation

**Step 1:** Clone the repository into your local machine
```bash
git clone https://github.com/rahul1416/BankingChatBot.git
cd BankingChatBot
```

**Step 2:** Create a virtual environment
```bash
python3 -m venv <env_name>
source <env_name>/Scripts/activate
```


**Step 3:** Install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```

**Step 4:** Apply the migrations
```bash
python3 manage.py migrate
```

## Setting up Ollama

**Step 1:** Download Ollama 
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Step 2:** Setup the ollama server

```bash
ollama serve
ollama run mistral
```

**Step 3:** Navigate into the static folder in the repository
```bash
ollama create rahul -f ./Modelfile
```

Your ollama server is up on `localhost:11434` and ready to work upon.

## Setting up Piper

Clone piper repository from [repository](https://github.com/rhasspy/piper)

For more details, you may refer to the [YouTube video](https://www.youtube.com/watch?v=pLR5AsbCMHs)

## Usage

```bash
python3 manage.py runserver
```

The server will start at `localhost:8000`