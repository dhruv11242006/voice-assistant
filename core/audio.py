import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

from core.config import client
from core.config import SAMPLE_RATE
from core.config import STT_MODEL
from core.config import VOLUME_THRESHOLD

def listen(ui):
    ui.set_status("Listening")

    print("Listening...")

    buffer = []

    silent_chunks = 0

    speaking = False

    max_silent_chunks = 15

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16',
        blocksize=3200
    ) as stream:

        while True:

            chunk, _ = stream.read(3200)

            volume = np.abs(chunk).mean()

            if volume > VOLUME_THRESHOLD:
                speaking = True
                silent_chunks = 0
                buffer.append(chunk)

            elif speaking:
                silent_chunks += 1
                buffer.append(chunk)

                if silent_chunks > max_silent_chunks:
                    break

    if not buffer:
        return ""

    audio = np.concatenate(buffer)

    wav.write("temp/temp.wav", SAMPLE_RATE, audio)

    with open("temp/temp.wav", "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=STT_MODEL
        )

    text = transcription.text.strip()

    print(f"You said: {text}")

    return text