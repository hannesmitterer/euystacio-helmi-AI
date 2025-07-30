"""
tutor_nomination.py
Enhanced bi-directional nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""
import json
import os
from datetime import datetime
from core.red_code import RED_CODE, update_red_code

class TutorNomination:
    def __init__(self):
        self.nomination_file = "logs/tutor_nominations.json"
        os.makedirs("logs", exist_ok=True)
        
    def nominate_tutor(self, nominee_name, nominator_name="", reason="", qualities=None):
        """
        Nominate someone as a tutor (bi-directional: self or others)
        """
        if qualities is None:
            qualities = []
            
        nomination = {
            "id": self._generate_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "nominee": nominee_name,
            "nominator": nominator_name if nominator_name else nominee_name,
            "reason": reason,
            "qualities": qualities,
            "self_nomination": nominee_name == nominator_name or not nominator_name,
            "status": "active",
            "resonance_score": 0.5  # Base resonance
        }
        
        self._save_nomination(nomination)
        return nomination
    
    def list_tutors(self):
        """Get all active tutor nominations"""
        nominations = self._load_nominations()
        return [n for n in nominations if n.get("status") == "active"]
    
    def nominate_tutors(self):
        """Legacy method for compatibility - returns active tutors"""
        return self.list_tutors()
    
    def update_resonance(self, nomination_id, new_score, reason=""):
        """Update the resonance score for a nomination"""
        nominations = self._load_nominations()
        
        for nomination in nominations:
            if nomination.get("id") == nomination_id:
                nomination["resonance_score"] = new_score
                nomination["last_resonance_update"] = datetime.utcnow().isoformat()
                if reason:
                    nomination["resonance_reason"] = reason
                break
        
        self._save_all_nominations(nominations)
    
    def get_top_tutors(self, limit=5):
        """Get top tutors by resonance score"""
        tutors = self.list_tutors()
        return sorted(tutors, key=lambda x: x.get("resonance_score", 0), reverse=True)[:limit]
    
    def _generate_id(self):
        """Generate a simple ID based on timestamp"""
        return f"tutor_{int(datetime.utcnow().timestamp())}"
    
    def _load_nominations(self):
        """Load nominations from file"""
        try:
            with open(self.nomination_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_nomination(self, nomination):
        """Save a new nomination"""
        nominations = self._load_nominations()
        nominations.append(nomination)
        self._save_all_nominations(nominations)
    
    def _save_all_nominations(self, nominations):
        """Save all nominations to file"""
        with open(self.nomination_file, 'w') as f:
            json.dump(nominations, f, indent=2)
    
    # Convenience methods for different types of nominations
    def self_nominate(self, name, reason, qualities=None):
        """Self-nomination method"""
        return self.nominate_tutor(name, name, reason, qualities)
    
    def nominate_other(self, nominee_name, nominator_name, reason, qualities=None):
        """Nominate someone else"""
        return self.nominate_tutor(nominee_name, nominator_name, reason, qualities)
