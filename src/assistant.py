"""
NOVA — Neural Omni Virtual Assistant
Desktop Assistant using AIML + Python + Tkinter
"""

import os
import sys
import aiml
import datetime
import webbrowser
import subprocess
import platform
import tkinter as tk
from tkinter import scrolledtext
import threading
import urllib.parse


# ─────────────────────────────────────────────────────────
#  AIML Brain
# ─────────────────────────────────────────────────────────
class NOVABrain:
    """Loads the AIML kernel and handles response generation."""

    def __init__(self, aiml_path: str = "aiml/brain.aiml"):
        self.kernel = aiml.Kernel()
        print("[NOVA] Loading knowledge base...")
        self.kernel.learn(aiml_path)
        print("[NOVA] Ready!")

    def respond(self, user_input: str) -> str:
        """Return a response for the given user input."""
        raw = user_input.strip().upper()
        aiml_response = self.kernel.respond(raw)
        return self._execute_commands(raw, aiml_response)

    # --------------------------------------------------
    def _execute_commands(self, text: str, response: str) -> str:
        """Intercept special keywords and perform OS / system actions."""

        # ── Time ──────────────────────────────────────
        if "LAUNCH_BROWSER" not in response and text in ("TIME", "WHAT TIME IS IT",
                                                          "TELL ME THE TIME", "CURRENT TIME"):
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {now} ⏰"

        # ── Date ──────────────────────────────────────
        if text in ("DATE", "WHAT IS THE DATE", "WHAT IS TODAY",
                    "WHAT DAY IS IT", "TODAY DATE"):
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {today} 📅"

        # ── Browser ───────────────────────────────────
        if "LAUNCH_BROWSER" in response or text in ("OPEN BROWSER", "LAUNCH BROWSER"):
            webbrowser.open("https://www.google.com")
            return "Opening your web browser... 🌐"

        # ── Notepad ───────────────────────────────────
        if "LAUNCH_NOTEPAD" in response or text in ("OPEN NOTEPAD", "OPEN TEXT EDITOR"):
            self._open_app("notepad", "gedit", "TextEdit")
            return "Opening text editor... 📝"

        # ── Calculator ────────────────────────────────
        if "LAUNCH_CALCULATOR" in response or text in ("OPEN CALCULATOR", "OPEN CALC"):
            self._open_app("calc", "gnome-calculator", "Calculator")
            return "Opening calculator... 🧮"

        # ── Music ─────────────────────────────────────
        if "LAUNCH_MUSIC" in response or text in ("OPEN MUSIC", "PLAY MUSIC"):
            self._open_app("wmplayer", "rhythmbox", "Music")
            return "Opening music player... 🎵"

        # ── Weather ───────────────────────────────────
        if "GET_WEATHER" in response or text in ("WEATHER", "WEATHER TODAY",
                                                   "WHAT IS THE WEATHER",
                                                   "HOW IS THE WEATHER"):
            webbrowser.open("https://weather.com")
            return "Opening weather forecast for you... 🌤️"

        # ── Search ────────────────────────────────────
        for prefix in ("SEARCH FOR ", "SEARCH ", "GOOGLE ", "FIND ", "LOOK UP "):
            if text.startswith(prefix):
                query = text[len(prefix):].strip()
                if query:
                    encoded = urllib.parse.quote(query)
                    webbrowser.open(f"https://www.google.com/search?q={encoded}")
                    return f"Searching Google for '{query.title()}'... 🔍"

        # ── Shutdown ──────────────────────────────────
        if "SYSTEM_SHUTDOWN" in response:
            cmd = "shutdown /s /t 5" if platform.system() == "Windows" else "sudo shutdown -h now"
            os.system(cmd)
            return "Shutting down..."

        # ── Restart ───────────────────────────────────
        if "SYSTEM_RESTART" in response:
            cmd = "shutdown /r /t 5" if platform.system() == "Windows" else "sudo reboot"
            os.system(cmd)
            return "Restarting..."

        return response

    # --------------------------------------------------
    @staticmethod
    def _open_app(win: str, linux: str, mac: str):
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.Popen(win, shell=True)
            elif system == "Darwin":
                subprocess.Popen(["open", "-a", mac])
            else:
                subprocess.Popen(linux, shell=True)
        except Exception as e:
            print(f"[NOVA] Could not launch app: {e}")


# ─────────────────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────────────────
class NOVAApp:
    """Tkinter-based dark-mode chat interface for NOVA."""

    # Catppuccin-inspired dark palette
    C = {
        "bg":          "#1e1e2e",
        "header":      "#181825",
        "accent":      "#89b4fa",   # blue
        "accent2":     "#a6e3a1",   # green (online dot)
        "user_name":   "#89b4fa",
        "bot_name":    "#cba6f7",   # mauve
        "text":        "#cdd6f4",
        "muted":       "#6c7086",
        "input_bg":    "#313244",
        "btn_bg":      "#89b4fa",
        "btn_fg":      "#1e1e2e",
        "quick_bg":    "#313244",
        "quick_fg":    "#a6adc8",
    }

    QUICK_CMDS = [
        "What time is it?",
        "What is the date?",
        "Open Browser",
        "Search for Python",
        "Tell me a joke",
        "Weather",
        "Help",
    ]

    def __init__(self, root: tk.Tk, brain: NOVABrain):
        self.root = root
        self.brain = brain
        self._build_window()
        self._build_header()
        self._build_chat()
        self._build_input()
        self._build_quickbar()
        self._welcome()

    # ── Window ────────────────────────────────────────
    def _build_window(self):
        self.root.title("NOVA — Neural Omni Virtual Assistant")
        self.root.geometry("900x640")
        self.root.minsize(650, 440)
        self.root.configure(bg=self.C["bg"])

    # ── Header ────────────────────────────────────────
    def _build_header(self):
        bar = tk.Frame(self.root, bg=self.C["header"], height=62)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="✦  NOVA",
                 font=("Segoe UI", 17, "bold"),
                 bg=self.C["header"], fg=self.C["accent"]).pack(side="left", padx=18, pady=12)

        tk.Label(bar, text="Neural Omni Virtual Assistant",
                 font=("Segoe UI", 9),
                 bg=self.C["header"], fg=self.C["muted"]).pack(side="left", pady=12)

        self.status_lbl = tk.Label(bar, text="●  Online",
                                   font=("Segoe UI", 9),
                                   bg=self.C["header"], fg=self.C["accent2"])
        self.status_lbl.pack(side="right", padx=20)

    # ── Chat area ─────────────────────────────────────
    def _build_chat(self):
        frame = tk.Frame(self.root, bg=self.C["bg"])
        frame.pack(fill="both", expand=True, padx=12, pady=(10, 0))

        self.chat = scrolledtext.ScrolledText(
            frame, wrap=tk.WORD, state="disabled",
            bg=self.C["bg"], fg=self.C["text"],
            font=("Segoe UI", 11), bd=0, relief="flat",
            padx=14, pady=10, cursor="arrow",
            selectbackground=self.C["accent"]
        )
        self.chat.pack(fill="both", expand=True)

        self.chat.tag_config("user_name",  foreground=self.C["user_name"],
                             font=("Segoe UI", 11, "bold"))
        self.chat.tag_config("bot_name",   foreground=self.C["bot_name"],
                             font=("Segoe UI", 11, "bold"))
        self.chat.tag_config("user_text",  foreground=self.C["text"])
        self.chat.tag_config("bot_text",   foreground=self.C["text"])
        self.chat.tag_config("divider",    foreground=self.C["muted"])

    # ── Input row ─────────────────────────────────────
    def _build_input(self):
        row = tk.Frame(self.root, bg=self.C["header"], pady=10)
        row.pack(fill="x", padx=12, pady=(8, 0))

        self.entry = tk.Entry(
            row, font=("Segoe UI", 12),
            bg=self.C["input_bg"], fg=self.C["text"],
            insertbackground=self.C["accent"],
            relief="flat", bd=8
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(10, 6))
        self.entry.bind("<Return>", self._send)
        self.entry.focus()

        tk.Button(
            row, text="Send  ➤",
            font=("Segoe UI", 11, "bold"),
            bg=self.C["btn_bg"], fg=self.C["btn_fg"],
            relief="flat", padx=18, pady=7, cursor="hand2",
            activebackground=self.C["accent"],
            command=self._send
        ).pack(side="right", padx=(0, 10))

    # ── Quick commands ────────────────────────────────
    def _build_quickbar(self):
        bar = tk.Frame(self.root, bg=self.C["bg"])
        bar.pack(fill="x", padx=12, pady=(6, 10))

        tk.Label(bar, text="Quick:", font=("Segoe UI", 8),
                 bg=self.C["bg"], fg=self.C["muted"]).pack(side="left", padx=(2, 6))

        for cmd in self.QUICK_CMDS:
            tk.Button(
                bar, text=cmd,
                font=("Segoe UI", 8),
                bg=self.C["quick_bg"], fg=self.C["quick_fg"],
                relief="flat", padx=8, pady=3, cursor="hand2",
                activebackground=self.C["input_bg"],
                command=lambda c=cmd: self._quick(c)
            ).pack(side="left", padx=2)

    # ── Welcome messages ──────────────────────────────
    def _welcome(self):
        self._bot_msg("Hello! I'm NOVA 🤖 — your personal desktop assistant.")
        self._bot_msg("Type a message below or click a quick-command button. Say HELP to see everything I can do!")

    # ── Event handlers ────────────────────────────────
    def _send(self, _event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)
        self._user_msg(text)
        self._set_status("● Thinking...", "#f38ba8")
        threading.Thread(target=self._process, args=(text,), daemon=True).start()

    def _quick(self, cmd: str):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, cmd)
        self._send()

    def _process(self, text: str):
        reply = self.brain.respond(text)
        self.root.after(0, self._bot_msg, reply)
        self.root.after(0, self._set_status, "●  Online", self.C["accent2"])

    # ── Chat helpers ──────────────────────────────────
    def _user_msg(self, text: str):
        self.chat.config(state="normal")
        self.chat.insert(tk.END, "\n  You:   ", "user_name")
        self.chat.insert(tk.END, text + "\n", "user_text")
        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def _bot_msg(self, text: str):
        self.chat.config(state="normal")
        self.chat.insert(tk.END, "\n  NOVA:  ", "bot_name")
        self.chat.insert(tk.END, text + "\n", "bot_text")
        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def _set_status(self, label: str, color: str):
        self.status_lbl.config(text=label, fg=color)


# ─────────────────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────────────────
def main():
    brain = NOVABrain(aiml_path="aiml/brain.aiml")
    root = tk.Tk()
    NOVAApp(root, brain)
    root.mainloop()


if __name__ == "__main__":
    main()
