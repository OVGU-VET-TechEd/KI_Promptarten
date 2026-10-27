"""
02 · SYSTEMPROMPT
Eine Anweisung, die VOR jedem Gespräch steht. Sie legt Rolle, Ton und Regeln fest.
Nutzer:innen sehen sie meist nicht – sie gilt aber für jede Antwort.

Das Skript stellt dieselbe Frage zweimal: ohne und mit Systemprompt.
Den Systemprompt finden (und ändern!) Sie in: prompts/SYSTEM_PROMPT.md
"""

import os
import sys

from ollama_client import chat, farbig, kopf, lies, zeige_kontext

HIER = os.path.dirname(os.path.abspath(__file__))
kopf("02 · Systemprompt")

frage = " ".join(sys.argv[1:]) or "Wie gehe ich sicher mit einem Lötkolben um?"
systemprompt = lies(os.path.join(HIER, "prompts", "SYSTEM_PROMPT.md"))

ohne = [{"role": "user", "content": frage}]
mit = [
    {"role": "system", "content": systemprompt},  # <- steht immer ganz oben
    {"role": "user", "content": frage},
]

for titel, nachrichten in (("A) OHNE Systemprompt", ohne), ("B) MIT Systemprompt", mit)):
    zeige_kontext(nachrichten, titel)
    print(farbig(chat(nachrichten), "assistant"))

print(farbig(
    "\n→ Vergleichen Sie A und B: Länge, Sprache, Hinweise auf Sicherheit.\n"
    "  Ändern Sie prompts/SYSTEM_PROMPT.md (z. B. 'antworte als Reim') und starten Sie neu.",
    "info"))
