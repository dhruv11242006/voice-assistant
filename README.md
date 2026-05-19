# 🎙️ SAGE — Smart Autonomous General Executive
> *A sarcastic, fast, always-listening personal voice assistant that actually talks back.*

Built from scratch in Python. Powered by Groq's insane speed, Llama 3.3's brain, and Microsoft Edge TTS voice. No wake word. No button. No nonsense. Just talk.

---

## ✨ Features
- 🎤 **Smart Voice Detection** — starts recording when you speak, stops when you go silent
- 🧠 **Groq + Llama 3.3** — lightning fast AI responses
- 🔊 **Edge TTS** — free, unlimited Microsoft neural voice (en-US-JennyNeural)
- 💬 **Conversation Memory** — remembers everything across sessions
- 💾 **Persistent Memory** — remembers your name and chat history forever
- 😏 **Sarcastic Personality** — roasts you while actually being helpful
- ⏰ **Time Awareness** — knows what time it is and reacts accordingly
- 🌤️ **Live Weather** — real-time weather via Open-Meteo (no API key needed)
- 🔍 **Web Search** — searches DuckDuckGo for news, events, and real-time info
- ✋ **Voice Interruption** — talk over SAGE and it stops immediately
- 🖥️ **Desktop UI** — dark themed chat interface with status indicator
- 👋 **"Goodbye"** — just say goodbye to exit

---

## 🛠️ Tech Stack
| Component | Tool |
|---|---|
| Speech to Text | Groq Whisper Large v3 Turbo |
| AI Brain | Llama 3.3 70B via Groq API |
| Text to Speech | Edge TTS (en-US-JennyNeural) |
| Audio Recording | SoundDevice + NumPy |
| Audio Playback | Pygame |
| Web Search | DuckDuckGo (ddgs) |
| Weather | Open-Meteo API (free, no key) |
| UI | CustomTkinter |
| Memory | JSON file |
| Interruption | WebRTCVAD |

---

## 📁 Project Structure
```
sage/
│
├── main.py
│
├── core/
│   ├── brain.py       # AI logic
│   ├── audio.py       # Recording + VAD
│   ├── speech.py      # TTS
│   ├── memory.py      # Load/save memory
│   ├── tools.py       # Weather + search
│   ├── router.py      # Intent routing
│   └── config.py      # API keys + models
│
├── ui/
│   └── ui.py          # Desktop UI
│
├── data/
│   └── memory.json    # Auto-generated
│
├── temp/              # Temp audio files
├── .env
├── requirements.txt
└── README.md
```

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

> **Windows users:** Install ffmpeg manually from [gyan.dev](https://gyan.dev/ffmpeg/builds/), extract to `C:\ffmpeg` and add `C:\ffmpeg\bin` to your PATH.

### 3. Set up your API key
Create a `.env` file in the project folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at [console.groq.com](https://console.groq.com)

> No ElevenLabs key needed anymore — switched to Edge TTS which is free and unlimited.

### 4. Run it
```bash
python main.py
```

### 5. First run
SAGE will ask your name and create a `memory.json` file automatically.

---

## 💬 Usage
Just run it and start talking. SAGE is always listening.
- Ask anything → it answers
- Ask about weather → live data, no key needed
- Ask about news/events → searches DuckDuckGo automatically
- Talk over it → it stops and listens
- Say **"goodbye"** → it exits

---

## 🔮 Roadmap
- [x] Persistent memory across sessions
- [x] Web search integration
- [x] Live weather updates
- [x] Desktop UI
- [x] Voice interruption
- [x] Modular architecture
- [ ] Wake word detection
- [ ] Reminders and alarms
- [ ] Computer control
- [ ] Better long-term memory (SQLite/ChromaDB)
- [ ] Local AI option (Ollama)

---

## 👤 Author
**Dhruv** — built this as a beginner Python project from scratch.

---

> *"Why are you up at 3am asking me things?" — SAGE, probably*