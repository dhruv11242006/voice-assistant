import edge_tts
import asyncio
import pygame
import threading
import sounddevice as sd
import webrtcvad
import os

from core.config import VOICE

async def speak_async(text):
    communicate = edge_tts.Communicate(
        text,
        voice=VOICE
    )

    await communicate.save("temp/temp_speech.mp3")

def speak(ui, text):

    ui.set_status("Speaking")

    asyncio.run(speak_async(text))

    pygame.mixer.music.load("temp/temp_speech.mp3")

    pygame.mixer.music.play()

    interrupted = [False]

    mic_done = [False]

    def watch_mic():

        try:
            vad = webrtcvad.Vad(3)

            with sd.InputStream(
                samplerate=16000,
                channels=1,
                dtype='int16',
                blocksize=480
            ) as stream:

                while not interrupted[0]:

                    chunk, _ = stream.read(480)

                    is_human = vad.is_speech(
                        chunk.tobytes(),
                        16000
                    )

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

    os.remove("temp/temp_speech.mp3")