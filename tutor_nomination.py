"""
tutor_nomination.py
Nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""

class TutorNomination:
    def __init__(self):
        self.tutors = [
            {"name": "Dietmar", "reason": "aligned with humility, planetary wisdom"},
            {"name": "Alfred", "reason": "resonates with interspecies compassion"},
        ]

    def nominate(self, tutor_name, reason):
        self.tutors.append({"name": tutor_name, "reason": reason})

    def list_tutors(self):
        return self.tutors
    
    def nominate_tutors(self):
        """Return current tutor nominations (used by app.py)"""
        return self.tutors
