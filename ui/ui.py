import customtkinter as ctk
import threading
import sounddevice as sd
import numpy as np
import math
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "bg":           "#0a0a0a",
    "surface":      "#141414",
    "border":       "#222222",
    "text":         "#f0f0f0",
    "subtext":      "#666666",
    "accent":       "#ffffff",
    "sage_bubble":  "#1a1a1a",
    "user_bubble":  "#1f1f1f",
    "sage_name":    "#aaaaaa",
    "user_name":    "#666666",
    "listening":    "#ffffff",
    "thinking":     "#ffcc44",
    "speaking":     "#44ddff",
    "idle":         "#333333",
}

class MicVisualizer(ctk.CTkCanvas):
    def __init__(self, parent, size=120, **kwargs):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=COLORS["bg"],
            highlightthickness=0,
            **kwargs
        )
        self.size = size
        self.cx = size // 2
        self.cy = size // 2
        self.base_r = size // 4
        self.volume = 0.0
        self.target_volume = 0.0
        self.state = "idle"
        self.angle = 0
        self.running = True
        self._draw()
        self._animate()
        self._start_mic()

    def _start_mic(self):
        def callback(indata, frames, time_info, status):
            rms = float(np.sqrt(np.mean(indata ** 2)))
            self.target_volume = min(rms * 8, 1.0)

        def run():
            try:
                with sd.InputStream(
                    channels=1,
                    samplerate=16000,
                    blocksize=1024,
                    callback=callback
                ):
                    while self.running:
                        time.sleep(0.05)
            except Exception:
                pass

        threading.Thread(target=run, daemon=True).start()

    def set_state(self, state):
        self.state = state

    def _animate(self):
        if not self.running:
            return
        # Smooth volume
        self.volume += (self.target_volume - self.volume) * 0.2
        self.angle = (self.angle + 2) % 360
        self._draw()
        self.after(30, self._animate)

    def _draw(self):
        self.delete("all")
        cx, cy = self.cx, self.cy

        state_colors = {
            "idle":      COLORS["idle"],
            "Listening": COLORS["listening"],
            "Thinking":  COLORS["thinking"],
            "Speaking":  COLORS["speaking"],
        }
        color = state_colors.get(self.state, COLORS["idle"])

        # Outer ripple rings when active
        if self.state in ("Listening", "Speaking"):
            for i in range(3):
                offset = (self.angle / 360 + i / 3) % 1.0
                ring_r = self.base_r + 10 + offset * 25
                alpha_val = int((1 - offset) * 40)
                ring_color = self._fade(color, alpha_val)
                self.create_oval(
                    cx - ring_r, cy - ring_r,
                    cx + ring_r, cy + ring_r,
                    outline=ring_color, width=1
                )

        # Pulse radius based on mic volume
        pulse = self.base_r + self.volume * 18
        if self.state == "Thinking":
            # Rotating arc for thinking
            start = self.angle
            self.create_arc(
                cx - pulse, cy - pulse,
                cx + pulse, cy + pulse,
                start=start, extent=270,
                outline=color, width=2, style="arc"
            )
        else:
            # Main circle
            self.create_oval(
                cx - pulse, cy - pulse,
                cx + pulse, cy + pulse,
                outline=color,
                width=2 if self.state == "idle" else 1,
                fill=""
            )

        # Inner filled circle
        inner_r = self.base_r * 0.55
        self.create_oval(
            cx - inner_r, cy - inner_r,
            cx + inner_r, cy + inner_r,
            fill=color, outline=""
        )

        # Mic icon (simple lines)
        mic_w = inner_r * 0.35
        mic_h = inner_r * 0.55
        self.create_rectangle(
            cx - mic_w, cy - mic_h,
            cx + mic_w, cy + mic_h * 0.3,
            fill=COLORS["bg"], outline=COLORS["bg"],
            width=0
        )
        # Mic stand
        self.create_line(cx, cy + mic_h * 0.3, cx, cy + mic_h * 0.7,
                         fill=COLORS["bg"], width=2)
        self.create_line(
            cx - mic_w * 1.2, cy + mic_h * 0.7,
            cx + mic_w * 1.2, cy + mic_h * 0.7,
            fill=COLORS["bg"], width=2
        )

    def _fade(self, hex_color, alpha):
        # Blend hex_color toward bg by alpha (0-255)
        def parse(h):
            h = h.lstrip("#")
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        fg = parse(hex_color)
        bg = parse(COLORS["bg"])
        t = alpha / 255
        r = int(bg[0] + (fg[0] - bg[0]) * t)
        g = int(bg[1] + (fg[1] - bg[1]) * t)
        b = int(bg[2] + (fg[2] - bg[2]) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def destroy(self):
        self.running = False
        super().destroy()


class SageUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("SAGE")
        self.root.geometry("420x720")
        self.root.resizable(False, False)
        self.root.configure(fg_color=COLORS["bg"])

        self._build_header()
        self._build_visualizer()
        self._build_status()
        self._build_chat()

    def _build_header(self):
        header = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        header.pack(pady=(24, 0), padx=24, fill="x")

        ctk.CTkLabel(
            header,
            text="SAGE",
            font=ctk.CTkFont(family="Courier", size=22, weight="bold"),
            text_color=COLORS["text"]
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Smart Autonomous General Executive",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["subtext"]
        ).pack(side="left", padx=(10, 0), pady=(4, 0))

    def _build_visualizer(self):
        viz_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        viz_frame.pack(pady=(16, 0))

        self.visualizer = MicVisualizer(viz_frame, size=130)
        self.visualizer.pack()

    def _build_status(self):
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Initializing...",
            font=ctk.CTkFont(family="Courier", size=11),
            text_color=COLORS["subtext"]
        )
        self.status_label.pack(pady=(8, 0))

    def _build_chat(self):
        # Divider
        divider = ctk.CTkFrame(
            self.root,
            height=1,
            fg_color=COLORS["border"]
        )
        divider.pack(fill="x", padx=24, pady=(16, 0))

        self.chat_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["subtext"],
            width=380,
            height=340
        )
        self.chat_frame.pack(pady=(8, 16), padx=16, fill="both", expand=True)

    def set_status(self, status):
        labels = {
            "Listening": "— listening",
            "Thinking":  "— thinking",
            "Speaking":  "— speaking",
            "Idle":      "— idle",
        }
        colors = {
            "Listening": COLORS["listening"],
            "Thinking":  COLORS["thinking"],
            "Speaking":  COLORS["speaking"],
            "Idle":      COLORS["subtext"],
        }
        self.status_label.configure(
            text=labels.get(status, f"— {status.lower()}"),
            text_color=colors.get(status, COLORS["subtext"])
        )
        self.visualizer.set_state(status)
        self.root.update()

    def add_message(self, sender, message):
        is_sage = sender == "SAGE"

        outer = ctk.CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        outer.pack(fill="x", pady=(0, 10))

        bubble = ctk.CTkFrame(
            outer,
            fg_color=COLORS["sage_bubble"] if is_sage else COLORS["user_bubble"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        bubble.pack(
            anchor="w" if is_sage else "e",
            padx=8
        )

        ctk.CTkLabel(
            bubble,
            text="SAGE" if is_sage else "You",
            font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
            text_color=COLORS["sage_name"] if is_sage else COLORS["user_name"]
        ).pack(padx=12, pady=(8, 2), anchor="w")

        ctk.CTkLabel(
            bubble,
            text=message,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text"],
            wraplength=260,
            justify="left"
        ).pack(padx=12, pady=(0, 10), anchor="w")

        self.root.update()
        self.root.update_idletasks()
        self.root.after(50, self._scroll_bottom)

    def _scroll_bottom(self):
        try:
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ui = SageUI()
    ui.add_message("SAGE", "Hey. Ready when you are.")
    ui.add_message("You", "What's the weather like?")
    ui.add_message("SAGE", "Checking... not that you couldn't do it yourself.")
    ui.set_status("Listening")
    ui.run()