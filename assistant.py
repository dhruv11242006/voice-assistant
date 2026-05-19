from groq import Groq
from datetime import datetime
from dotenv import load_dotenv
import os
import pygame
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from ddgs import DDGS
import webrtcvad
import json
import threading
import edge_tts
import asyncio
from ui.ui import SageUI
import random
import requests

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
load_dotenv()
ui = SageUI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# el_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
running = True
conversation_history = []
pygame.mixer.init()



def load_memory():
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            return json.load(f)
    return {"user_name": "", "conversation_history": []}

def save_memory():
    with open("memory.json", "w") as f:
        json.dump({
            "user_name": user_name,
            "conversation_history": conversation_history
        }, f)

def search(query):
    print(f"Searching for: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No results found"
        summary = ""
        for r in results:
            summary += r['title'] + " — " + r['body'] + "\n"
        return summary
    except Exception as e:
        print(f"Search failed: {e}")
        return ""
    
def get_weather(city="Paderborn"):
    try:
        # first get coordinates for the city
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url).json()
        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]

        # then get weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weathercode,windspeed_10m&temperature_unit=celsius"
        weather_response = requests.get(weather_url).json()
        current = weather_response["current"]

        temp = current["temperature_2m"]
        wind = current["windspeed_10m"]
        code = current["weathercode"]

        weather_codes = {
            0: "clear sky", 1: "mainly clear", 2: "partly cloudy",
            3: "overcast", 45: "foggy", 48: "foggy",
            51: "light drizzle", 61: "light rain", 63: "moderate rain",
            71: "light snow", 73: "moderate snow", 80: "rain showers",
            95: "thunderstorm"
        }
        condition = weather_codes.get(code, "unknown conditions")

        return f"Temperature: {temp}°C, Condition: {condition}, Wind: {wind} km/h"
    except Exception as e:
        print(f"Weather failed: {e}")
        return "couldn't get weather data"

def listen():
    ui.set_status("Listening")
    print("Listening...")
    sample_rate = 16000
    buffer = []
    silent_chunks = 0
    speaking = False
    max_silent_chunks = 15

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16', blocksize=3200) as stream:
        while True:
            chunk, _ = stream.read(3200)
            volume = np.abs(chunk).mean()

            if volume > 15:
                speaking = True
                silent_chunks = 0
                buffer.append(chunk)
            elif speaking:
                silent_chunks += 1
                buffer.append(chunk)
                if silent_chunks > max_silent_chunks:
                    break

    if not buffer:
        print("Sorry, I didn't catch that")
        return ""

    audio = np.concatenate(buffer)
    wav.write("temp.wav", sample_rate, audio)
    print("Processing...")

    with open("temp.wav", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
        )

    text = transcription.text.strip()
    if text == "":
        print("Sorry, I didn't catch that")
        return ""

    print(f"You said: {text}")
    return text


async def speak_async(text):
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.save("temp_speech.mp3")

def speak(text):
    ui.set_status("Speaking")
    asyncio.run(speak_async(text))
    pygame.mixer.music.load("temp_speech.mp3")
    pygame.mixer.music.play()

    interrupted = [False]
    mic_done = [False]

    def watch_mic():
        try:
            vad = webrtcvad.Vad(3)
            with sd.InputStream(samplerate=16000, channels=1, dtype='int16', blocksize=480) as stream:
                while not interrupted[0]:
                    chunk, _ = stream.read(480)
                    is_human = vad.is_speech(chunk.tobytes(), 16000)
                    if is_human:
                        interrupted[0] = True
                        pygame.mixer.music.stop()
                        print("Interrupted!")
                        break
        finally:
            mic_done[0] = True

    watch_thread = threading.Thread(target=watch_mic)
    watch_thread.start()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    interrupted[0] = True
    while not mic_done[0]:
        pygame.time.wait(50)

    watch_thread.join()
    pygame.mixer.music.unload()
    os.remove("temp_speech.mp3")



def think(text):
    ui.set_status("Thinking")
    global conversation_history
    current_time = datetime.now().strftime("%I:%M %p")
    print("Thinking...")
    weather_words = ["weather", "temperature", "cold", "hot", "raining", "sunny", "forecast"]
    tool_results = ""

    if any(word in text.lower() for word in weather_words):
        import re
        cities = ["Paderborn", "Berlin", "London", "Paris", "New York"]
        city = "Paderborn"
        for c in cities:
            if c.lower() in text.lower():
                city = c
                break
        tool_results = get_weather(city)
        print(f"Weather fetched: {tool_results}")
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]
    conversation_history.append({"role": "user", "content": text})

    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the web ONLY when the user explicitly asks about current news, recent events, live scores, or real-time prices. Do NOT search for general knowledge or things you already know.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "the search query to look up"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a city. Use this when the user asks about weather, temperature, or climate.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "the city name to get weather for"}
                    },
                    "required": ["city"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": f"You are Sage, {user_name}'s sarcastic personal voice assistant. You are helpful but love to make witty sarcastic remarks. You genuinely care about {user_name}'s wellbeing — if it's late at night or very early morning, check in on them. Keep answers short and conversational. Current time is: {current_time}"},
            *conversation_history
        ],
        tools=tools,
        tool_choice="auto",
        parallel_tool_calls=False
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        if tool_name == "search_web":
            print(f"Searching for: {args['query']}")
            tool_results = search(args["query"])
        elif tool_name == "get_weather":
            print(f"Getting weather for: {args['city']}")
            tool_results = get_weather(args["city"])

        final_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"You are Sage, {user_name}'s sarcastic personal voice assistant. You are helpful but love to make witty sarcastic remarks. You genuinely care about {user_name}'s wellbeing — if it's late at night or very early morning, check in on them. Keep answers short and conversational. Current time is: {current_time}"},
                *conversation_history,
                {"role": "user", "content": f"Tool results: {tool_results}\n\nNow answer the original question using these results."}
            ]
        )
        reply = final_response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    else:
        reply = message.content

    conversation_history.append({"role": "assistant", "content": reply})
    return reply

memory = load_memory()
conversation_history = memory["conversation_history"]

if memory["user_name"] == "":
    user_name = input("What should SAGE call you? ")
else:
    user_name = memory["user_name"]
    print(f"Welcome back {user_name}!")

def assistant_loop():
    speak(f"Hey {user_name}, I am ready!")
    ui.set_status("Idle")
    while True:
        result = listen()
        if result == "":
            continue
        if "goodbye" in result.lower():
            running = False
            save_memory()
            goodbyes = [
                f"Later {user_name}, try not to miss me too much!",
                f"Goodbye {user_name}, go touch some grass.",
                f"See ya {user_name}, I'll be here judging your life choices when you get back.",
                f"Finally some peace and quiet. Bye {user_name}!",
                f"Logging off. Try to survive without me {user_name}.",
                f"Goodbye {user_name}. Don't do anything I wouldn't do... actually, just don't do anything.",
            ]
            speak(random.choice(goodbyes))
            ui.root.quit()
            break
        reply = think(result)
        ui.add_message("You", result)
        ui.add_message("SAGE", reply)
        print(reply)
        speak(reply)
        save_memory()
        ui.set_status("Idle")

threading.Thread(target=assistant_loop, daemon=True).start()
ui.run()
