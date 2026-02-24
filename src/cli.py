"""
NOVA CLI — Command Line Interface
Run: python src/cli.py
"""

import os
import sys
import aiml
import datetime
import webbrowser
import platform
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BANNER = r"""
 _   _  _____  _   _  ___
| \ | ||  _  || | | |/   |
|  \| || | | || | | |/ /| |
| . ` || | | || | | / /_| |
| |\  |\ \_/ /\ \_/ \___  |
\_| \_/ \___/  \___/    |_/

  Neural Omni Virtual Assistant
  Powered by AIML + Python
  Type 'help' for commands | 'bye' to exit
"""


def load_kernel(aiml_path: str) -> aiml.Kernel:
    k = aiml.Kernel()
    k.learn(aiml_path)
    return k


def handle(kernel: aiml.Kernel, user_input: str) -> str:
    text = user_input.strip().upper()
    resp = kernel.respond(text)

    if text in ("TIME", "WHAT TIME IS IT", "CURRENT TIME", "TELL ME THE TIME"):
        return "Current time: " + datetime.datetime.now().strftime("%I:%M %p")

    if text in ("DATE", "WHAT IS THE DATE", "WHAT IS TODAY", "WHAT DAY IS IT", "TODAY DATE"):
        return "Today: " + datetime.datetime.now().strftime("%A, %B %d, %Y")

    if "LAUNCH_BROWSER" in resp or text == "OPEN BROWSER":
        webbrowser.open("https://www.google.com")
        return "Opening browser..."

    if "GET_WEATHER" in resp or "WEATHER" in text:
        webbrowser.open("https://weather.com")
        return "Opening weather page..."

    for pfx in ("SEARCH FOR ", "SEARCH ", "GOOGLE ", "FIND "):
        if text.startswith(pfx):
            q = text[len(pfx):].strip()
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(q)}")
            return f"Searching for '{q}'..."

    return resp


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    aiml_path = os.path.join(base, "aiml", "brain.aiml")

    if not os.path.exists(aiml_path):
        print(f"[ERROR] AIML file not found: {aiml_path}")
        sys.exit(1)

    kernel = load_kernel(aiml_path)
    print(BANNER)

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "bye", "goodbye"):
                print("NOVA: Goodbye! 👋")
                break
            print(f"NOVA: {handle(kernel, user_input)}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nNOVA: Goodbye! 👋")
            break


if __name__ == "__main__":
    main()
