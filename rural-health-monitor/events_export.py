#!/usr/bin/env python3
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
CONFIG = json.loads((BASE / "config.json").read_text())
ARTICLES = json.loads((DATA / "articles.json").read_text()) if (DATA / "articles.json").exists() else {"articles": []}
UTC = timezone.utc


def parse_iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def is_event(article):
    text = f"{article.get('query','')} {article.get('title','')}".lower()
    return any(term in text for term in CONFIG.get("event_terms", []))


def main():
    now = datetime.now(UTC)
    cutoff = now - timedelta(days=7)
    events = []
    seen = set()
    for article in ARTICLES.get("articles", []):
        try:
            dt = parse_iso(article["published_at"])
        except Exception:
            continue
        if dt < cutoff or not is_event(article):
            continue
        key = (article.get("title", "").strip().lower(), (article.get("source") or "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        events.append({
            "title": article.get("title"),
            "source": article.get("source") or article.get("domain"),
            "link": article.get("link"),
            "published_at": article.get("published_at"),
            "notes": f"Source: {article.get('source') or article.get('domain','unknown')}\nQuery: {article.get('query','rural health events')}\nLink: {article.get('link')}"
        })

    out = {"generated_at": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"), "events": events[:30]}
    path = DATA / "events.json"
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps({"events": len(out['events']), "path": str(path)}))


if __name__ == "__main__":
    main()
