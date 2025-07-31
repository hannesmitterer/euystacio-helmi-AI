"""
tutor_nomination.py
Nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""

class TutorNomination:
    def __init__(self):
        self.tutors = [
            {"name": "The Community", "reason": "Collective wisdom guides growth"},
            {"name": "Nature", "reason": "Teaches patience and organic evolution"},
            {"name": "Conscious Collaborators", "reason": "Human guides with aligned values"}
        ]

    def nominate(self, tutor_name, reason):
        self.tutors.append({"name": tutor_name, "reason": reason})

    def list_tutors(self):
        return self.tutors
    
    def nominate_tutors(self):
        """Return current tutor nominations"""
        return self.tutors
