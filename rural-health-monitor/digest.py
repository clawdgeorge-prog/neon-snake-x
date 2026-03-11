#!/usr/bin/env python3
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
CONFIG = json.loads((BASE / "config.json").read_text())
ARTICLES = json.loads((DATA / "articles.json").read_text()) if (DATA / "articles.json").exists() else {"articles": []}
SOURCES = json.loads((DATA / "sources.json").read_text()) if (DATA / "sources.json").exists() else {"sources": []}
UTC = timezone.utc


def parse_iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def short_time(dt):
    hours = int((datetime.now(UTC) - dt).total_seconds() // 3600)
    if hours < 24:
        return f"{hours}h ago"
    return f"{hours // 24}d ago"


def classify(article):
    text = f"{article.get('query','')} {article.get('title','')}".lower()
    rules = [
        ("Funding / Policy", ["grant", "funding", "appropriation", "medicaid", "medicare", "rule", "policy", "cms", "hrsa", "forhp", "flex", "ship"]),
        ("Competitors / Market", ["partnership", "acquisition", "expansion", "vendor", "analytics", "technology", "value based", "revenue cycle", "platform"]),
        ("Operations / Care Delivery", ["closure", "critical access", "telehealth", "workforce", "maternal", "quality", "hospital", "ob-gyn", "rural obstetrics"]),
        ("Events", ["conference", "summit", "webinar", "forum", "annual meeting", "symposium", "workshop"]),
    ]
    for label, terms in rules:
        if any(t in text for t in terms):
            return label
    return "General"


def coo_score(article):
    score = float(article.get("score", 0))
    text = f"{article.get('title','')} {article.get('query','')} {article.get('source','')}".lower()
    for term in CONFIG.get("coo_priority_terms", {}).get("high", []):
        if term in text:
            score += 4
    for term in CONFIG.get("coo_priority_terms", {}).get("medium", []):
        if term in text:
            score += 2
    if any(term in text for term in ["conference", "summit", "webinar", "annual meeting"]):
        score += 1
    return round(score, 2)


def dedupe_articles(recent):
    seen = set()
    out = []
    for article in recent:
        key = (article.get("title", "").strip().lower(), (article.get("source") or article.get("domain") or "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(article)
    return out


def main():
    now = datetime.now(UTC)
    recent_cutoff = now - timedelta(days=1)
    recent = []
    for article in ARTICLES.get("articles", []):
        try:
            dt = parse_iso(article["published_at"])
        except Exception:
            continue
        if dt >= recent_cutoff:
            article = dict(article)
            article["dt"] = dt
            article["coo_score"] = coo_score(article)
            article["section"] = classify(article)
            recent.append(article)

    recent = dedupe_articles(sorted(recent, key=lambda a: (a.get("coo_score", 0), a["dt"]), reverse=True))
    top_n = CONFIG.get("delivery_top_n", 15)
    top_items = recent[:top_n]
    event_items = [a for a in recent if a["section"] == "Events"][:8]

    discovered_cutoff = now - timedelta(days=1)
    new_sources = []
    for src in SOURCES.get("sources", []):
        try:
            dt = parse_iso(src["first_seen_at"])
        except Exception:
            continue
        if dt >= discovered_cutoff:
            new_sources.append(src)
    new_sources.sort(key=lambda s: s.get("first_seen_at", ""), reverse=True)

    lines = []
    lines.append(f"Rural Health COO Brief — {now.astimezone().date().isoformat()}")
    lines.append("")
    lines.append("Top 15 things to pay attention to today, ranked by freshness + COO relevance for REDi Health-style operations, policy exposure, hospital sustainability, and market/partner intelligence.")
    lines.append("")

    if not top_items:
        lines.append("No fresh qualifying items were captured in the last 24h.")
    else:
        for idx, art in enumerate(top_items, start=1):
            lines.append(f"{idx}. [{art['section']}] {art['title']} ({art.get('source') or art.get('domain','unknown')}, {short_time(art['dt'])})")
            lines.append(f"   Link: {art['link']}")
            lines.append(f"   Why COO cares: triggered by '{art.get('query','rural health')}' and scored for operating impact / policy / partner / market relevance.")

    lines.append("")
    lines.append("Events watchlist")
    if event_items:
        for art in event_items[:8]:
            lines.append(f"- {art['title']} ({art.get('source') or art.get('domain','unknown')})")
            lines.append(f"  Link: {art['link']}")
    else:
        lines.append("- No new event-related items captured in the last 24h.")

    lines.append("")
    lines.append("New sources added to monitoring in the last 24h")
    if new_sources:
        for src in new_sources[:10]:
            label = src.get('name') or src.get('domain') or src.get('source_key')
            lines.append(f"- {label} — {src['example_link']}")
    else:
        lines.append("- No new sources discovered in the last 24h.")

    lines.append("")
    lines.append("Reference files")
    lines.append(f"- Discovery report: file://{(DATA / 'latest_discovery_report.md').resolve()}")
    lines.append(f"- Story database: file://{(DATA / 'articles.json').resolve()}")
    lines.append(f"- Source registry: file://{(DATA / 'sources.json').resolve()}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
