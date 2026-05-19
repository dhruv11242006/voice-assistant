import json
import os

def load_memory():
    if os.path.exists("data/memory.json"):
        with open("data/memory.json", "r") as f:
            return json.load(f)

    return {
        "user_name": "",
        "conversation_history": []
    }

def save_memory(user_name, conversation_history):
    with open("data/memory.json", "w") as f:
        json.dump({
            "user_name": user_name,
            "conversation_history": conversation_history
        }, f)