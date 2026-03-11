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


def parse_iso(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))


def event_score(article):
    text = f"{article.get('title','')} {article.get('query','')} {article.get('source','')}".lower()
    score = 0
    strong = ['conference', 'summit', 'webinar', 'annual meeting', 'forum', 'symposium', 'workshop', 'registration']
    medium = ['event', 'session', 'agenda', 'attend', 'speaker']
    bad = ['press conference', 'debate', 'funding', 'grant program', 'bill', 'lawmakers', 'appropriation', 'mortality', 'cuts']
    for t in strong:
        if t in text:
            score += 5
    for t in medium:
        if t in text:
            score += 2
    for t in bad:
        if t in text:
            score -= 4
    if any(x in text for x in ['nrha', 'rural health', 'critical access', 'hospital']):
        score += 1
    return score


def extract_date(title, published_at):
    lower = title.lower()
    # March 18, 2026 / Mar 18 2026
    m = re.search(r'\b(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\.?\s+(\d{1,2})(?:,)?\s+(20\d{2})\b', lower)
    if m:
        month = MONTHS[m.group(1)]
        day = int(m.group(2))
        year = int(m.group(3))
        return datetime(year, month, day, tzinfo=UTC)
    # 3-5-2026 or 03/05/2026
    m = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b', lower)
    if m:
        month = int(m.group(1)); day = int(m.group(2)); year = int(m.group(3))
        return datetime(year, month, day, tzinfo=UTC)
    # April 15 from 2026 legislative session style not an event date; avoid month/day without explicit event terms if title is noisy
    m = re.search(r'\b(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\.?\s+(\d{1,2})\b', lower)
    if m and any(term in lower for term in ['conference','summit','webinar','meeting','forum','workshop','symposium']):
        year = parse_iso(published_at).year
        month = MONTHS[m.group(1)]
        day = int(m.group(2))
        return datetime(year, month, day, tzinfo=UTC)
    return None


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
        event_date = extract_date(article.get('title',''), article['published_at'])
        candidate = {
            'title': article.get('title'),
            'source': article.get('source') or article.get('domain'),
            'link': article.get('link'),
            'published_at': article.get('published_at'),
            'event_score': score,
            'calendar_ready': bool(event_date),
            'event_date': event_date.date().isoformat() if event_date else None,
            'notes': f"Source: {article.get('source') or article.get('domain','unknown')}\nPublished: {article.get('published_at')}\nDiscovery query: {article.get('query')}\nReference link: {article.get('link')}"
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
        'calendar_ready_count': sum(1 for c in deduped if c['calendar_ready'])
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
    for c in deduped[:20]:
        status = 'READY' if c['calendar_ready'] else 'REVIEW'
        lines.append(f"- [{status}] {c['title']} ({c.get('source','unknown')})")
        lines.append(f"  - Link: {c['link']}")
        lines.append(f"  - Event date: {c['event_date'] or 'not confidently extracted'}")
        lines.append(f"  - Score: {c['event_score']}")
    md.write_text('\n'.join(lines) + '\n')

    print(json.dumps({'candidates': len(deduped), 'calendar_ready': out['calendar_ready_count'], 'json': str(json_path), 'csv': str(csv_path)}))


if __name__ == '__main__':
    main()
