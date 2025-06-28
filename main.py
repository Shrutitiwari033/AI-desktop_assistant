import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import pyttsx3
import google.generativeai as genai
from config import api_key

chatStr = ""

# Initialize text-to-speech engine for Windows
engine = pyttsx3.init()

def say(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Initialize genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

def chat(query):
    global chatStr
    chatStr += f"You: {query}\nJarvis: "

    try:
        response = model.generate_content(chatStr)
        reply = response.text.strip()
        say(reply)
        chatStr += f"{reply}\n"
        return reply
    except Exception as e:
        say("Sorry, an error occurred while processing your request.")
        print("Error:", e)
        return ""

def ai(prompt):
    try:
        response = model.generate_content(prompt)
        text = f"Google GenAI response for Prompt: {prompt}\n\n{response.text.strip()}"
        if not os.path.exists("GenAI"):
            os.mkdir("GenAI")

        filename = f"GenAI/{prompt[:50].replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        say("Response saved successfully.")
    except Exception as e:
        say("Failed to generate or save the response.")
        print("Error:", e)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"You: {query}")
            return query
        except Exception as e:
            say("Some error occurred while recognizing speech.")
            print("Speech Recognition Error:", e)
            return ""

if __name__ == '__main__':
    say("Welcome to Jarvis A.I powered by Gemini")
    while True:
        query = takeCommand()
        if not query:
            continue

        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.org"],
            ["google", "https://www.google.com"]
        ]
        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])
                break

        if "open music" in query.lower():
            musicPath = "C:\\Users\\91876\\Downloads\\Laal Pari - Housefull 5 128 Kbps.mp3" # Change path
            os.startfile(musicPath)

        elif "the time" in query.lower():
            timeStr = datetime.datetime.now().strftime("%H:%M")
            say(f"The time is {timeStr}")


        elif "open camera" in query.lower():
          os.system("start microsoft.windows.camera:")



        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "jarvis quit" in query.lower():
            say("Goodbye!")
            break

        elif "reset chat" in query.lower():
            chatStr = ""
            say("Chat reset.")

        else:
            chat(query)
