

# Django BankingChatbot

This project serves as the backend for a web application that utilizes speech recognition, text processing, and text-to-speech capabilities.

## Technologies Used

Django: Backend framework for building web applications.

Vosk: Speech recognition library.
JavaScript: Frontend scripting language.
SendOlama API: External API for processing text data.
Piper: Tool for text-to-speech conversion.

## Installation

### Clone the repository:

``` sh
git clone https://github.com/rahul1416/BankingChatBot.git
```
### Install dependencies:

``` sh 
pip install -r requirements.txt
```
### Run Ollama Server
``` sh
ollama run mistral

```

Bash
python manage.py migrate
Use code with caution.
## Usage

Start the development server:

Bash
python manage.py runserver
Use code with caution.
Open your web browser and navigate to http://localhost:8000.

Interact with the frontend interface to send audio data.

The backend will process the audio using Vosk for speech recognition.
Verify the received text data.

Send the verified text data to the SendOlama API.

Render the response and use Piper for text-to-speech output.

## License

[Include your desired license information here. Refer to popular licenses like MIT or Apache for guidance]