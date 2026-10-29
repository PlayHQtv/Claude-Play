# PlayHQ Meta-Builds Karussell (Vorlage)

Premium-Karussell im Schwarz-Gold-Glassmorphism-Look fuer @playhqtv (erstes Posting: MW4 Top 4 Meta Builds, 29.10.2026).

- `templates/` – Slide-Vorlagen (Cover `Main`, Build-Slides, Call to Action `Cta`), 1080x1920
- `weapons/` – Waffen-Screenshots aus dem Waffenschmied (Seitenansicht, schwarzer Hintergrund)
- `render.py` – rendert alle Slides nach `out/` (Playwright/Chromium, Fonts: Inter Display 900 + Inter)

Neue Waffe: Screenshot nach `weapons/`, in `BLOBS` eintragen, Template einer Build-Slide kopieren, Name/Nummer/Untertitel aendern, Aufsaetze in `DATA` eintragen, in `ORDER` aufnehmen, `python3 render.py`.
