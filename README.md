# 🎙️ SAGE — Smart Autonomous General Executive

> *A sarcastic, fast, always-listening personal voice assistant that actually talks back.*

Built from scratch in Python. Powered by Groq's insane speed, Llama 3.3's brain, and ElevenLabs' voice. No wake word. No button. No nonsense. Just talk.

---

## ✨ Features

- 🎤 **Smart Voice Detection** — starts recording when you speak, stops when you go silent
- 🧠 **Groq + Llama 3.3** — lightning fast AI responses
- 🔊 **ElevenLabs TTS** — natural sounding voice output
- 💬 **Conversation Memory** — remembers everything across sessions
- 💾 **Persistent Memory** — remembers your name and chat history forever
- 😏 **Sarcastic Personality** — checks your wellbeing and roasts you while doing it
- ⏰ **Time Awareness** — knows what time it is and reacts accordingly
- 👋 **"Goodbye"** — just say goodbye to exit

---
.
## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| Speech to Text | Groq Whisper Large v3 Turbo |
| AI Brain | Llama 3.3 70B via Groq API |
| Text to Speech | ElevenLabs |
| Audio Recording | SoundDevice + NumPy |
| Audio Playback | Pygame |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/dhruv11242006/voice-assistant.git
cd voice-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API keys

Create a `.env` file in the project folder:

```
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

Get your free API keys:
- Groq → [console.groq.com](https://console.groq.com)
- ElevenLabs → [elevenlabs.io](https://elevenlabs.io)

### 4. Run it

```bash
python assistant.py
```

SAGE will ask your name on first run and remember it for the session 😄

### 5. First run

SAGE will ask your name and create a `memory.json` file automatically — no need to create it manually.

---

## 💬 Usage

Just run it and start talking. SAGE is always listening.

- Ask anything → it answers
- Talk over it → it stops and listens
- Say **"goodbye"** → it exits

---

## 🔮 Roadmap

- [x] Persistent memory across sessions
- [ ] Web search integration
- [ ] Weather updates
- [ ] Wake word detection
- [ ] Reminders and alarms
---

## 👤 Author

**Dhruv** — built this as a beginner Python project from scratch.

---

> *"Why are you up at 3am asking me things?" — SAGE, probably*