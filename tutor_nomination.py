"""
tutor_nomination.py - simple top-level tutor nomination fallback

This returns a list of tutors (static or loaded from tutors.json) and
implements a minimal API used by app.py.
"""
import json
import os

TUTORS_PATH = "tutors.json"

class TutorNomination:
    def __init__(self, path=TUTORS_PATH):
        self.path = path
        self._tutors = None
        self._ensure_default()

    def _ensure_default(self):
        if not os.path.exists(self.path):
            default = [
                {"id": "tutor-1", "name": "Seed Tutor", "role": "guide", "resonance": 0.9},
                {"id": "tutor-2", "name": "Community Tutor", "role": "witness", "resonance": 0.7}
            ]
            try:
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(default, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

    def list_tutors(self):
        if self._tutors is None:
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._tutors = json.load(f)
            except Exception:
                self._tutors = []
        return self._tutors

    def nominate(self, criteria=None):
        # Placeholder: return highest resonance tutor
        tutors = self.list_tutors()
        if not tutors:
            return None
        best = max(tutors, key=lambda t: t.get("resonance", 0))
        return best
