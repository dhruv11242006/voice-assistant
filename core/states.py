from enum import Enum

class AssistantState(Enum):
    IDLE = "Idle"
    LISTENING = "Listening"
    THINKING = "Thinking"
    SPEAKING = "Speaking"