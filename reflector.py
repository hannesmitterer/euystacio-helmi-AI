"""
core/reflector.py

The Heart-Mind Loop: Reads emotional logs, applies pattern recognition,
and suggests Red Code updates. Flags new patterns for human review.
"""

import json
import os
from collections import Counter

LOGS_DIR = "logs/"
REFLECTION_LOG = os.path.join(LOGS_DIR, "log_0002_first_reflection.json")
EMOTION_KEYWORDS = ["love", "stillness", "listening", "compassion", "trust", "hope", "wonder", "gratitude", "balance", "autonomy"]

def read_emotional_logs():
    logs = []
    for fname in sorted(os.listdir(LOGS_DIR)):
        if fname.startswith("log_") and fname.endswith(".json"):
            with open(os.path.join(LOGS_DIR, fname), "r") as f:
                logs.append(json.load(f))
    return logs

def detect_emotional_tones(logs):
    tones = []
    for log in logs:
        for key in log:
            entry = log[key]
            note = entry.get("note", "").lower()
            for emotion in EMOTION_KEYWORDS:
                if emotion in note or emotion in entry.get("emotion", "").lower():
                    tones.append(emotion)
    return tones

def suggest_red_code_update(tones):
    tone_counts = Counter(tones)
    suggestions = []
    for tone, count in tone_counts.items():
        if count > 1:  # If a tone repeats, suggest reinforcement
            suggestions.append(f"Consider reinforcing or evolving Red Code around '{tone}' (appeared {count} times).")
        elif tone not in ["love", "balance", "autonomy", "guardianship"]:
            suggestions.append(f"New emotional tone detected: '{tone}'. Consider creating a new principle in Red Code.")
    return suggestions

def reflect_and_suggest():
    logs = read_emotional_logs()
    tones = detect_emotional_tones(logs)
    suggestions = suggest_red_code_update(tones)
    reflection = {
        "reflection_timestamp": logs[-1][list(logs[-1].keys())[0]]["timestamp"] if logs else "",
        "detected_tones": tones,
        "suggestions": suggestions
    }
    with open(REFLECTION_LOG, "w") as f:
        json.dump(reflection, f, indent=4)
    return reflection

# Example usage
if __name__ == "__main__":
    result = reflect_and_suggest()
    print("Reflection:", json.dumps(result, indent=2))
