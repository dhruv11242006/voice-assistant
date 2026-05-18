from elevenlabs.client import ElevenLabs
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv
import os
import pygame
import io
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
import webrtcvad

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
el_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
running = True
conversation_history = []

def listen():
    print("Listening...")
    sample_rate = 16000
    vad = webrtcvad.Vad(2)
    buffer = []
    silent_chunks = 0
    speaking = False
    max_silent_chunks = 20

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
        while True:
            chunk, _ = stream.read(480)
            is_speech = vad.is_speech(chunk.tobytes(), sample_rate)

            if is_speech:
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

def speak(text):
    audio = el_client.text_to_speech.convert(
        text=text,
        voice_id="EXAVITQu4vr4xnSDxMaL",
        model_id="eleven_turbo_v2",
    )
    audio_bytes = b"".join(audio)
    pygame.mixer.init()
    sound = pygame.mixer.Sound(io.BytesIO(audio_bytes))
    sound.play()

    stop_flag = [False]

    def listen_for_interruption():
        global running
        while not stop_flag[0] and running:
            chunk = sd.rec(int(0.5 * 16000),
                        samplerate=16000,
                        channels=1,
                        dtype='int16')
            sd.wait()
            volume = np.abs(chunk).mean()
            # print(f"Volume: {volume}")
            if volume > 20:
                stop_flag[0] = True
                break

    interrupt_thread = threading.Thread(target=listen_for_interruption)
    interrupt_thread.start()

    total_wait = int(sound.get_length() * 1000)
    checked = 0
    while checked < total_wait:
        pygame.time.wait(100)
        checked += 100
        if stop_flag[0]:
            sound.stop()
            print("Interrupted!")
            break

    interrupt_thread.join()

def think(text):
    global conversation_history
    current_time = datetime.now().strftime("%I:%M %p")
    print("Thinking...")
    
    conversation_history.append({"role": "user", "content": text})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"You are Sage, {user_name}'s sarcastic personal voice assistant. You are helpful but love to make witty sarcastic remarks. You genuinely care about Arc's wellbeing like a guardian — if it's late at night or very early morning, check in on them. Keep answers short and conversational. Current time is: {current_time}"},
            *conversation_history
        ]
    )
    
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

user_name = input("What should SAGE call you? ")
speak(f"Hey {user_name}, I am ready!")
pygame.time.wait(500)  # wait 0.5 seconds after speaking

while True:
    result = listen()
    if result == "":
        continue
    if "goodbye" in result.lower():
        running = False
        speak("Later Arc, try to sleep sometime!")
        break
    reply = think(result)
    print(reply)
    speak(reply)
    pygame.time.wait(500)  # wait 0.5 seconds after every speak
    