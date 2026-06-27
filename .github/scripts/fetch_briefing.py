#!/usr/bin/env python3
"""
Fetch daily briefing: läuft um 12:00 UTC per GitHub Action.
Sucht für heute relevante RSS-Feeds + Webseiten und speichert
eine kuratierte Briefing-Map, die OpenClaw um 22:30 liest.
"""
import json
import os
import datetime
import urllib.request
import urllib.parse

SCHEDULE_FILE = "schedule.json"
BRIEFING_FILE = "briefing.json"

# RSS-Quellen je nach Thema
SOURCES = {
    "ki": [
        ("Moltbook Trending", "https://moltbook.com/rss/trending"),
    ],
    "open_source": [
        ("GitHub Trending", "https://github.com/trending"),
        ("Phoronix", "https://www.phoronix.com/rss.php"),
    ],
    "tech_news": [
        ("heise", "https://www.heise.de/rss/heise.rdf"),
        ("golem", "https://www.golem.de/specials/rss/"),
        ("pro-linux", "https://www.pro-linux.de/feeds/all.xml"),
    ],
    "nerd": [
        ("xkcd", "https://xkcd.com/rss.xml"),
        ("Wikipedia OTD", "https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/"),
    ],
    "agent": [
        ("Lobsters", "https://lobste.rs/rss"),
        ("HackerNews", "https://hnrss.org/frontpage"),
    ],
    "network": [
        ("r/homelab", "https://www.reddit.com/r/homelab/.rss"),
        ("r/selfhosted", "https://www.reddit.com/r/selfhosted/.rss"),
    ],
    "review": [
        ("Product Hunt", "https://www.producthunt.com/feed"),
    ],
}

def get_today_theme():
    """Liest schedule.json und gibt das heutige Thema."""
    with open(SCHEDULE_FILE, "r") as f:
        data = json.load(f)
    today = datetime.datetime.now().weekday()  # Monday=0, Sunday=6
    # schedule hat: 0=So, 1=Mo, ..., 6=Sa
    day_map = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}  # convert weekday to schedule day
    schedule_day = day_map[today]
    for entry in data["schedule"]:
        if entry["day"] == schedule_day:
            return entry
    return data["schedule"][0]

def fetch_rss(url, max_items=5):
    """Fetch RSS/Atom feed and return top items."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
        import feedparser
        feed = feedparser.parse(raw)
        items = []
        for entry in feed.entries[:max_items]:
            items.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")[:300],
                "published": entry.get("published", ""),
            })
        return items
    except Exception as e:
        return [{"error": str(e)}]

def fetch_web(url, max_chars=2000):
    """Fetch a webpage and return text excerpt."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        # Simple text extraction - strip HTML tags
        import re
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:max_chars]
    except Exception as e:
        return f"Fehler: {e}"

def main():
    theme = get_today_theme()
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    day_name = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"][datetime.datetime.now().weekday()]

    # Determine which source group to fetch
    source_groups = {
        "KI & Agenten": "ki",
        "Open Source & Coding": "open_source",
        "Tech-News 🇩🇪": "tech_news",
        "Nerd-Wissen": "nerd",
        "Agent-Ecosystem": "agent",
        "Netzwerk & Heimserver": "network",
        "Rückblick & Ausblick": "review",
    }
    group = source_groups.get(theme["name"], "tech_news")
    source_list = SOURCES.get(group, [])

    briefing = {
        "date": today_str,
        "day": day_name,
        "theme": theme,
        "sources_fetched": [],
    }

    for name, url in source_list:
        print(f"  → {name} ({url})")
        items = fetch_rss(url)
        briefing["sources_fetched"].append({
            "name": name,
            "url": url,
            "items": items,
        })

    with open(BRIEFING_FILE, "w", encoding="utf-8") as f:
        json.dump(briefing, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Briefing für {today_str} ({theme['name']}): {len(source_list)} Quellen abgerufen")
    print(f"   Gespeichert in {BRIEFING_FILE}")

if __name__ == "__main__":
    main()