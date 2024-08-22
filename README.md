# Max: Your Dreamy Victorian Butler

Max is a virtual assistant that personifies a dreamy young butler from the Victorian era. Max is designed to provide emotional support, distracting you from anxieties and engaging in meaningful conversations with a uniquely personal touch.

## Features

- **Voice Recognition:** Listens for the activation word "Макс" and engages in conversation.
- **Chatbot Interaction:** Utilizes OpenAI's GPT-3.5 model to generate human-like responses.
- **Text-to-Speech:** Converts GPT-3's text responses to speech using ElevenLabs' text-to-speech technology.
- **Maintains Conversation History:** Keeps track of conversation history to provide contextually relevant responses.

## Prerequisites

To run this project, you'll need:

- Python 3.6+
- OpenAI API Key
- ElevenLabs API Key

## Usage

1. Replace the placeholders for OpenAI and ElevenLabs API keys in the script:

    ```python
    openai_api_key = "your openai api key"
    elevenlabs_api_key = "your 11labs api key"
    ```
## How It Works

1. **Initialization:**
   - Sets up the OpenAI and ElevenLabs clients using provided API keys.

2. **Listening for Activation:**
   - Continuously listens for the activation word "Max" (english, change it to your activation word if you want, it understands any language). Once detected, the conversation mode is activated.

3. **Voice Input:**
   - Captures user voice input and converts it to text using the Google Speech Recognition API.

4. **Generate GPT-3 Response:**
   - Sends the user's message to GPT-3 and receives a text response.

5. **Text-to-Speech:**
   - Converts GPT-3's text response to speech using ElevenLabs and plays it back to the user.

6. **Conversation Management:**
   - Continues listening for voice input and generating responses until the user says "спасибо макс" to end the conversation.

## Acknowledgments

- [OpenAI](https://www.openai.com) for providing the GPT-3.5 API.
- [ElevenLabs](https://www.eleven-labs.com) for the text-to-speech technology.
- [Google Speech Recognition](https://pypi.org/project/SpeechRecognition/) for the voice recognition.

## License

This project is licensed under the MIT License. Use in the code my git hab link if using it in your project
