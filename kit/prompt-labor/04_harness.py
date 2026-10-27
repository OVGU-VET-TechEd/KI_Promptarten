"""
04 · HARNESS-PROMPT
Ein Sprachmodell kann von sich aus nur Text erzeugen. Eine "Harness" (engl. Geschirr,
Zaumzeug) ist das Programm DRUMHERUM: Sie gibt dem Modell Werkzeuge (Dateien lesen,
schreiben …), sagt ihm, was es gerade sieht (Datum, Dateien), führt die gewünschten
Werkzeuge aus und meldet das Ergebnis zurück. Diese Datei IST eine Mini-Harness.
Coding-Agenten wie Claude Code, GitHub Copilot (Agent-Modus) oder Cline sind große Harnesses.

Den Harness-Prompt finden Sie in: prompts/HARNESS_PROMPT.md
Ausprobieren:  python 04_harness.py
Eigene Aufgabe: python 04_harness.py "Lies laborauftrag.txt und schreibe 3 Quizfragen in quiz.md"
"""

import datetime
import json
import os
import sys

from ollama_client import chat, farbig, kopf, lies, zeige_kontext

HIER = os.path.dirname(os.path.abspath(__file__))
ORDNER = os.path.join(HIER, "arbeitsordner")
MAX_SCHRITTE = 8  # Sicherheitsgrenze: die Harness entscheidet, wann Schluss ist


def sicherer_pfad(name):
    """Die Harness erlaubt nur Dateien im Arbeitsordner – das Modell kann nicht ausbrechen."""
    return os.path.join(ORDNER, os.path.basename(str(name)))


# ---- Die Werkzeuge: normale Python-Funktionen ------------------------------------
def liste_dateien():
    return ", ".join(sorted(os.listdir(ORDNER))) or "(leer)"


def lies_datei(name):
    pfad = sicherer_pfad(name)
    return lies(pfad) if os.path.isfile(pfad) else f"FEHLER: Datei '{name}' gibt es nicht."


def schreibe_datei(name, inhalt):
    with open(sicherer_pfad(name), "w", encoding="utf-8") as datei:
        datei.write(inhalt)
    return f"OK: {len(inhalt)} Zeichen in '{os.path.basename(name)}' geschrieben."


WERKZEUGE = {
    "liste_dateien": (liste_dateien, 'liste_dateien – zeigt alle Dateien. argumente: {}'),
    "lies_datei": (lies_datei, 'lies_datei – liest eine Datei. argumente: {"name": "x.txt"}'),
    "schreibe_datei": (schreibe_datei,
                       'schreibe_datei – schreibt eine Datei. argumente: {"name": "x.md", "inhalt": "..."}'),
    "fertig": (None, 'fertig – beendet die Aufgabe. argumente: {"zusammenfassung": "..."}'),
}

# ---- Harness-Prompt zusammensetzen ----------------------------------------------
kopf("04 · Harness-Prompt")
aufgabe = " ".join(sys.argv[1:]) or (
    "Lies die Datei laborauftrag.txt und schreibe daraus eine Sicherheits-Checkliste "
    "zum Abhaken (Markdown, '- [ ] ...') in die Datei checkliste.md."
)
harness_prompt = lies(os.path.join(HIER, "prompts", "HARNESS_PROMPT.md")).format(
    datum=datetime.date.today().strftime("%d.%m.%Y"),
    dateien=liste_dateien(),
    werkzeuge="\n".join(f"- {beschreibung}" for _, beschreibung in WERKZEUGE.values()),
)
nachrichten = [
    {"role": "system", "content": harness_prompt},
    {"role": "user", "content": aufgabe},
]
zeige_kontext(nachrichten, "Harness-Prompt + Aufgabe")

# ---- Die Agentenschleife: denken → Werkzeug → Ergebnis → denken … -----------------
for schritt in range(1, MAX_SCHRITTE + 1):
    antwort = chat(nachrichten, json_modus=True, temperatur=0)
    nachrichten.append({"role": "assistant", "content": antwort})
    try:
        aktion = json.loads(antwort)
        name = aktion.get("werkzeug", "")
        argumente = aktion.get("argumente") or {}
        if isinstance(argumente, str):  # kleine Modelle schicken Argumente manchmal als Text
            argumente = json.loads(argumente or "{}")
        if not isinstance(argumente, dict):
            argumente = {}
    except json.JSONDecodeError:
        aktion, name, argumente = {}, "", {}

    print(farbig(f"\nSchritt {schritt} · Modell: {aktion.get('gedanke', '')}", "assistant"))
    print(farbig(f"  → fordert Werkzeug an: {name} {json.dumps(argumente, ensure_ascii=False)[:120]}",
                 "assistant"))

    if name == "fertig":
        print(farbig(f"\n✔ Fertig: {argumente.get('zusammenfassung', '')}", "tool"))
        break
    if name not in WERKZEUGE:
        ergebnis = f"FEHLER: Werkzeug '{name}' gibt es nicht. Erlaubt: {', '.join(WERKZEUGE)}"
    else:
        try:
            ergebnis = WERKZEUGE[name][0](**argumente)
        except TypeError as fehler:
            ergebnis = f"FEHLER: falsche Argumente ({fehler})"

    print(farbig(f"  ← Harness meldet: {ergebnis[:200]}", "tool"))
    nachrichten.append({"role": "user", "content":
                        f"Ergebnis von {name}: {ergebnis}\nWas ist dein nächster Schritt? (nur JSON)"})
else:
    print(farbig(f"\n■ Abbruch nach {MAX_SCHRITTE} Schritten (Sicherheitsgrenze der Harness).", "tool"))

print(farbig("\n→ Schauen Sie in den Ordner arbeitsordner/ – was hat das Modell angelegt?", "info"))
