import customtkinter as ctk
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SageUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("SAGE")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        # title
        self.title_label = ctk.CTkLabel(
            self.root,
            text="⚡ SAGE",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=20)

        # status indicator
        self.status_label = ctk.CTkLabel(
            self.root,
            text="● Initializing...",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.status_label.pack(pady=5)

        # chat frame
        self.chat_frame = ctk.CTkScrollableFrame(
            self.root,
            width=360,
            height=400
        )
        self.chat_frame.pack(pady=10, padx=20)

    def set_status(self, status):
        colors = {
            "Listening": "#00ff88",
            "Thinking": "#ffaa00",
            "Speaking": "#00aaff",
            "Idle": "gray"
        }
        color = colors.get(status, "gray")
        self.status_label.configure(
            text=f"● {status}",
            text_color=color
        )
        self.root.update()

    def add_message(self, sender, message):
        is_sage = sender == "SAGE"

        bubble = ctk.CTkFrame(
            self.chat_frame,
            fg_color="#1e3a5f" if is_sage else "#2d4a1e",
            corner_radius=15
        )
        bubble.pack(
            pady=5,
            padx=10,
            anchor="w" if is_sage else "e",
            fill="none"
        )

        name_label = ctk.CTkLabel(
            bubble,
            text=sender,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00aaff" if is_sage else "#00ff88"
        )
        name_label.pack(padx=10, pady=(8,2), anchor="w")

        msg_label = ctk.CTkLabel(
            bubble,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=250,
            justify="left"
        )
        msg_label.pack(padx=10, pady=(2,8), anchor="w")

        self.root.update()
        self.root.update_idletasks()

        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = SageUI()
    ui.add_message("SAGE", "Hey! I am ready.")
    ui.add_message("You", "What is the weather like?")
    ui.add_message("SAGE", "Searching for that right now...")
    ui.set_status("Listening")
    ui.run()