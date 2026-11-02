# Wir stehen zusammen – Onepager

Einseitige Kampagnenseite für #WirStehenZusammen. Eine Seite (`index.html`), Bilder in `img/`, Schriften in `fonts/`.

**Inhalt:** Kopfbereich mit stummer Teaser-Schleife, Protestversprechen mit Deutschlandkarte und Rangliste, „Es reicht!“, Plan, Mitmachen, Teaser mit Ton, Material, Impressum/Datenschutz (Platzhalter).

## Noch offen
- Teaser: übergangsweise ist „Wir fahren zusammen – Wir streiken zusammen“ von Vimeo eingebettet (oben stumm als Hintergrund, unten mit Ton). Eigenes Video später per Vimeo-ID tauschen (`909677587`)
- `material/WSZ_Flyer.pdf` und Sharepic-Paket ablegen
- Telegram-Link eintragen
- Versprechen-Formular an den Server anbinden (speichert in der Vorschau nichts)
- Impressum und Datenschutz rechtlich klären
- Alle Zahlen, Treffpunkte und Kontakte sind Beispieldaten

## Linkvorschau & Teilen
- Vorschaubild: `og.jpg` (1200 × 630, unter 300 KB halten). Bei eigener Domain `og:url` und `og:image` im `<head>` von `index.html` anpassen.
- Nach einer Zusage erscheinen Teilen-Buttons (WhatsApp, Telegram, Link kopieren, auf dem Handy zusätzlich „Teilen…“).

## Schriften
League Spartan und Figtree liegen in `fonts/` (OFL-Lizenz). Es gibt keine Verbindung zu Google Fonts.

## Öffentlich und Entwurf
- `index.html` = öffentlich: nur Dresden und Magdeburg, Zusagen ab 0 (Zahl erscheint erst ab 1), keine Platzhalter. Treffen/Telegram und Material erscheinen erst, wenn es sie wirklich gibt.
- `entwurf.html` = für das Team: alle Beispieldaten und Platzhalter, gelbe Leiste oben, `noindex`.

## Bearbeiten
Nicht `index.html` oder `entwurf.html` direkt ändern, sondern `_quellen/template.html`. Danach aus dem Repo-Root:

```
python3 _quellen/build.py
```

Das erzeugt beide Fassungen neu (nur Python 3, keine weiteren Pakete).

- **Texte und Abschnitte:** direkt im HTML von `_quellen/template.html`
- **Städte:** Liste `var C=[ … ]` im Script. Öffentlich erscheint eine Stadt nur mit `echt:1`. `tp` (Treffpunkt) und `c` (Zusagen) sind Beispieldaten und werden öffentlich geleert bzw. auf 0 gesetzt.
- **Nur im Entwurf:** alles zwischen `<!--entwurf-->` und `<!--/entwurf-->`
- **Material:** `<!--mat:material/DATEI-->…<!--/mat-->` erscheint öffentlich, sobald die Datei im Repo liegt
- **Platzhalter-Markierungen** (`<span class="ph">…</span>`) werden öffentlich automatisch entfernt

## Fremder Code
`js/vimeo-player.min.js`: offizielle Vimeo-Player-Bibliothek @vimeo/player 2.24.0 (MIT-Lizenz, © Vimeo). Liegt lokal, damit beim Laden keine Verbindung zu einem fremden CDN entsteht.
