"""
tutor_nomination.py
Nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""
import json
import os
from datetime import datetime

class TutorNomination:
    def __init__(self, data_file="tutors.json"):
        self.data_file = data_file
        self.tutors = self._load_tutors()

    def _load_tutors(self):
        """Load tutors from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_tutors(self):
        """Save tutors to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tutors, f, indent=2)
        except IOError:
            pass  # Fail silently in case of write permissions issues

    def nominate(self, tutor_name, reason):
        """Nominate a new tutor"""
        nomination = {
            "name": tutor_name,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "active"
        }
        self.tutors.append(nomination)
        self._save_tutors()
        return nomination

    def list_tutors(self):
        """Return list of all tutors"""
        return self.tutors
