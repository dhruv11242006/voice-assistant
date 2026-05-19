import threading
import random

from ui.ui import SageUI

from core.audio import listen
from core.speech import speak
from core.brain import think
from core.memory import load_memory
from core.memory import save_memory

ui = SageUI()

memory = load_memory()

conversation_history = memory["conversation_history"]

if memory["user_name"] == "":
    user_name = input("What should SAGE call you? ")

else:
    user_name = memory["user_name"]

    print(f"Welcome back {user_name}!")

def assistant_loop():

    speak(ui, f"Hey {user_name}, I am ready!")

    ui.set_status("Idle")

    while True:

        result = listen(ui)

        if result == "":
            continue

        if "goodbye" in result.lower():

            save_memory(
                user_name,
                conversation_history
            )

            goodbyes = [
                f"Later {user_name}!",
                f"Go touch some grass {user_name}.",
                f"See ya {user_name}!"
            ]

            speak(ui, random.choice(goodbyes))

            ui.root.quit()

            break

        reply, updated_history = think(
            user_name,
            result,
            conversation_history,
            ui
        )
        print(f"SAGE: {reply}")
        ui.add_message("You", result)

        ui.add_message("SAGE", reply)

        speak(ui, reply)

        save_memory(
            user_name,
            updated_history
        )

threading.Thread(
    target=assistant_loop,
    daemon=True
).start()

ui.run()