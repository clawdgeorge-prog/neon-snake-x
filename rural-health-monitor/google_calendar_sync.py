#!/usr/bin/env python3
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
SECRETS = Path("/Users/georgeclawd/.openclaw/secrets/google")
TOKEN_PATH = SECRETS / "token.json"
CALENDAR_STATE_PATH = DATA / "calendar_state.json"
EVENTS_PATH = DATA / "event_candidates.json"
CALENDAR_NAME = "Rural Health Events & Intel"
TIMEZONE = "America/Denver"
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]
UTC = timezone.utc


def load_state():
    if CALENDAR_STATE_PATH.exists():
        return json.loads(CALENDAR_STATE_PATH.read_text())
    return {}


def save_state(state):
    CALENDAR_STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True))


def load_events():
    if EVENTS_PATH.exists():
        return json.loads(EVENTS_PATH.read_text())
    return {"events": []}


def get_service():
    if not TOKEN_PATH.exists():
        raise SystemExit(f"Missing token: {TOKEN_PATH}")
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def ensure_calendar(service, state):
    if state.get("calendar_id"):
        try:
            cal = service.calendars().get(calendarId=state["calendar_id"]).execute()
            return cal["id"]
        except Exception:
            pass

    page_token = None
    while True:
        resp = service.calendarList().list(pageToken=page_token).execute()
        for item in resp.get("items", []):
            if item.get("summary") == CALENDAR_NAME:
                state["calendar_id"] = item["id"]
                save_state(state)
                return item["id"]
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    cal = service.calendars().insert(body={
        "summary": CALENDAR_NAME,
        "description": "Tracked rural health conferences, webinars, policy events, and market-relevant happenings for REDi Health COO monitoring.",
        "timeZone": TIMEZONE,
    }).execute()
    state["calendar_id"] = cal["id"]
    save_state(state)
    return cal["id"]


def sync_events(service, calendar_id, state):
    tracked = state.setdefault("events", {})
    payload = load_events()
    added = []
    skipped = []
    low_confidence = []

    for event in payload.get("events", []):
        # Use calendar_confidence if available, otherwise fall back to calendar_ready
        confidence = event.get("calendar_confidence", 0.5 if event.get("calendar_ready") else 0)
        
        # Only sync events with >= 50% confidence
        if confidence < 0.5:
            low_confidence.append(event.get("title"))
            skipped.append(event.get("title"))
            continue
            
        if not event.get("calendar_ready"):
            skipped.append(event.get("title"))
            continue
            
        source_key = f"{event.get('title','').strip().lower()}|{event.get('event_date')}"
        if tracked.get(source_key):
            skipped.append(event.get("title"))
            continue

        date_str = event["event_date"]
        end_date = (datetime.fromisoformat(date_str) + timedelta(days=1)).date().isoformat()
        body = {
            "summary": event["title"],
            "description": event.get("notes", ""),
            "start": {"date": date_str, "timeZone": TIMEZONE},
            "end": {"date": end_date, "timeZone": TIMEZONE},
            "transparency": "transparent",
        }
        created = service.events().insert(calendarId=calendar_id, body=body).execute()
        tracked[source_key] = {
            "google_event_id": created["id"],
            "title": event["title"],
            "event_date": date_str,
            "source": event.get("source"),
            "link": event.get("link"),
            "confidence": confidence,
            "synced_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        }
        added.append(event["title"])

    save_state(state)
    return added, skipped, low_confidence


def main():
    state = load_state()
    service = get_service()
    calendar_id = ensure_calendar(service, state)
    added, skipped, low_confidence = sync_events(service, calendar_id, state)
    print(json.dumps({
        "calendar_id": calendar_id,
        "added": added,
        "skipped": skipped,
        "low_confidence": low_confidence[:10],  # Show first 10 low confidence
        "tracked_total": len(state.get("events", {}))
    }, indent=2))


if __name__ == "__main__":
    main()
