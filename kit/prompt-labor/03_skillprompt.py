"""
03 · SKILLPROMPT
Ein Skill ist eine abgelegte Anleitung für eine bestimmte Aufgabe (Ordner skills/).
Das Modell sieht zunächst nur einen KATALOG (Name + Beschreibung jedes Skills).
Erst wenn ein Skill passt, wird seine vollständige Anleitung in den Kontext geladen.
Fachbegriff: "progressive disclosure" – Wissen wird erst bei Bedarf aufgedeckt.

Ausprobieren:
  python 03_skillprompt.py "Mach mir ein Quiz zum Thema Schutzleiter"
  python 03_skillprompt.py "Welche Gefahren gibt es an einer Ständerbohrmaschine?"
  python 03_skillprompt.py "Was ist die Hauptstadt von Frankreich?"   (kein Skill passt)
Eigenen Skill bauen: Ordner skills/mein-skill/ mit einer SKILL.md anlegen.
"""

import json
import os
import sys

from ollama_client import chat, farbig, kopf, lies, zeige_kontext

HIER = os.path.dirname(os.path.abspath(__file__))
SKILL_ORDNER = os.path.join(HIER, "skills")


def lade_skills():
    """Liest alle skills/*/SKILL.md und trennt Kopf (Name, Beschreibung) von Inhalt."""
    skills = {}
    for ordner in sorted(os.listdir(SKILL_ORDNER)):
        pfad = os.path.join(SKILL_ORDNER, ordner, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        _, kopfteil, inhalt = lies(pfad).split("---", 2)
        felder = dict(z.split(":", 1) for z in kopfteil.strip().splitlines() if ":" in z)
        name = felder["name"].strip()
        skills[name] = {"beschreibung": felder["description"].strip(), "inhalt": inhalt.strip()}
    return skills


kopf("03 · Skillprompt")
auftrag = " ".join(sys.argv[1:]) or "Mach mir ein Quiz zum Thema Schutzleiter."
skills = lade_skills()

# Schritt 1: Nur der Katalog ist sichtbar (wenige Zeilen pro Skill)
katalog = "\n".join(f"- {name}: {s['beschreibung']}" for name, s in skills.items())
auswahl_nachrichten = [
    {"role": "system", "content":
        "Du wählst für einen Auftrag den passenden Skill aus diesem Katalog:\n"
        f"{katalog}\n\n"
        'Antworte nur mit JSON: {"skill": "<name>"} oder {"skill": "keiner"}.'},
    {"role": "user", "content": auftrag},
]
zeige_kontext(auswahl_nachrichten, "Schritt 1: Skill-Katalog (nur Kurzbeschreibungen)")
try:
    gewaehlt = json.loads(chat(auswahl_nachrichten, json_modus=True, temperatur=0)).get("skill")
except json.JSONDecodeError:
    gewaehlt = "keiner"
print(farbig(f"\n→ Gewählter Skill: {gewaehlt}", "tool"))

# Schritt 2: Den vollständigen Skill in den Kontext laden – oder ohne Skill antworten
nachrichten = []
if gewaehlt in skills:
    nachrichten.append({"role": "system", "content": skills[gewaehlt]["inhalt"]})
nachrichten.append({"role": "user", "content": auftrag})

zeige_kontext(nachrichten, "Schritt 2: Auftrag + geladene Skill-Anleitung")
print(farbig(chat(nachrichten), "assistant"))
