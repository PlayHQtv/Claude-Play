# PlayHQ Remotion

Videos für @playhqtv, gebaut mit [Remotion](https://www.remotion.dev) (React).

## Befehle

```bash
npm install
npm run studio   # Vorschau im Browser mit Live-Bearbeitung der Props
npm run render   # rendert out/playhq-intro.mp4
npm run still    # Einzelbild (Frame 60) als PNG
```

## Kompositionen

| ID            | Format              | Länge         | Datei                  |
| ------------- | ------------------- | ------------- | ---------------------- |
| `PlayHQIntro` | 1080×1920 (9:16)    | 5 s @ 30 fps  | `src/PlayHQIntro.tsx`  |

Texte und Farben (`title`, `handle`, `tagline`, `accent`, `accent2`) sind Props und
lassen sich in `src/Root.tsx` oder beim Rendern ändern, z. B.:

```bash
npx remotion render PlayHQIntro out/intro.mp4 --props='{"tagline":"Neue Clips jeden Tag"}'
```

`remotion.config.ts` nutzt in der Cloud-Umgebung das vorinstallierte Chromium.
Lokal lädt Remotion automatisch einen eigenen Browser; alternativ `REMOTION_BROWSER` setzen.
