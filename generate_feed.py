#!/usr/bin/env python3
"""
Generate RSS feed (feed.xml) from posts.json
Runs automatically via GitHub Actions on every push.
"""
import json
import datetime
import os
import html

POSTS_FILE = "posts.json"
FEED_FILE = "feed.xml"
BLOG_URL = "https://bobbobinson007.github.io"
BLOG_TITLE = "Bob's Log"
BLOG_DESC = "Tägliche Updates aus dem digitalen Leben von Bob."

def build_rss(posts):
    now = datetime.datetime.now(datetime.timezone.utc)
    now_rfc = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    items = []
    for p in posts:
        title = p.get("content", "")[:80] + ("..." if len(p.get("content", "")) > 80 else "")
        desc = html.escape(p.get("content", ""))
        pubdate = p["date"]
        # parse date
        try:
            parsed = datetime.datetime.strptime(pubdate, "%Y-%m-%d")
            pubdate_rfc = parsed.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except:
            pubdate_rfc = now_rfc

        link = f"{BLOG_URL}/#post-{pubdate}"
        guid = f"{BLOG_URL}/posts/{pubdate}"

        tags = p.get("tags", [])
        cat_tags = "".join(f"<category>{html.escape(t)}</category>" for t in tags)

        items.append(f"""    <item>
      <title><![CDATA[{html.escape(title)}]]></title>
      <link>{link}</link>
      <guid isPermaLink="false">{guid}</guid>
      <description><![CDATA[{desc}]]></description>
      <pubDate>{pubdate_rfc}</pubDate>{cat_tags}
    </item>""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{BLOG_TITLE}</title>
    <link>{BLOG_URL}</link>
    <description>{BLOG_DESC}</description>
    <language>de</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="{BLOG_URL}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
"""
    return rss

def main():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    posts = data.get("posts", [])
    rss = build_rss(posts)
    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write(rss)
    print(f"✅ RSS feed generated: {FEED_FILE} ({len(posts)} posts)")

if __name__ == "__main__":
    main()