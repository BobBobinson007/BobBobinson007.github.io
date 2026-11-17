# minx – Vanilla Survival Server

Interaktive Server-Seite: https://bobbobinson007.github.io/minx/

Inhalt:

- **Beitreten** – Einrichtungs-Guide als **Overlay-Wizard** (wie das Spieler-
  Dashboard): poppt bei „Kopieren“ neben der IP auf (auch per Nav-Link),
  „Weiter“ führt Schritt für Schritt: Discord & Whitelist → Version
  (**26.2 empfohlen**, alle Versionen 1.8–26.3 möglich) → **Simple Voice
  Chat** (empfohlen) → Server beitreten. Keine Mods nötig.
- **Statistiken** – Spielerstatistiken aus aktueller und alter Welt,
  automatisch pro Spieler zusammengeführt. Jeder Spieler bekommt automatisch
  ein persönliches Dashboard: Skin, Kennzahlen, Distanz-Aufschlüsselung,
  Lieblingsblöcke/-Items und Fakten. Animiert, mobil-optimiert, per Link teilbar.
- **Gebäude** – Bildergalerie. Bilder in `galerie/` legen und in
  `daten/galerie.json` eintragen, sie erscheinen automatisch auf der Seite.
- **Regeln** – die Serverregeln.
- **Server-IP** – `minxserver.duckdns.org`, mit Live-Status (online/offline,
  Spielerzahl) und Online-Badge ganz oben im Header (Hover zeigt, wer online ist).

## Daten

Die JSON-Dateien in `daten/` werden vom Exporter auf dem Server erzeugt
(`/home/ansible/Tools/scripts/minx_page_export.py`) und automatisch gepusht.
Nur freigegebene Felder, keine Koordinaten, keine IPs. Details: SCHNITTSTELLE.md.
