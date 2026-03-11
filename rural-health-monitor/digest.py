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
    """Enhanced classification with more granular categories."""
    text = f"{article.get('query','')} {article.get('title','')} {article.get('source','')}".lower()
    
    # Priority order matters - check most specific first
    rules = [
        # Funding / Policy - high priority for COO
        ("Funding / Policy", ["grant", "funding", "appropriation", "medicaid", "medicare", "rule", "policy", "cms", "hrsa", "forhp", "flex", "ship", "reimbursement", "budget", "legislation"]),
        # Competitors / Market / M&A
        ("Competitors / Market", ["partnership", "acquisition", "merger", "expansion", "vendor", "analytics", "technology", "value based", "revenue cycle", "platform", "investment", "deal", "contract"]),
        # Hospital Operations / Closures
        ("Hospital Operations", ["closure", "critical access", "telehealth", "workforce", "maternal", "quality", "hospital", "ob-gyn", "rural obstetrics", "maternity", "emergency", "icu", "bed", "staffing"]),
        # Events - conferences, webinars, etc
        ("Events", ["conference", "summit", "webinar", "forum", "annual meeting", "symposium", "workshop", "registration open", "save the date"]),
        # Workforce
        ("Workforce", ["workforce", "staffing", "nurse", "physician", "doctor", "recruitment", "retention", "training", " residency", "nursing"]),
    ]
    for label, terms in rules:
        if any(t in text for t in terms):
            return label
    return "General"


def coo_score(article):
    """Enhanced COO scoring with more nuanced weighting."""
    score = float(article.get("score", 0))
    text = f"{article.get('title','')} {article.get('query','')} {article.get('source','')}".lower()
    
    # High-priority terms (COO critical)
    high_priority = CONFIG.get("coo_priority_terms", {}).get("high", [])
    for term in high_priority:
        if term in text:
            score += 4
    
    # Medium-priority terms
    med_priority = CONFIG.get("coo_priority_terms", {}).get("medium", [])
    for term in med_priority:
        if term in text:
            score += 2
    
    # Event boost
    if any(term in text for term in ["conference", "summit", "webinar", "annual meeting", "registration open", "save the date"]):
        score += 2
    
    # Source authority boost
    authoritative = ["modern healthcare", "becker's hospital review", "fierce healthcare", "kff health news", "health affairs", "north carolina health news", "the daily yonder", "rural health info", "chartis"]
    for src in authoritative:
        if src in text:
            score += 1
    
    return round(score, 2)


def dedupe_articles(recent):
    """Enhanced deduplication with fuzzy matching for similar titles."""
    seen = set()
    out = []
    for article in recent:
        title = article.get("title", "").strip().lower()
        source = (article.get("source") or article.get("domain") or "").strip().lower()
        
        # Exact match
        key = (title, source)
        if key in seen:
            continue
        
        # Fuzzy: check for near-duplicates (title with minor variations)
        is_dup = False
        for seen_title, seen_source in seen:
            if seen_source == source:
                # Simple similarity: if >80% characters match, consider duplicate
                if len(title) > 20 and len(seen_title) > 20:
                    # Count matching words
                    title_words = set(title.split())
                    seen_words = set(seen_title.split())
                    common = title_words & seen_words
                    if len(common) / max(len(title_words), len(seen_words)) > 0.8:
                        is_dup = True
                        break
        
        if is_dup:
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
    
    # Group by category for better digest organization
    categories = ["Funding / Policy", "Competitors / Market", "Hospital Operations", "Events", "Workforce", "General"]
    grouped = {cat: [] for cat in categories}
    for art in recent:
        cat = art.get("section", "General")
        if cat in grouped:
            grouped[cat].append(art)
        else:
            grouped["General"].append(art)

    # Get events separately for dedicated section
    event_items = grouped.get("Events", [])[:8]

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
    lines.append(f"# Rural Health COO Brief — {now.astimezone().date().isoformat()}")
    lines.append("")
    lines.append("Top 15 things to pay attention to today, ranked by freshness + COO relevance for REDi Health-style operations, policy exposure, hospital sustainability, and market/partner intelligence.")
    lines.append("")

    if not top_items:
        lines.append("No fresh qualifying items were captured in the last 24h.")
    else:
        for idx, art in enumerate(top_items, start=1):
            lines.append(f"{idx}. **[{art['section']}]** {art['title']}")
            lines.append(f"   Source: {art.get('source') or art.get('domain','unknown')} | {short_time(art['dt'])}")
            lines.append(f"   Link: {art['link']}")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Events watchlist")
    if event_items:
        for art in event_items:
            lines.append(f"- **{art['title']}**")
            lines.append(f"  Source: {art.get('source') or art.get('domain','unknown')} | {short_time(art['dt'])}")
            lines.append(f"  Link: {art['link']}")
    else:
        lines.append("- No new event-related items captured in the last 24h.")

    lines.append("")
    lines.append("## New sources added to monitoring (last 24h)")
    if new_sources:
        for src in new_sources[:10]:
            label = src.get('name') or src.get('domain') or src.get('source_key')
            lines.append(f"- {label}")
            lines.append(f"  {src.get('example_link', '')}")
    else:
        lines.append("- No new sources discovered in the last 24h.")

    lines.append("")
    lines.append("## Reference")
    lines.append(f"- Discovery report: `{(DATA / 'latest_discovery_report.md').resolve()}`")
    lines.append(f"- Story database: `{(DATA / 'articles.json').resolve()}`")
    lines.append(f"- Source registry: `{(DATA / 'sources.json').resolve()}`")
    lines.append(f"- Event candidates: `{(DATA / 'event_candidates.json').resolve()}`")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
