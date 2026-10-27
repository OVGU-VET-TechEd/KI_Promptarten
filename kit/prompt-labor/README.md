# Prompt-Labor · Starter-Kit

Sechs kleine Experimente, mit denen Sie die Prompt-Arten **selbst ausprobieren** –
mit einem Sprachmodell, das komplett **auf Ihrem eigenen Rechner** läuft (keine Cloud,
keine Daten verlassen den Laptop).

| Datei | Prompt-Art | Was Sie sehen |
|---|---|---|
| `01_interaktionsprompt.py` | Interaktionsprompt | Eine einzelne Nachricht – mehr weiß das Modell nicht. |
| `02_systemprompt.py` | Systemprompt | Dieselbe Frage ohne/mit Systemprompt im Vergleich. |
| `03_skillprompt.py` | Skillprompt | Das Modell wählt aus einem Skill-Katalog und lädt die Anleitung nach. |
| `04_harness.py` | Harness-Prompt | Eine Mini-Harness gibt dem Modell Werkzeuge (Dateien lesen/schreiben). |
| `05_loop.py` | Loop-Prompt | Derselbe Prompt läuft in Runden, bis eine Prüfung bestanden ist. |
| `06_wiki.py` | Wiki-Prompt | Das Modell baut ein Wiki aus Quellen und beantwortet Fragen daraus. |

Alle Prompts liegen als lesbare Textdateien in `prompts/` und `skills/` – **ändern Sie sie!**

---

## 1 · Einmalige Einrichtung (ca. 20 Minuten)

1. **Ollama installieren** – <https://ollama.com/download> (macOS, Windows, Linux).
   Nach der Installation läuft Ollama im Hintergrund (Lama-Symbol in der Menüleiste/Taskleiste).
2. **Modell herunterladen** – im Terminal:
   ```bash
   ollama pull gemma4:e2b
   ```
   Kurztest: `ollama run gemma4:e2b "Sag Hallo auf Deutsch"` (Beenden mit `/bye`).
3. **Python installieren** (Version 3.10 oder neuer) – <https://www.python.org/downloads/>
   Windows: beim Installieren das Häkchen **„Add Python to PATH“** setzen.
   Zusätzliche Pakete braucht das Kit **nicht**.
4. **VS Code installieren** – <https://code.visualstudio.com/>
   und darin die Erweiterung **Python** (Microsoft) – VS Code schlägt sie beim Öffnen vor.
5. **Diesen Ordner öffnen**: VS Code → *Datei → Ordner öffnen …* → `prompt-labor`.

### Welches Modell?

| Modell | Download | Wann? |
|---|---|---|
| `gemma4:e2b` | einige GB | **Standard.** Guter Kompromiss für Laptops mit 8–16 GB RAM. |
| `gemma4:e4b` | größer | Bessere Ergebnisse, braucht mehr Arbeitsspeicher. |
| `llama3.2:3b` | ca. 2 GB | Getestete Alternative, schnell. |
| `gemma3:1b` | ca. 0,8 GB | Für schwache Rechner. Reicht für 01–03, **scheitert meist an 04 (Harness)** – lehrreich! |

Modell wechseln: in `ollama_client.py` die Zeile `MODEL = ... "gemma4:e2b"` ändern
oder im Terminal `export PROMPT_LABOR_MODEL=llama3.2:3b` (Windows PowerShell:
`$env:PROMPT_LABOR_MODEL="llama3.2:3b"`).

## 2 · Experimente starten

**Variante A – ohne Tippen:** In VS Code *Terminal → Aufgabe ausführen … (Run Task)* →
z. B. „02 Systemprompt“ auswählen.

**Variante B – im Terminal** (*Terminal → Neues Terminal*):
```bash
python3 01_interaktionsprompt.py "Erkläre das Ohmsche Gesetz in 3 Sätzen."
python3 02_systemprompt.py
python3 03_skillprompt.py "Welche Gefahren gibt es an einer Ständerbohrmaschine?"
python3 04_harness.py
python3 05_loop.py "Messen mit dem Multimeter"
python3 06_wiki.py einlesen
python3 06_wiki.py frage "Warum kommt die Schutzbrille erst zuletzt?"
```
(Windows: `python` statt `python3`.)

Die farbige Ausgabe zeigt immer **was das Modell zu sehen bekommt**:
violett = System, blau = Nutzer:in, grün = Modell, gelb = Harness/Werkzeuge.

## 3 · Aufgaben zum Weiterdenken

1. **Systemprompt:** Ändern Sie `prompts/SYSTEM_PROMPT.md` so, dass das Modell als
   Ausbilder:in im Metallhandwerk antwortet. Was ändert sich?
2. **Skill:** Legen Sie `skills/betriebsanweisung/SKILL.md` an (Kopf mit `name` und
   `description` wie in den Beispielen). Wird er für passende Aufträge gewählt?
3. **Harness:** Geben Sie `04_harness.py` eine eigene Aufgabe. Wo ist die Grenze
   des kleinen Modells? Was verhindert die Harness (Ordner, Schrittzahl)?
4. **Loop:** Ergänzen Sie in `05_loop.py` → `pruefe()` ein eigenes Kriterium
   (z. B. „muss das Wort *Strombegrenzung* enthalten“).
5. **Wiki:** Legen Sie eine eigene Quelle als `.txt` in `quellen/` und lesen Sie sie ein.
   Prüfen Sie die Wiki-Seite: Hat das Modell etwas erfunden?

## Hinweise

- Kleine lokale Modelle machen **mehr Fehler** als große Cloud-Modelle. Genau daran
  sieht man gut, wofür Systemprompt, Skills, Harness, Loop und Wiki gebraucht werden.
- KI-Ausgaben zu Arbeitsschutz immer mit Primärquellen (Gesetz, DGUV) prüfen.
- Zurücksetzen: Dateien in `arbeitsordner/` (außer `laborauftrag.txt`) und `wiki/`
  (außer `index.md`) löschen, in `wiki/index.md` die Listeneinträge entfernen.

Lizenz: CC BY 4.0 · OVGU Magdeburg, Professur für Ingenieurpädagogik und Didaktik der technischen Bildung
