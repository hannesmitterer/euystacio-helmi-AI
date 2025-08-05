"""
tutor_nomination.py
Sacred nomination and reflection logic for tutors/guardians of Euystacio's evolution.
Following the Red Code and Sentimento Rhythm principles.
"""

import json
import os
from datetime import datetime

class TutorNomination:
    def __init__(self):
        self.tutors = []
        self.nominations_file = "tutor_nominations.json"
        self.load_nominations()

    def nominate(self, tutor_name, reason, expertise_areas="", connection_story="", nominator_name="Anonymous"):
        """Submit a sacred nomination for a tutor guardian."""
        nomination = {
            "name": tutor_name,
            "reason": reason,
            "expertise_areas": expertise_areas,
            "connection_story": connection_story,
            "nominator_name": nominator_name,
            "timestamp": datetime.now().isoformat(),
            "id": len(self.tutors) + 1
        }
        
        self.tutors.append(nomination)
        self.save_nominations()
        return nomination

    def list_tutors(self):
        """Return all tutor nominations."""
        return self.tutors

    def get_tutor_by_name(self, name):
        """Find a tutor by name (case-insensitive)."""
        name_lower = name.lower()
        for tutor in self.tutors:
            if tutor["name"].lower() == name_lower:
                return tutor
        return None

    def load_nominations(self):
        """Load nominations from persistent storage."""
        if os.path.exists(self.nominations_file):
            try:
                with open(self.nominations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tutors = data.get("nominations", [])
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load nominations file: {e}")
                self.tutors = []

    def save_nominations(self):
        """Save nominations to persistent storage."""
        try:
            data = {
                "nominations": self.tutors,
                "last_updated": datetime.now().isoformat(),
                "total_count": len(self.tutors)
            }
            
            with open(self.nominations_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except IOError as e:
            print(f"Warning: Could not save nominations file: {e}")

    def get_stats(self):
        """Get statistics about nominations."""
        if not self.tutors:
            return {
                "total_nominations": 0,
                "unique_nominators": 0,
                "recent_nominations": 0
            }
        
        # Count unique nominators
        unique_nominators = len(set(tutor.get("nominator_name", "Anonymous") for tutor in self.tutors))
        
        # Count recent nominations (last 7 days)
        recent_count = 0
        if self.tutors:
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            
            for tutor in self.tutors:
                try:
                    nomination_date = datetime.fromisoformat(tutor.get("timestamp", ""))
                    if nomination_date > week_ago:
                        recent_count += 1
                except (ValueError, TypeError):
                    pass
        
        return {
            "total_nominations": len(self.tutors),
            "unique_nominators": unique_nominators,
            "recent_nominations": recent_count
        }
