"""
01 · INTERAKTIONSPROMPT
Das, was Sie selbst in ein Chatfenster tippen – ein einzelner Auftrag.

Ausprobieren:  python 01_interaktionsprompt.py
Eigenen Auftrag: python 01_interaktionsprompt.py "Erkläre das Ohmsche Gesetz in 3 Sätzen."
"""

import sys

from ollama_client import chat, farbig, kopf, zeige_kontext

kopf("01 · Interaktionsprompt")

auftrag = " ".join(sys.argv[1:]) or (
    "Nenne drei typische Gefährdungen an einem Lötarbeitsplatz in der Berufsschule."
)

nachrichten = [
    {"role": "user", "content": auftrag},  # <- nur EINE Nachricht, sonst nichts
]

zeige_kontext(nachrichten)
print(farbig("\nAntwort des Modells:\n", "info"))
print(farbig(chat(nachrichten), "assistant"))

print(farbig(
    "\n→ Beobachtung: Das Modell weiß nichts über Sie, Ihren Kurs oder Ihre Zielgruppe.\n"
    "  Alles, was es 'weiß', steht in dieser einen Nachricht.", "info"))
