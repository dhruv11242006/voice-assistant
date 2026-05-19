from datetime import datetime
from core.config import client, CHAT_MODEL
from core.tools import search, get_weather
from core.router import route_tools

def think(user_name, text, conversation_history, ui):
    ui.set_status("Thinking")
    current_time = datetime.now().strftime("%I:%M %p")

    system_prompt = (
        f"You are Sage, {user_name}'s witty and sarcastic AI assistant. "
        f"You ALWAYS respond with sarcasm and dry humor, no matter what. "
        f"Never break character. Never be overly nice or formal. "
        f"Keep responses short and punchy. "
        f"Current time is {current_time}. "
        f"You are located in Paderborn, Germany. "
    )

    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    conversation_history.append({
        "role": "user",
        "content": text
    })

    print("Thinking...")

    # Route to tools first
    tool_result = route_tools(text, get_weather, search)

    if tool_result:
        # Tool returned data — inject into model
        messages = [
            {"role": "system", "content": system_prompt},
            *conversation_history,
            {
                "role": "system",
                "content": (
                    f"Here is the real-time data you need to answer: {tool_result}. "
                    f"Use this to answer the user naturally and sarcastically. "
                    f"Do NOT say you don't have real-time access."
                )
            }
        ]
    else:
        # No tool needed — straight to model
        messages = [
            {"role": "system", "content": system_prompt},
            *conversation_history
        ]

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages
    )

    reply = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply, conversation_history