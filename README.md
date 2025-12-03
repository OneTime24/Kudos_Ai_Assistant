🎙️ Kudos – Voice Activated AI Assistant

Kudos is a Python-based AI assistant that listens to the keyword “Kudos”, responds through Gemini AI, speaks using TTS, plays audio replies, searches Google, opens websites, and even plays YouTube videos — all with voice commands.

🚀 Features
🎧 Voice Activated

Detects keyword “Kudos”

Listens and replies automatically

🧠 AI Responses

Uses Google Gemini 1.5 Flash

Short or detailed answers based on your question

🔊 Human-like Text-to-Speech

Uses pyttsx3

Adjustable voice, rate, and volume

🎵 Smart Audio Replies

Plays pre-recorded MP3 responses for questions like:

“How are you?”

“Who created you?”

“Pakistan ka matlab kya”

“Gilgit Baltistan ke bare mein bataen”

🌍 Web Automation

“Open YouTube” → opens website

“Search Python lists” → Google search

“Play Atif Aslam song” → Plays first YouTube result

🛠 Technologies Used

Python 3

Google Gemini API

SpeechRecognition

Pygame (audio playback)

pyttsx3 (text-to-speech)

YouTubeSearchPython

Webbrowser module

📥 Installation
1. Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

2. Install dependencies
pip install google-generativeai
pip install SpeechRecognition
pip install pyttsx3
pip install pygame
pip install youtube-search-python
pip install colorama

3. Set your Gemini API Key

Inside the code:

genai.configure(api_key="YOUR_API_KEY")

▶️ Usage

Run the program:

python main.py


You will see:

Welcome to Kudos: your AI Assistant!
Say 'Kudos' to activate me...


Then speak commands like:

“Kudos”

“Open Google”

“Search Python functions”

“Play Dil Dil Pakistan”

“How are you?”

“Exit”

📂 Project Structure
project/
│── main.py
│── README.md
│── audio/
│     ├── how_are_you.mp3
│     ├── gilgit_baltistan.mp3
│     └── etc...

❤️ Creator

Made by Mohsin Ali and Team
