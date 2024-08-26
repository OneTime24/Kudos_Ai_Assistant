import os
import google.generativeai as genai
from colorama import Fore, Style
import pyttsx3
import speech_recognition as sr
import webbrowser
from youtubesearchpython import VideosSearch
import pygame

# Initialize pygame
pygame.mixer.init()

# Gemini API key
genai.configure(api_key="AIzaSyC8DdamcmYru2GqJ3YhpGIgrl3Zi0BbPiE")

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

print(Fore.CYAN + "Welcome to Kudos: your AI Assistant!")
print(Fore.YELLOW + "Say 'Kudos' to activate me and 'exit' to end the conversation." + Style.RESET_ALL)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Select a more human-like voice (change index if necessary)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change the index to select a different voice
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

speaking = False  # Flag to track if AI is speaking

# Function to speak the response
def speak(text):
    global speaking
    speaking = True
    engine.say(text)
    engine.runAndWait()
    speaking = False

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to handle audio playback
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Dictionary for specific questions and corresponding audio responses
audio_responses = {
    "how are you": "D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\thank_you_for_asking.mp3",
    "what is your name": "D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\I'm_kudos.mp3",
    "how is the weather": "D:\\Work Space\\Programming\\PYTHON\\Project AI\\Assistant\\AI-PRED\\how_is_the_weather.mp3",
    "who created you":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\made_by.mp3",
    "Aapka kya naam hai":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\mera_naam.mp3",
    "Aapka kya name hai":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\mera_naam.mp3",
    "Aapka kya naam hai":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\mera_naam.mp3",
    "ap kya kr skte hein":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\ai_hon.mp3",
    "pakistan ka matlab kya":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\la_illah.mp3",
    "gilgit baltistan ke bare mein bataen":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\gb.mp3",
    "gilgit baltistan ke bare mein batayein":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\gb.mp3",
    "gilgit baltistan ke bare me bateyiye":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\gb.mp3",
    "uswa ke barey me bataye":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\uswa_barey.mp3",
    "uswa ke bare mein bataen":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\uswa_barey.mp3",
    "uswa ke bare me bateyiye":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\uswa_barey.mp3",
    "pakistan ke barey me bataye":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\pakistan.mp3",
    "pakistan ke bare mein bataen":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\pakistan.mp3",
    "pakistan ke bare me bateyiye":"D:\Work Space\Programming\PYTHON\Project AI\Assistant\AI-PRED\\pakistan.mp3"
    # Add more questions and corresponding audio file paths here
}

# Function to handle specific questions
def handle_specific_questions(question):
    question_lower = question.lower()
    if question_lower in audio_responses:
        play_audio(audio_responses[question_lower])  # Play the corresponding audio file
        print(Fore.GREEN + f"Playing response for '{question_lower}'" + Style.RESET_ALL)
        return True
    return False

# Function to handle website opening
def open_website(site_name):
    if not site_name.startswith("http://") and not site_name.startswith("https://"):
        site_name = site_name.replace(" ", "")
        site_name = "https://" + site_name + ".com"
    webbrowser.open(site_name)
    return True

# Function to handle Google searches
def search_google(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    print(Fore.GREEN + f"Searching Google for {query}" + Style.RESET_ALL)
    speak(f"Searching Google for {query}")
    return True

# Function to play a YouTube video directly
def play_youtube_video(query):
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()["result"][0]
    video_url = result["link"]
    print(Fore.GREEN + f"Playing {query} on YouTube" + Style.RESET_ALL)
    speak(f"Playing {query} on YouTube")
    webbrowser.open(video_url)
    return True

# Function to handle additional features
def respond_with_features(voice_data):
    voice_data_lower = voice_data.lower()

    if handle_specific_questions(voice_data_lower):
        return True

    if "open" in voice_data_lower:
        site_name = voice_data_lower.split("open")[-1].strip()
        if open_website(site_name):
            print(Fore.GREEN + f"Opening {site_name}" + Style.RESET_ALL)
            speak(f"Opening {site_name}")
            return True  
    elif "play" in voice_data_lower:
        search_query = voice_data_lower.split("play")[-1].strip()
        return play_youtube_video(search_query)
    elif "search" in voice_data_lower:
        search_query = voice_data_lower.split("search")[-1].strip()
        if search_google(search_query):
            return True  
    return False 

# Function to listen for the "Kudos" keyword
def listen_for_kudos():
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(Fore.YELLOW + "Waiting for 'Kudos'..." + Style.RESET_ALL)
            audio = recognizer.listen(source)

            try:
                keyword = recognizer.recognize_google(audio)
                if "kudos" in keyword.lower():
                    print(Fore.GREEN + "'Kudos' detected! How can I assist you?" + Style.RESET_ALL)
                    speak("Yes, how can I assist you?")
                    handle_conversation()  # Proceed to the main conversation loop

            except sr.UnknownValueError:
                continue  # Keep listening if no keyword is detected
            except sr.RequestError as e:
                print(Fore.RED + f"Could not request results from Google Speech Recognition service; {e}" + Style.RESET_ALL)

# Function to handle the conversation once activated
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
                    print(Fore.CYAN + "Goodbye! Say 'Kudos' to activate me again." + Style.RESET_ALL)
                    speak("Goodbye!")
                    break  # Exit the conversation loop and return to waiting for 'Kudos'

                # Check if the user wants to stop speaking
                if "stop speaking" in question.lower() and speaking:
                    engine.stop()
                    print(Fore.YELLOW + "Stopped speaking." + Style.RESET_ALL)
                    return

                # Calling New Feature Function
                if not respond_with_features(question):
                    response = chat_session.send_message(question)
                    response_text = response.text

                    # Avoid special characters in the response
                    response_text = response_text.replace('*', '').replace('#', '')

                    # Provide a short response unless a long one is explicitly requested
                    if any(keyword in question.lower() for keyword in ["detailed", "long", "detail", "explain in detail"]):
                        # Limit the response to a paragraph of 4-6 sentences
                        sentences = response_text.split(". ")
                        detailed_response = ". ".join(sentences[:6]) + "."  # Get the first 6 sentences
                        print("\n" + Fore.BLUE + "Kudos: " + detailed_response + Style.RESET_ALL + "\n")
                        speak(detailed_response)
                    else:
                        short_response = response_text.split(". ")[0] + "."
                        print("\n" + Fore.BLUE + "Kudos: " + short_response + Style.RESET_ALL + "\n")
                        speak(short_response)

            except sr.UnknownValueError:
                print(Fore.RED + "Sorry, I could not understand the audio." + Style.RESET_ALL)
            except sr.RequestError as e:
                print(Fore.RED + f"Could not request results from Google Speech Recognition service; {e}" + Style.RESET_ALL)

# Main loop for interaction
while True:
    listen_for_kudos()  # Wait for 'Kudos' keyword
