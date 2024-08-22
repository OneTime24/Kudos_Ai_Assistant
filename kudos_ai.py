import os
import google.generativeai as genai
from colorama import Fore, Style
import pyttsx3
import speech_recognition as sr
import webbrowser
from youtubesearchpython import VideosSearch

# Gemini API key
genai.configure(api_key="AIzaSyC8DdamcmYru2GqJ3YhpGIgrl3Zi0BbPiE")

# model configuration
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
print(Fore.YELLOW + "Say 'exit' to end the conversation." + Style.RESET_ALL)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to handle website opening
def open_website(site_name):
    # common website shortcuts
    common_sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "github": "https://www.github.com",
    }

    # Check if site is in the common website shortcut
    for key, url in common_sites.items():
        if key in site_name.lower():
            webbrowser.open(url)
            return True

    # If not then attempt to open directly
    if not site_name.startswith("http://") and not site_name.startswith("https://"):
        site_name = site_name.replace(" ", "")  # Remove spaces from the site name
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
    # Feature 1: Open Website
    if "open" in voice_data.lower():
        site_name = voice_data.lower().split("open")[-1].strip()
        if open_website(site_name):
            print(Fore.GREEN + f"Opening {site_name}" + Style.RESET_ALL)
            speak(f"Opening {site_name}")
            return True  

    # Feature 2: Play YouTube Video Directly
    elif "play" in voice_data.lower():
        search_query = voice_data.lower().split("play")[-1].strip()
        return play_youtube_video(search_query)

    # Feature 3: Search on Google
    elif "search" in voice_data.lower():
        search_query = voice_data.lower().split("search")[-1].strip()
        if search_google(search_query):
            return True  

    return False 

# Main loop for interaction
while True:
    with sr.Microphone() as source:
        print(Fore.YELLOW + "Listening..." + Style.RESET_ALL)
        audio = recognizer.listen(source)
        try:
            question = recognizer.recognize_google(audio)
            print(Fore.GREEN + "You: " + question + Style.RESET_ALL)

            if question.lower() == "exit":
                print(Fore.CYAN + "Goodbye!" + Style.RESET_ALL)
                break

            # Calling New Feature Function
            if not respond_with_features(question):
                response = chat_session.send_message(question)
                print("\n" + Fore.BLUE + "Kudos: " + response.text + Style.RESET_ALL + "\n")
                speak(response.text)

        except sr.UnknownValueError:
            print(Fore.RED + "Sorry, I could not understand the audio." + Style.RESET_ALL)
        except sr.RequestError as e:
            print(Fore.RED + f"Could not request results from Google Speech Recognition service; {e}" + Style.RESET_ALL)
