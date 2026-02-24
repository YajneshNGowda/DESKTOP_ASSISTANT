# ✦ NOVA — Neural Omni Virtual Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/AIML-2.0-8A2BE2?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/GUI-Tkinter-4CAF50?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

---

> **NOVA** is a conversational desktop assistant built with **AIML (Artificial Intelligence Markup Language)** and **Python**. It features a sleek dark-mode GUI and can answer questions, open applications, search the web, report time and date, check weather, tell jokes, and more — all powered by AIML pattern matching rules.

---

##  Project Structure

```
nova-desktop-assistant/
│
├── aiml/
│   └── brain.aiml          ←  AIML knowledge base (60+ rules)
│
├── src/
│   ├── assistant.py        ←  GUI application (Tkinter dark-mode)
│   └── cli.py              ←  Terminal / CLI version
│
├── assets/
│   └── (icons, images)     ←  Static assets (optional)
│
├── run.py                  ←  Main entry point
├── requirements.txt        ←  Python dependencies
├── LICENSE                 ←  MIT License
└── README.md               ←  This file
```

---

##  What Is AIML?

**AIML (Artificial Intelligence Markup Language)** is an XML-based scripting language for building conversational agents. It was originally developed as part of the A.L.I.C.E. chatbot project.

NOVA's brain works through **pattern matching**:

```
User Input  →  AIML Pattern Match  →  Template Response  →  Python Execution
```

### Core AIML Elements

| Tag | Purpose |
|-----|---------|
| `<category>` | Defines a single conversation rule |
| `<pattern>` | The input pattern (supports wildcards `*`) |
| `<template>` | The response text or action |
| `<srai>` | Redirects to another pattern (recursive matching) |
| `<star/>` | Inserts the text matched by `*` |

### Example AIML Rule

```xml
<!-- Simple greeting -->
<category>
  <pattern>HELLO</pattern>
  <template>Hello! I'm NOVA. How can I help you today?</template>
</category>

<!-- Wildcard search command -->
<category>
  <pattern>SEARCH FOR *</pattern>
  <template>Searching for "<star/>" on Google! <srai>DO_SEARCH <star/></srai></template>
</category>

<!-- SRAI redirect (alias) -->
<category>
  <pattern>FIND *</pattern>
  <template><srai>SEARCH FOR <star/></srai></template>
</category>
```

When you type *"Find Python tutorials"*, AIML matches `FIND *`, redirects via `<srai>` to `SEARCH FOR *`, and Python intercepts the `DO_SEARCH` tag to open a real browser.

---

##  How NOVA Works — Architecture

```
┌─────────────────────────────────────────────┐
│                  NOVA System                │
│                                             │
│  ┌────────────┐     ┌──────────────────┐    │
│  │  Tkinter   │────▶│   NOVABrain      │    │
│  │  GUI / CLI │     │  (AIML Kernel)   │    │
│  └────────────┘     └────────┬─────────┘    │
│                              │              │
│                    ┌─────────▼──────────┐   │
│                    │  brain.aiml        │   │
│                    │  (Pattern Rules)   │   │
│                    └─────────┬──────────┘   │
│                              │              │
│                    ┌─────────▼──────────┐   │
│                    │  Python Executor   │   │
│                    │  (OS / Web tasks)  │   │
│                    └────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Flow:**
1. User types a message in the GUI or CLI
2. Input is normalized (uppercased) and passed to the AIML kernel
3. The AIML kernel matches the input against patterns in `brain.aiml`
4. The matched template is returned
5. Python checks the response for special command tokens (`LAUNCH_BROWSER`, `GET_WEATHER`, etc.)
6. If a command is detected, the corresponding OS action is executed
7. The final response text is displayed to the user

---

##  Getting Started

### Prerequisites

- Python **3.8** or higher
- `pip` package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/nova-desktop-assistant.git
cd nova-desktop-assistant

# 2. (Recommended) Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run NOVA

```bash
# Launch GUI (default)
python run.py

# Launch CLI (terminal mode)
python run.py --cli
```

---

##  Supported Commands

| What You Say | What NOVA Does |
|---|---|
| `Hello` / `Hi` / `Hey NOVA` | Greets you back |
| `What is your name?` | Tells its name and purpose |
| `Who are you?` | Explains itself |
| `What can you do?` | Lists all features |
| `What time is it?` | Shows the current time |
| `What is the date?` | Shows today's full date |
| `Open browser` | Opens your default web browser |
| `Open notepad` | Opens text editor |
| `Open calculator` | Opens calculator app |
| `Open music` | Opens music player |
| `Search for [topic]` | Searches Google |
| `Google [topic]` | Searches Google |
| `Find [topic]` | Searches Google |
| `What is the weather?` | Opens weather forecast |
| `Tell me a joke` | Tells a joke |
| `Another joke` | Tells another joke |
| `How are you?` | Responds conversationally |
| `Thank you` | Acknowledges thanks |
| `Shutdown` | Prompts system shutdown |
| `Help` | Shows command reference |
| `Bye` / `Goodbye` | Exits gracefully |

---

##  Interface Preview

```
╔══════════════════════════════════════════════════╗
║  ✦ NOVA    Neural Omni Virtual Assistant  ● Online║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  NOVA:  Hello! I'm NOVA 🤖 — your personal...   ║
║                                                  ║
║  You:   What time is it?                         ║
║  NOVA:  The current time is 10:45 AM ⏰           ║
║                                                  ║
║  You:   Search for machine learning              ║
║  NOVA:  Searching Google for 'Machine Learning'  ║
║                                                  ║
╠══════════════════════════════════════════════════╣
║  [ Type a message...              ]  [ Send ➤ ]  ║
║  Quick: [Time][Date][Browser][Joke][Weather][Help]║
╚══════════════════════════════════════════════════╝
```

---

## ➕ Extending NOVA

### Add New Conversation Rules

Open `aiml/brain.aiml` and insert a new `<category>` block:

```xml
<category>
  <pattern>WHAT IS YOUR FAVORITE COLOR</pattern>
  <template>I love deep space blue — just like the cosmos I was named after! 💙</template>
</category>
```

### Add New System Actions

In `src/assistant.py`, find the `_execute_commands()` method and add a new branch:

```python
if text == "OPEN FILES":
    subprocess.Popen("explorer" if platform.system() == "Windows" else "nautilus", shell=True)
    return "Opening file manager... 📂"
```

### Add Multiple AIML Files

```python
# In NOVABrain.__init__(), load multiple AIML files:
self.kernel.learn("aiml/brain.aiml")
self.kernel.learn("aiml/custom.aiml")
self.kernel.learn("aiml/technical.aiml")
```

---

##  Technologies Used

| Technology | Role |
|---|---|
| **Python 3** | Core programming language |
| **AIML 1.0 / 2.0** | NLP pattern-matching engine |
| **python-aiml** | AIML interpreter library |
| **Tkinter** | Desktop GUI framework (built into Python) |
| **webbrowser** | Open URLs and search queries |
| **subprocess** | Launch native OS applications |
| **threading** | Non-blocking UI during response processing |
| **urllib.parse** | URL encoding for search queries |
| **platform** | Cross-platform OS detection |

---

##  Dependencies

```
aiml==1.0.6
python-aiml==0.8.6
```

> **Note:** `tkinter` is part of Python's standard library — no extra install needed.

---


