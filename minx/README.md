# minx – Vanilla Survival Server

Interaktive Server-Seite: https://bobbobinson007.github.io/minx/

Inhalt:

- **Beitreten** – Einrichtungs-Guide in 5 Schritten (abhakbar): Discord
  beitreten, Whitelist beantragen, Version 26.2 (keine Mods nötig),
  Luna Client empfohlen, IP eingeben.
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
