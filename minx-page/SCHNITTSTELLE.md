# Schnittstelle: Serverdaten zum Minx Server

## Ziel

Spielerelemente und Statistiken des Minx-Servers sollen automatisiert, aber kontrolliert und sicher auf dieser GitHub-Page landen. Die Page ist statisch (GitHub Pages) – sie kann keine Datenbank abfragen. Daten werden deshalb als JSON-Dateien hierher übertragen und beim Deployment automatisch ausgeliefert.

## Datenquelle

- Aktuelle Welt: `/opt/minecraft/server/world/stats/<uuid>.json` (Statistiken), `advancements/`, `playerdata/`
- Alte Welt: Der Server lief bis zum Wechsel unter einer anderen Welt (`world.kubek`). Bobs Spieler und seine Statistiken existierten dort schon. Diese alten Daten werden separat exportiert und als historische Daten geführt, damit die Leistungen aus der alten Welt nicht verloren gehen.

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

Bilder gehen denselben Weg wie die Daten: lokal ablegen, einchecken, pushen. Für später ist vorgesehen, dass die Seite den Ordner `galerie/` automatisch ausliest – dazu reicht später eine einfache JSON-Liste im Ordner `daten/`.
