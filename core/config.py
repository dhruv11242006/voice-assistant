from groq import Groq
from dotenv import load_dotenv
import os
import pygame

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

pygame.mixer.init()

VOICE = "en-US-JennyNeural"

STT_MODEL = "whisper-large-v3-turbo"

CHAT_MODEL = "llama-3.3-70b-versatile"

SAMPLE_RATE = 16000

VOLUME_THRESHOLD = 15