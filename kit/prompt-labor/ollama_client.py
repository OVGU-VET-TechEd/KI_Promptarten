"""
Kleiner Helfer, der mit Ollama spricht – ohne zusätzliche Pakete.

Alle Beispiel-Skripte importieren diese Datei. Sie macht nur zwei Dinge:
  1. eine Nachrichtenliste an das lokale Sprachmodell schicken (chat)
  2. sichtbar machen, WAS genau an das Modell geschickt wird (zeige_kontext)

Welches Modell benutzt wird, steht in MODEL. Sie können es ohne Code-Änderung
umstellen, z. B. im Terminal:   export PROMPT_LABOR_MODEL=gemma3:1b
"""

import json
import os
import sys
import urllib.error
import urllib.request

MODEL = os.environ.get("PROMPT_LABOR_MODEL", "gemma4:e2b")
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
if not OLLAMA_URL.startswith("http"):
    OLLAMA_URL = "http://" + OLLAMA_URL

# Farben für das Terminal (funktionieren in VS Code, macOS, Linux, Windows Terminal)
FARBEN = {
    "system": "\033[95m",     # violett
    "user": "\033[94m",       # blau
    "assistant": "\033[92m",  # grün
    "tool": "\033[93m",       # gelb
    "info": "\033[90m",       # grau
    "ende": "\033[0m",
}


def farbig(text, rolle):
    return f"{FARBEN.get(rolle, '')}{text}{FARBEN['ende']}"


def chat(nachrichten, json_modus=False, temperatur=0.3):
    """Schickt die Nachrichtenliste an Ollama und gibt die Antwort als Text zurück.

    nachrichten: Liste wie [{"role": "system", "content": "..."},
                            {"role": "user", "content": "..."}]
    json_modus:  True zwingt das Modell, gültiges JSON zu antworten.
    """
    daten = {
        "model": MODEL,
        "messages": nachrichten,
        "stream": False,
        "options": {"temperature": temperatur},
    }
    if json_modus:
        daten["format"] = "json"
    anfrage = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=json.dumps(daten).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(anfrage, timeout=600) as antwort:
            return json.loads(antwort.read())["message"]["content"]
    except urllib.error.HTTPError as fehler:
        if fehler.code == 404:
            sys.exit(farbig(
                f"\nModell '{MODEL}' ist nicht installiert.\n"
                f"Bitte im Terminal ausführen:  ollama pull {MODEL}\n", "tool"))
        raise
    except urllib.error.URLError:
        sys.exit(farbig(
            "\nOllama ist nicht erreichbar. Läuft die Ollama-App?\n"
            "Starten Sie Ollama oder führen Sie im Terminal aus:  ollama serve\n", "tool"))


def zeige_kontext(nachrichten, titel="Das bekommt das Modell zu sehen"):
    """Druckt die komplette Nachrichtenliste farbig aus – das 'Kontextfenster'."""
    print(farbig(f"\n┌─ {titel} " + "─" * max(0, 60 - len(titel)), "info"))
    for n in nachrichten:
        print(farbig(f"│ [{n['role'].upper()}]", n["role"]))
        for zeile in n["content"].strip().splitlines():
            print(farbig(f"│   {zeile}", n["role"]))
    print(farbig("└" + "─" * 63, "info"))


def lies(pfad):
    with open(pfad, encoding="utf-8") as datei:
        return datei.read()


def kopf(titel):
    print(farbig("\n" + "═" * 64, "info"))
    print(f"  {titel}   (Modell: {MODEL})")
    print(farbig("═" * 64, "info"))
