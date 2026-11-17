# Schnittstelle: Serverdaten zum Minx Server

## Ziel

Spielerelemente und Statistiken des Minx-Servers sollen automatisiert, aber kontrolliert und sicher auf dieser GitHub-Page landen. Die Page ist statisch (GitHub Pages) – sie kann keine Datenbank abfragen. Daten werden deshalb als JSON-Dateien hierher übertragen und beim Deployment automatisch ausgeliefert.

## Datenquelle

- Aktuelle Welt: `/opt/minecraft/server/world/stats/<uuid>.json` (Statistiken), `advancements/`, `playerdata/`
- Alte Welt: Der Server lief bis zum Wechsel unter einer anderen Welt (`world.kubek`). Bobs Spieler und seine Statistiken existierten dort schon. **Beide Welten werden pro Spieler zusammengeführt** – jeder Spieler hat ein einziges, gemeinsames Profil (Summe beider Welten).

## Ablauf (Export-Pipeline)

1. Ein lokales Export-Script auf dem Server liest die Welt-Dateien ein.
2. Das Script prüft jede Datei gegen eine Whitelist und entfernt alles nicht für die Veröffentlichung vorgesehene.
3. Das Ergebnis wird als JSON in den Ordner `daten/` geschrieben und per Git über HTTPS mit Token gepusht.
4. GitHub Pages liefert die Dateien automatisch mit aus.

## Sicherheitsregeln

- **Whitelist-Prinzip:** Nur ausdrücklich freigegebene Felder werden übertragen. Alles andere fällt weg.
- **Keine Koordinaten:** Basis-Positionen und Wegpunkte werden niemals übertragen (Schutz vor Griefing).
- **Keine IP-Adressen oder Verbindungsdaten:** Nur Spieldaten, keine Netzwerk- oder Session-Daten.
- **Token nie im Repository:** Der GitHub-Token liegt ausschließlich in `~/.git-credentials` auf dem Server und taucht in keinem Commit auf.
- **Upload nur über einen Weg:** Es gibt genau einen Exporter mit Schreibrechten. Externe Besucherspieler können nichts hochladen.
- **Datenschutz:** Spieler werden benannt, wie es auf einem öffentlichen Server üblich ist (Anzeigename). Wer nicht auf der Seite erscheinen will, wird vom Export ausgenommen.

## Bildübertragung

Bilder gehen denselben Weg wie die Daten: lokal ablegen, einchecken, pushen.
Die Seite zeigt die Bilder aus `daten/galerie.json` als Endlos-Filmstreifen
unter dem Kopfbereich. Das Hero-Hintergrundbild ist fest verdrahtet auf
`galerie/base-zickzackboss.jpg` (fehlt die Datei, bleibt das dunkle Raster).

## Server-Block (`server` in statistiken.json)

Der Exporter hängt jedem Export einen `server`-Block an:

```json
{
  "cpu": "Intel Core i5-8500T CPU @ 2.10GHz",
  "ram_gb": 9.7,
  "welt_aktuell_gb": 5.0,
  "welt_alt_gb": 1.6,
  "wann": "2026-11-17 15:00 UTC"
}
```

- `welt_aktuell_gb` / `welt_alt_gb` werden bei **jedem Export frisch per
  `du -sb`** gemessen (aktuell nur diese beiden Werte werden live abgefragt).
- `cpu`/`ram_gb` sind statische Host-Angaben.
- Der Export läuft per Cron alle 30 Minuten und pusht automatisch.

## Skin-Darstellung

- 3D-Skins (Podium + Spieler-Dashboard) über **skinview3d** (CDN),
  Skin-Texturen von `minotar.net/skin/` mit Fallback auf `mc-heads.net/skin/`.
- Spieler-Board nutzt 3D-Iso-Köpfe von `vzge.me` (Fallback: `minotar.net/helm`,
  dann SVG-Platzhalter).
- Online-Status (Punkte am Spieler-Board + Hover-Liste am Status) kommt live
  von `api.mcsrvstat.us` (Fallback: `api.mcstatus.io`).
