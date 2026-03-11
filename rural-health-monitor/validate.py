#!/usr/bin/env python3
"""Validation script for rural-health-monitor pipeline."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

def load_json(path, default=None):
    if default is None:
        default = {}
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception as e:
            print(f"⚠️  Failed to load {path}: {e}")
            return default
    return default

def check_articles():
    """Check articles.json."""
    path = DATA / "articles.json"
    data = load_json(path)
    articles = data.get("articles", [])
    print(f"📰 Articles: {len(articles)} stored")
    
    if articles:
        # Check age
        UTC = timezone.utc
        now = datetime.now(UTC)
        cutoff = now - timedelta(days=7)
        fresh = 0
        for a in articles:
            try:
                dt = datetime.fromisoformat(a.get("published_at", "").replace("Z", "+00:00"))
                if dt >= cutoff:
                    fresh += 1
            except:
                pass
        print(f"   Fresh (7d): {fresh}")
    return len(articles) > 0

def check_sources():
    """Check sources.json."""
    path = DATA / "sources.json"
    data = load_json(path)
    sources = data.get("sources", [])
    print(f"🌐 Sources: {len(sources)} discovered")
    return len(sources) > 0

def check_events():
    """Check event_candidates.json."""
    path = DATA / "event_candidates.json"
    data = load_json(path)
    events = data.get("events", [])
    ready = data.get("calendar_ready_count", 0)
    avg_conf = data.get("avg_confidence", 0)
    print(f"📅 Events: {len(events)} candidates, {ready} calendar-ready (avg conf: {avg_conf:.0%})")
    return len(events) > 0

def check_config():
    """Check config.json."""
    path = BASE / "config.json"
    data = load_json(path)
    queries = data.get("queries", [])
    sources = data.get("known_sources", [])
    print(f"⚙️  Config: {len(queries)} queries, {len(sources)} known sources")
    print(f"   Max results/query: {data.get('max_results_per_query', 8)}")
    print(f"   Story age: {data.get('max_story_age_days', 7)} days")
    return len(queries) > 0

def check_calendar_state():
    """Check calendar_state.json."""
    path = DATA / "calendar_state.json"
    data = load_json(path)
    cal_id = data.get("calendar_id")
    events = data.get("events", {})
    print(f"📆 Calendar: {len(events)} events synced")
    if cal_id:
        print(f"   Calendar ID: {cal_id[:20]}...")
    return True

def main():
    print("=" * 50)
    print("Rural Health Monitor - Validation Report")
    print("=" * 50)
    print("")
    
    checks = [
        ("Config", check_config),
        ("Articles", check_articles),
        ("Sources", check_sources),
        ("Events", check_events),
        ("Calendar State", check_calendar_state),
    ]
    
    results = []
    for name, fn in checks:
        try:
            result = fn()
            results.append(result)
            status = "✅" if result else "⚠️ "
            print(f"{status} {name} OK")
        except Exception as e:
            print(f"❌ {name} FAILED: {e}")
            results.append(False)
        print("")
    
    print("=" * 50)
    if all(results):
        print("✅ All checks passed!")
        return 0
    else:
        print("⚠️  Some checks failed - run pipeline to populate data")
        return 1

if __name__ == "__main__":
    sys.exit(main())
