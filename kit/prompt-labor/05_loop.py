"""
05 · LOOP-PROMPT
Derselbe Prompt wird immer wieder ausgeführt – jedes Mal mit dem aktuellen Stand und
einer Rückmeldung – bis ein Prüfkriterium erfüllt ist oder eine Höchstzahl erreicht ist.
Prinzip: Plan → Ausführen → Prüfen → Verbessern (wie der PDCA-Zyklus im Qualitätsmanagement).

Wichtig: Die Prüfung macht hier ein normales Programm (prüfe()), nicht das Modell selbst.
Sonst würde sich das Modell womöglich selbst "durchwinken".

Den Loop-Prompt finden Sie in: prompts/LOOP_PROMPT.md
Ausprobieren:  python 05_loop.py
Anderes Thema: python 05_loop.py "Messen mit dem Multimeter"
"""

import os
import re
import sys

from ollama_client import chat, farbig, kopf, lies

HIER = os.path.dirname(os.path.abspath(__file__))
MAX_RUNDEN = 5
ZIEL = os.path.join(HIER, "arbeitsordner", "arbeitsblatt.md")


def pruefe(text):
    """Gibt eine Liste der NICHT erfüllten Kriterien zurück (leer = alles erfüllt)."""
    zeilen = [z for z in text.strip().splitlines() if z.strip()]
    maengel = []
    if not zeilen or not zeilen[0].startswith("# "):
        maengel.append("Die erste Zeile muss eine Überschrift mit '# ' sein.")
    # erlaubt "1. …", "### 1. …", "**1.** …" oder "Aufgabe 1: …"
    aufgaben = re.findall(r"^[\s#*]*(?:Aufgabe\s*)?(\d+)[.:)]", text, flags=re.MULTILINE)
    if set(aufgaben) != {"1", "2", "3", "4", "5"}:
        maengel.append(f"Es müssen genau 5 nummerierte Aufgaben sein (Zeilen '1. ' bis '5. '), "
                       f"gefunden: Nummern {', '.join(sorted(set(aufgaben), key=int)) or 'keine'}.")
    if not re.search(r"^## Sicherheitshinweis", text, flags=re.MULTILINE):
        maengel.append("Es fehlt der Abschnitt '## Sicherheitshinweis'.")
    woerter = len(text.split())
    if woerter > 220:
        maengel.append(f"Zu lang: {woerter} Wörter (erlaubt: 220). Kürze jede Aufgabe auf einen Satz.")
    return maengel


kopf("05 · Loop-Prompt")
thema = " ".join(sys.argv[1:]) or "Reihenschaltung von Widerständen"
vorlage = lies(os.path.join(HIER, "prompts", "LOOP_PROMPT.md"))
stand = "(noch leer – erstelle einen ersten Entwurf)"
rueckmeldung = "(erste Runde – noch keine Rückmeldung)"

for runde in range(1, MAX_RUNDEN + 1):
    prompt = vorlage.format(thema=thema, stand=stand, rueckmeldung=rueckmeldung)
    stand = chat([{"role": "user", "content": prompt}], temperatur=0.4).strip()
    stand = re.sub(r"^```(?:markdown)?\s*|\s*```$", "", stand)  # Code-Zäune entfernen
    maengel = pruefe(stand)

    print(farbig(f"\n── Runde {runde} " + "─" * 50, "info"))
    print(farbig(f"   {len(stand.split())} Wörter", "assistant"))
    if not maengel:
        print(farbig("   ✔ Alle Kriterien erfüllt – Schleife endet.", "tool"))
        break
    for m in maengel:
        print(farbig(f"   ✘ {m}", "tool"))
    rueckmeldung = "\n".join(f"- {m}" for m in maengel)
else:
    print(farbig(f"\n■ Nach {MAX_RUNDEN} Runden abgebrochen. Ein Mensch muss nachbessern.", "tool"))

with open(ZIEL, "w", encoding="utf-8") as datei:
    datei.write(stand + "\n")
print(farbig("\nErgebnis (gespeichert in arbeitsordner/arbeitsblatt.md):\n", "info"))
print(farbig(stand, "assistant"))
