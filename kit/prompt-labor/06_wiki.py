"""
06 · WIKI-PROMPT
Ein Sprachmodell vergisst nach jedem Gespräch alles. Ein Wiki ist sein Langzeitgedächtnis:
Das Modell liest Quellen EINMAL, schreibt das Wichtigste als Wiki-Seiten auf und pflegt
ein Inhaltsverzeichnis (wiki/index.md). Spätere Fragen beantwortet es aus dem Wiki.
Der Wiki-Prompt legt fest, WIE das Wiki gepflegt wird (Aufbau, Benennung, Verlinkung).

Den Wiki-Prompt finden Sie in: prompts/WIKI_PROMPT.md

Ausprobieren (zwei Schritte):
  python 06_wiki.py einlesen                      → liest alle Dateien aus quellen/ ins Wiki
  python 06_wiki.py frage "Warum kommt PSA zuletzt?"  → beantwortet die Frage aus dem Wiki
Eigene Quelle: eine .txt-Datei in quellen/ legen und erneut "einlesen".
"""

import json
import os
import re
import sys

from ollama_client import chat, farbig, kopf, lies, zeige_kontext

HIER = os.path.dirname(os.path.abspath(__file__))
QUELLEN = os.path.join(HIER, "quellen")
WIKI = os.path.join(HIER, "wiki")
INDEX = os.path.join(WIKI, "index.md")
WIKI_PROMPT = lies(os.path.join(HIER, "prompts", "WIKI_PROMPT.md"))


def seiten_im_index():
    return re.findall(r"\[\[([^\]]+)\]\]", lies(INDEX))


def einlesen():
    bekannt = lies(INDEX)
    for datei in sorted(os.listdir(QUELLEN)):
        if not datei.endswith(".txt") or f"(Quelle: {datei})" in bekannt:
            continue  # schon im Wiki – nicht doppelt einlesen
        nachrichten = [
            {"role": "system", "content": WIKI_PROMPT +
                "\nVorhandene Wiki-Seiten: " + (", ".join(seiten_im_index()) or "keine") +
                '\n\nAntworte nur mit JSON: {"seite": "<name>.md", "titel": "...", "inhalt": "<Markdown>"}'},
            {"role": "user", "content": f"Neue Quelle '{datei}':\n\n{lies(os.path.join(QUELLEN, datei))}"},
        ]
        zeige_kontext(nachrichten, f"Einlesen: {datei}")
        try:
            seite = json.loads(chat(nachrichten, json_modus=True, temperatur=0.2))
            name = re.sub(r"[^a-z0-9\-]", "", seite["seite"].lower().removesuffix(".md")) + ".md"
            inhalt, titel = seite["inhalt"], seite["titel"]
        except (json.JSONDecodeError, KeyError, AttributeError):
            print(farbig(f"✘ Antwort zu {datei} war kein gültiges JSON – bitte erneut versuchen.", "tool"))
            continue
        with open(os.path.join(WIKI, name), "w", encoding="utf-8") as f:
            f.write(inhalt.strip() + "\n")
        with open(INDEX, "a", encoding="utf-8") as f:
            f.write(f"- [[{name.removesuffix('.md')}]] {titel} (Quelle: {datei})\n")
        print(farbig(f"✔ Wiki-Seite angelegt: wiki/{name}", "tool"))
    print(farbig("\nAktueller Index:\n", "info") + lies(INDEX))


def frage(text):
    # Schritt 1: Nur der Index wird gezeigt – das Modell wählt passende Seiten
    auswahl = [
        {"role": "system", "content": "Hier ist der Index eines Wikis:\n" + lies(INDEX) +
            '\nWelche Seiten helfen bei der Frage? Antworte nur mit JSON: {"seiten": ["name", ...]}'},
        {"role": "user", "content": text},
    ]
    try:
        gewaehlt = json.loads(chat(auswahl, json_modus=True, temperatur=0)).get("seiten", [])
    except json.JSONDecodeError:
        gewaehlt = []
    gewaehlt = [s.removesuffix(".md") for s in gewaehlt if s.removesuffix(".md") in seiten_im_index()]
    gewaehlt = gewaehlt or seiten_im_index()
    print(farbig(f"→ Geladene Wiki-Seiten: {', '.join(gewaehlt)}", "tool"))

    # Schritt 2: Die gewählten Seiten werden in den Kontext geladen
    seiten = "\n\n".join(lies(os.path.join(WIKI, s + ".md")) for s in gewaehlt)
    nachrichten = [
        {"role": "system", "content":
            "Beantworte die Frage NUR mit dem folgenden Wiki-Wissen. Nenne am Ende die "
            "genutzten Seiten als [[seitenname]]. Steht die Antwort nicht im Wiki, sage das.\n\n"
            + seiten},
        {"role": "user", "content": text},
    ]
    zeige_kontext(nachrichten, "Frage + Wiki-Seiten")
    print(farbig(chat(nachrichten), "assistant"))


kopf("06 · Wiki-Prompt")
if len(sys.argv) >= 2 and sys.argv[1] == "einlesen":
    einlesen()
elif len(sys.argv) >= 3 and sys.argv[1] == "frage":
    if not seiten_im_index():
        sys.exit("Das Wiki ist noch leer. Bitte zuerst:  python 06_wiki.py einlesen")
    frage(" ".join(sys.argv[2:]))
else:
    print(__doc__)
