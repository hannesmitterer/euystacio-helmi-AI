"""
tutor_nomination.py
Nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""

class TutorNomination:
    def __init__(self):
        # Pre-populate with known tutors from the manifesto
        self.tutors = [
            {"name": "Dietmar", "reason": "aligned with humility, planetary consciousness"},
            {"name": "Alfred", "reason": "resonates with interspecies compassion, planetary balance"}
        ]

    def nominate(self, tutor_name, reason):
        self.tutors.append({"name": tutor_name, "reason": reason})

    def list_tutors(self):
        return self.tutors
    
    def nominate_tutors(self):
        """Alias for API compatibility"""
        return self.list_tutors()
