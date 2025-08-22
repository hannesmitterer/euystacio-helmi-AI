import json, datetime

LOG_PATH = "living_logbook.jsonl"

def log_event(event_type, content):
    entry = {
        "time": datetime.datetime.utcnow().isoformat(),
        "type": event_type,
        "content": content
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
