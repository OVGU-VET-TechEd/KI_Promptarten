# Prompt-Arten verstehen

Interaktive Lerneinheit für Studierende ohne Informatik-Hintergrund:
**Interaktionsprompt · Systemprompt · Skillprompt · Harness-Prompt · Loop-Prompt · Wiki-Prompt**

🌐 **Webseite:** https://ovgu-vet-teched.github.io/KI_Promptarten/

- Zwei Lernniveaus (🌱 Einsteiger:in / 🔧 Fortgeschritten), umschaltbar auf der Seite
- Roter Faden in vier Stufen (Sprechen → Harness → Loops → lernende Agenten), interaktives Schichtenmodell, Schritt-für-Schritt-Simulation, Vergleichstabelle, Zuordnungsquiz
- Übungen für den Chat (z. B. HAWKI) ohne Installation
- **Starter-Kit** [`kit/prompt-labor`](kit/prompt-labor) für VS Code + Ollama (lokales Modell, z. B. `gemma4:e2b`):
  sechs Python-Experimente ohne Zusatzpakete, eines pro Prompt-Art –
  Download: [`downloads/prompt-labor.zip`](downloads/prompt-labor.zip)

Teil des Seminars [Fachdidaktik II – Ingenieurpädagogisches Labor (WiSe 2026/27)](https://ovgu-vet-teched.github.io/IngP-d_Labor_WiSe_2026_2027/).

Zip neu bauen nach Änderungen am Kit:
```bash
cd kit && rm -f ../downloads/prompt-labor.zip && zip -rq ../downloads/prompt-labor.zip prompt-labor -x '*.DS_Store' '*__pycache__*'
```

---
OVGU Magdeburg · Professur für Ingenieurpädagogik und Didaktik der technischen Bildung · Hannes Tegelbeckers
Lizenz: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.de)
