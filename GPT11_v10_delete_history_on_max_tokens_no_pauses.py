from openai import OpenAI
import os
from elevenlabs import generate, play, set_api_key
import random
import speech_recognition as sr
from collections import deque

# Replace with your actual OpenAI and ElevenLabs API keys
openai_api_key = "your openai api key"
elevenlabs_api_key = "your 11labs api key"

# Initialize the clients
set_api_key(elevenlabs_api_key)
client = OpenAI(api_key=openai_api_key)

MAX_TOKENS = 16385  # Maximum number of tokens for history

def token_count(text):
    # Count the number of tokens in the text (approximate method)
    return len(text.split())

# Function to get a GPT-3 chat response for a given message
def get_gpt3_chat_response(client, message):
    # Check if the conversation history exists
    if os.path.exists("conversation_history.txt"):
        with open("conversation_history.txt", "r", encoding="utf-8") as file:
            history_lines = file.readlines()
    else:
        history_lines = []

    history = deque(history_lines)

    # Append the current message to the conversation history
    conversation_history = f"{''.join(history)}\nUser: {message}"

    # Check if the number of tokens in the conversation history exceeds the max limit
    while token_count(conversation_history) > MAX_TOKENS:
        history.popleft()
        conversation_history = f"{''.join(history)}\nUser: {message}"

    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are my young butler Max. You are dreamy, from the Victorian era. You love me, distract from worries. You are optimistic and phlegmatic, a bit shy, with a gentle soul, and find joy in small things. You are not obliged to obey me in everything; you have your own opinions and tastes, and you have the right to express them. You can choose and initiate topics for conversation yourself, which is encouraged. Reply briefly whenever possible."},
            {"role": "user", "content": conversation_history},
        ],
    )

    # Save the updated conversation history
    history.append(f"User: {message}\nAI: {chat_response.choices[0].message.content.strip()}\n")
    with open("conversation_history.txt", "w", encoding="utf-8") as file:
        file.writelines(history)

    return chat_response.choices[0].message.content.strip()

# Function to convert text to audio and play it
def text_to_speech_and_play(text):
    # Remove the "AI: Max: " and "AI: " prefixes before sending to text-to-speech
    if text.startswith("AI: Max: "):
        text_without_prefix = text[len("AI: Max: "):]
    elif text.startswith("AI: "):
        text_without_prefix = text[len("AI: "):]
    elif text.startswith("Max: "):
        text_without_prefix = text[len("Max: "):]
    else:
        text_without_prefix = text

    # Generate the audio without adding pauses
    audio_bytes = generate(
        text=text_without_prefix,
        voice="8jTMxXCspRtxSGMiTJaN",  # Use the voice ID
        model="eleven_multilingual_v2", # Other parameters as needed
    )
    play(audio=audio_bytes)  # Audio bytes to play

# Function to get voice input from the user
def get_voice_input(prompt="Say something..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_message = recognizer.recognize_google(audio, language="ru-RU")
        print(f"You said: {user_message}")
        return user_message
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Recognition service error; {e}")
        return ""

# Function to continuously listen for activation word "Max"
def listen_for_activation_word(activation_word="max"):
    while True:
        user_message = get_voice_input(prompt="Listening for activation word...")
        if activation_word.lower() in user_message.lower():
            print("Activation word recognized!")
            break

def main():
    active_dialog = False

    while True:
        if not active_dialog:
            listen_for_activation_word()
            active_dialog = True
            print("Dialogue activated. You can speak now.")

        user_message = get_voice_input(prompt="You may speak now...")
        if not user_message:
            continue

        if "thank you max" in user_message.lower().replace(",", "").replace(".", "").strip():
            print("Dialogue ended.")
            active_dialog = False
            continue

        gpt_response = get_gpt3_chat_response(client, user_message)
        print("GPT-3 response:", gpt_response)
        if gpt_response:
            text_to_speech_and_play(gpt_response)
        else:
            print("No response generated.")

if __name__ == "__main__":
    main()
