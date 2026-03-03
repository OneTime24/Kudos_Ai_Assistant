# ==============================
# Kudos - Voice Controlled AI Assistant
# ==============================
# This script implements a voice-activated AI assistant using:
# - Google Gemini API for AI responses
# - SpeechRecognition for voice input
# - pyttsx3 for text-to-speech output
# - pygame for playing custom audio responses
# - Web browser integration for search and YouTube playback
# ==============================

import os
import google.generativeai as genai
from colorama import Fore, Style
import pyttsx3
import speech_recognition as sr
import webbrowser
from youtubesearchpython import VideosSearch
import pygame


# ------------------------------
# Initialize audio mixer (used for playing MP3 responses)
# ------------------------------
pygame.mixer.init()


# ------------------------------
# Configure Gemini API
# ------------------------------
# NOTE: In production, API keys should be stored securely
# using environment variables instead of hardcoding.
genai.configure(api_key="AIzaSyC8DdamcmYru2GqJ3YhpGIgrl3Zi0BbPiE")


# ------------------------------
# AI Model Configuration
# ------------------------------
generation_config = {
    "temperature": 1,              # Controls randomness of responses
    "top_p": 0.95,                 # Nucleus sampling
    "top_k": 64,                   # Limits token selection pool
    "max_output_tokens": 8192,     # Maximum length of response
    "response_mime_type": "text/plain",
}


# Initialize Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a persistent chat session
chat_session = model.start_chat(history=[])


# ------------------------------
# User Interface Messages
# ------------------------------
print(Fore.CYAN + "Welcome to Kudos: your AI Assistant!")
print(Fore.YELLOW + "Say 'Kudos' to activate me and 'exit' to end the conversation." + Style.RESET_ALL)


# ------------------------------
# Text-To-Speech (TTS) Setup
# ------------------------------
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Select voice (index may vary by system)
engine.setProperty('rate', 170)            # Speech speed
engine.setProperty('volume', 1.0)          # Volume level (0.0 to 1.0)

speaking = False  # Tracks whether the assistant is currently speaking


# ------------------------------
# Speak Function
# Converts text response to speech
# ------------------------------
def speak(text):
    global speaking
    speaking = True
    engine.say(text)
    engine.runAndWait()
    speaking = False


# ------------------------------
# Speech Recognition Setup
# ------------------------------
recognizer = sr.Recognizer()


# ------------------------------
# Audio Playback Function
# Plays predefined MP3 responses
# ------------------------------
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


# ------------------------------
# Predefined Audio Responses
# Maps specific questions to local MP3 files
# ------------------------------
audio_responses = {
    # English responses
    "how are you": "D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\thank_you_for_asking.mp3",
    "what is your name": "D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\I'm_kudos.mp3",
    "how is the weather": "D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\how_is_the_weather.mp3",

    # Urdu responses
    "who created you":"D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\made_by.mp3",
    "aapka kya naam hai":"D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\mera_naam.mp3",
    "pakistan ka matlab kya":"D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\la_illah.mp3",
    "gilgit baltistan ke bare mein bataen":"D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\gb.mp3",
    "uswa ke bare mein bataen":"D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\uswa_barey.mp3",
    "pakistan ke bare mein bataen":"D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\pakistan.mp3"
}


# ------------------------------
# Checks if question matches predefined responses
# ------------------------------
def handle_specific_questions(question):
    question_lower = question.lower()
    if question_lower in audio_responses:
        play_audio(audio_responses[question_lower])
        print(Fore.GREEN + f"Playing response for '{question_lower}'" + Style.RESET_ALL)
        return True
    return False


# ------------------------------
# Opens a website in browser
# ------------------------------
def open_website(site_name):
    if not site_name.startswith("http://") and not site_name.startswith("https://"):
        site_name = site_name.replace(" ", "")
        site_name = "https://" + site_name + ".com"
    webbrowser.open(site_name)
    return True


# ------------------------------
# Performs a Google search
# ------------------------------
def search_google(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    print(Fore.GREEN + f"Searching Google for {query}" + Style.RESET_ALL)
    speak(f"Searching Google for {query}")
    return True


# ------------------------------
# Plays YouTube video based on search query
# ------------------------------
def play_youtube_video(query):
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()["result"][0]
    video_url = result["link"]

    print(Fore.GREEN + f"Playing {query} on YouTube" + Style.RESET_ALL)
    speak(f"Playing {query} on YouTube")
    webbrowser.open(video_url)
    return True


# ------------------------------
# Handles feature-based commands (open, play, search)
# ------------------------------
def respond_with_features(voice_data):
    voice_data_lower = voice_data.lower()

    if handle_specific_questions(voice_data_lower):
        return True

    if "open" in voice_data_lower:
        site_name = voice_data_lower.split("open")[-1].strip()
        if open_website(site_name):
            speak(f"Opening {site_name}")
            return True

    elif "play" in voice_data_lower:
        search_query = voice_data_lower.split("play")[-1].strip()
        return play_youtube_video(search_query)

    elif "search" in voice_data_lower:
        search_query = voice_data_lower.split("search")[-1].strip()
        return search_google(search_query)

    return False


# ------------------------------
# Waits for activation keyword "Kudos"
# ------------------------------
def listen_for_kudos():
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(Fore.YELLOW + "Waiting for 'Kudos'..." + Style.RESET_ALL)
            audio = recognizer.listen(source)

            try:
                keyword = recognizer.recognize_google(audio)
                if "kudos" in keyword.lower():
                    print(Fore.GREEN + "'Kudos' detected!" + Style.RESET_ALL)
                    speak("Yes, how can I assist you?")
                    handle_conversation()

            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(Fore.RED + f"Speech Recognition error: {e}" + Style.RESET_ALL)


# ------------------------------
# Main conversation loop
# ------------------------------
def handle_conversation():
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(Fore.YELLOW + "Listening for your query..." + Style.RESET_ALL)
            audio = recognizer.listen(source)

            try:
                question = recognizer.recognize_google(audio)
                print(Fore.GREEN + "You: " + question + Style.RESET_ALL)

                if question.lower() == "exit":
                    speak("Goodbye!")
                    break

                if "stop speaking" in question.lower() and speaking:
                    engine.stop()
                    return

                # Feature handling first
                if not respond_with_features(question):

                    # AI-generated response
                    response = chat_session.send_message(question)
                    response_text = response.text.replace('*', '').replace('#', '')

                    # Short vs Detailed response handling
                    if any(keyword in question.lower() for keyword in ["detailed", "long", "detail", "explain in detail"]):
                        sentences = response_text.split(". ")
                        detailed_response = ". ".join(sentences[:6]) + "."
                        speak(detailed_response)
                    else:
                        short_response = response_text.split(". ")[0] + "."
                        speak(short_response)

            except sr.UnknownValueError:
                print(Fore.RED + "Could not understand audio." + Style.RESET_ALL)
            except sr.RequestError as e:
                print(Fore.RED + f"Speech Recognition error: {e}" + Style.RESET_ALL)


# ------------------------------
# Program Entry Point
# ------------------------------
# Continuously listens for activation keyword
while True:
    listen_for_kudos()