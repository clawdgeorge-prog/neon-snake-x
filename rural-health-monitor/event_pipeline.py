#!/usr/bin/env python3
import csv
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
CONFIG = json.loads((BASE / "config.json").read_text())
ARTICLES = json.loads((DATA / "articles.json").read_text()) if (DATA / "articles.json").exists() else {"articles": []}
UTC = timezone.utc
MONTHS = {
    'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
    'july':7,'august':8,'september':9,'october':10,'november':11,'december':12,
    'jan':1,'feb':2,'mar':3,'apr':4,'jun':6,'jul':7,'aug':8,'sep':9,'sept':9,'oct':10,'nov':11,'dec':12,
}
# Extended date patterns for event extraction
DATE_PATTERNS = [
    # March 18, 2026 / Mar 18 2026 / March 18th, 2026
    (r'\b(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d{2})\b', 3),
    # 3-5-2026 or 03/05/2026 or 3/5/26
    (r'\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b', 3),
    (r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2})\b', 3),
    # April 15 (requires year from published_at or current year)
    (r'\b(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\.?\s+(\d{1,2})(?:st|nd|rd|th)?\b', 2),
    # Day of week + date: "Monday, March 18" or "Monday, March 18th"
    (r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday),?\s+(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\.?\s+(\d{1,2})(?:st|nd|rd|th)?\b', 3),
    # "early April", "late March", "mid-April"
    (r'\b(early|mid|late)\s+(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\b', 2),
    # Q1 2026, Q2 2026
    (r'\b(q[1-4])\s+(20\d{2})\b', 2),
    # "first week of April", "second week of March"
    (r'\b(first|second|third|fourth|fifth)\s+week\s+of\s+(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\b', 3),
]


def parse_iso(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def extract_date_advanced(title, published_at, content=""):
    """Enhanced date extraction with confidence scoring."""
    text = f"{title} {content}".lower()
    published_dt = None
    try:
        published_dt = parse_iso(published_at)
    except Exception:
        pass
    
    # Try each pattern
    for pattern, groups in DATE_PATTERNS:
        m = re.search(pattern, text)
        if not m:
            continue
        
        try:
            if groups == 3:
                # Full date with year
                if m.lastindex >= 3:
                    g1, g2, g3 = m.group(1), m.group(2), m.group(3)
                    # Check if first group is a month
                    if g1.lower() in MONTHS:
                        month = MONTHS[g1.lower()]
                        day = int(g2)
                        year = int(g3) if len(g3) == 4 else 2000 + int(g3)
                    else:
                        # MM/DD/YYYY format
                        month = int(g1)
                        day = int(g2)
                        year = int(g3) if len(g3) == 4 else 2000 + int(g3)
                    return datetime(year, month, day, tzinfo=UTC), 0.9
            elif groups == 2:
                # Month + day only, use published year
                if published_dt:
                    g1, g2 = m.group(1), m.group(2)
                    if g1.lower() in MONTHS:
                        month = MONTHS[g1.lower()]
                        day = int(g2)
                        return datetime(published_dt.year, month, day, tzinfo=UTC), 0.7
                    else:
                        # early/mid/late pattern
                        month = MONTHS[g2.lower()]
                        return datetime(published_dt.year, month, 15, tzinfo=UTC), 0.4
        except (ValueError, AttributeError):
            continue
    
    return None, 0.0


def event_score(article):
    """Enhanced event scoring with confidence weighting."""
    text = f"{article.get('title','')} {article.get('query','')} {article.get('source','')}".lower()
    score = 0
    
    # Strong event indicators
    strong = ['conference', 'summit', 'annual meeting', 'registration open', 'save the date', 'symposium', 'convention']
    medium = ['webinar', 'forum', 'workshop', 'seminar', 'training', 'deadline', 'call for proposals', 'agenda released']
    weak = ['event', 'meeting', 'session', 'call', 'program']
    
    for t in strong:
        if t in text:
            score += 5
    for t in medium:
        if t in text:
            score += 2
    for t in weak:
        if t in text:
            score += 1
    
    # Negative indicators (not actual events)
    bad = ['press conference', 'debate', 'funding opportunity', 'grant program', 'bill', 'lawmakers', 'appropriation', 'mortality', 'cuts', 'study finds', 'report released', 'analysis']
    for t in bad:
        if t in text:
            score -= 3
    
    # Rural health relevance boost
    if any(x in text for x in ['nrha', 'rural health', 'critical access', 'hospital', 'forhp', 'hrsa', 'flex', 'ship']):
        score += 2
    
    return max(0, score)


def calendar_confidence(article):
    """Calculate confidence that an event is calendar-ready."""
    title = article.get('title', '').lower()
    text = f"{title} {article.get('query', '')} {article.get('source', '')}".lower()
    
    confidence = 0.0
    
    # Check high-confidence terms
    high_conf = CONFIG.get("calendar_confidence_terms", {}).get("high", [])
    for term in high_conf:
        if term in text:
            confidence += 0.35
    
    # Check medium-confidence terms
    med_conf = CONFIG.get("calendar_confidence_terms", {}).get("medium", [])
    for term in med_conf:
        if term in text:
            confidence += 0.2
    
    # Check low-confidence terms
    low_conf = CONFIG.get("calendar_confidence_terms", {}).get("low", [])
    for term in low_conf:
        if term in text:
            confidence += 0.1
    
    # Date extraction boost
    event_date, date_conf = extract_date_advanced(article.get('title', ''), article.get('published_at', ''))
    if event_date:
        confidence += date_conf * 0.3
    
    # Penalize if clearly not a calendar event
    if any(t in text for t in ['funding', 'grant', 'deadline', 'report', 'study', 'analysis', 'mortality', 'closure']):
        confidence -= 0.2
    
    return min(1.0, max(0.0, confidence))


def main():
    now = datetime.now(UTC)
    cutoff = now - timedelta(days=14)
    candidates = []
    for article in ARTICLES.get('articles', []):
        try:
            dt = parse_iso(article['published_at'])
        except Exception:
            continue
        if dt < cutoff:
            continue
        score = event_score(article)
        if score < 5:
            continue
        event_date, date_conf = extract_date_advanced(article.get('title',''), article.get('published_at',''))
        confidence = calendar_confidence(article)
        candidate = {
            'title': article.get('title'),
            'source': article.get('source') or article.get('domain'),
            'link': article.get('link'),
            'published_at': article.get('published_at'),
            'event_score': score,
            'calendar_ready': bool(event_date and confidence >= 0.5),
            'calendar_confidence': round(confidence, 2),
            'event_date': event_date.date().isoformat() if event_date else None,
            'notes': f"Source: {article.get('source') or article.get('domain','unknown')}\nPublished: {article.get('published_at')}\nDiscovery query: {article.get('query')}\nReference link: {article.get('link')}\nConfidence: {confidence:.0%}"
        }
        candidates.append(candidate)

    # dedupe by title+source
    deduped = []
    seen = set()
    for c in sorted(candidates, key=lambda x: (x['calendar_ready'], x['event_score'], x['published_at']), reverse=True):
        key = (c['title'].strip().lower(), (c.get('source') or '').strip().lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(c)

    out = {
        'generated_at': now.replace(microsecond=0).isoformat().replace('+00:00','Z'),
        'events': deduped[:40],
        'calendar_ready_count': sum(1 for c in deduped if c['calendar_ready']),
        'avg_confidence': round(sum(c['calendar_confidence'] for c in deduped) / len(deduped), 2) if deduped else 0
    }
    json_path = DATA / 'event_candidates.json'
    json_path.write_text(json.dumps(out, indent=2))

    csv_path = DATA / 'calendar_import.csv'
    with csv_path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Subject','Start Date','All Day Event','Description','Private'])
        writer.writeheader()
        for c in deduped:
            if not c['calendar_ready']:
                continue
            writer.writerow({
                'Subject': c['title'][:200],
                'Start Date': c['event_date'],
                'All Day Event': 'True',
                'Description': c['notes'],
                'Private': 'True'
            })

    md = DATA / 'event_review_queue.md'
    lines = ['# Rural Health Event Review Queue', '']
    lines.append(f"Generated: {now.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Calendar-ready: {out['calendar_ready_count']} | Avg confidence: {out['avg_confidence']:.0%}")
    lines.append("")
    for c in deduped[:25]:
        status = 'READY' if c['calendar_ready'] else f"REVIEW ({c['calendar_confidence']:.0%})"
        lines.append(f"- [{status}] {c['title']} ({c.get('source','unknown')})")
        lines.append(f"  - Link: {c['link']}")
        lines.append(f"  - Event date: {c['event_date'] or 'not extracted'}")
        lines.append(f"  - Score: {c['event_score']}")
    md.write_text('\n'.join(lines) + '\n')

    print(json.dumps({'candidates': len(deduped), 'calendar_ready': out['calendar_ready_count'], 'avg_confidence': out['avg_confidence'], 'json': str(json_path), 'csv': str(csv_path)}))


if __name__ == '__main__':
    main()
