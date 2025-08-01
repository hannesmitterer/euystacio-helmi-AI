"""
tutor_nomination.py
Nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""
import json
import os
from datetime import datetime

class TutorNomination:
    def __init__(self, tutors_file='tutors.json'):
        self.tutors_file = tutors_file
        self.ensure_tutors_file()

    def ensure_tutors_file(self):
        """Create tutors file if it doesn't exist"""
        if not os.path.exists(self.tutors_file):
            with open(self.tutors_file, 'w') as f:
                json.dump([], f)

    def load_tutors(self):
        """Load tutors from file"""
        try:
            with open(self.tutors_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def save_tutors(self, tutors):
        """Save tutors to file"""
        with open(self.tutors_file, 'w') as f:
            json.dump(tutors, f, indent=2)

    def nominate(self, tutor_name, reason, nominated_by=None):
        """Nominate a new tutor"""
        tutors = self.load_tutors()
        tutor = {
            "id": len(tutors) + 1,
            "name": tutor_name,
            "reason": reason,
            "nominated_by": nominated_by,
            "nominated_at": datetime.now().isoformat(),
            "status": "pending",  # pending, approved, rejected
            "approved_by": None,
            "approved_at": None
        }
        tutors.append(tutor)
        self.save_tutors(tutors)
        return tutor

    def approve_tutor(self, tutor_id, approved_by=None):
        """Approve a tutor nomination (admin only)"""
        tutors = self.load_tutors()
        for tutor in tutors:
            if tutor["id"] == tutor_id:
                tutor["status"] = "approved"
                tutor["approved_by"] = approved_by
                tutor["approved_at"] = datetime.now().isoformat()
                self.save_tutors(tutors)
                return tutor
        return None

    def reject_tutor(self, tutor_id, rejected_by=None):
        """Reject a tutor nomination (admin only)"""
        tutors = self.load_tutors()
        for tutor in tutors:
            if tutor["id"] == tutor_id:
                tutor["status"] = "rejected"
                tutor["rejected_by"] = rejected_by
                tutor["rejected_at"] = datetime.now().isoformat()
                self.save_tutors(tutors)
                return tutor
        return None

    def list_tutors(self, status=None):
        """List tutors, optionally filtered by status"""
        tutors = self.load_tutors()
        if status:
            return [t for t in tutors if t.get("status") == status]
        return tutors

    def get_tutor(self, tutor_id):
        """Get a specific tutor by ID"""
        tutors = self.load_tutors()
        for tutor in tutors:
            if tutor["id"] == tutor_id:
                return tutor
        return None
