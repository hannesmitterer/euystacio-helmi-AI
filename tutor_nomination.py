"""
tutor_nomination.py
Nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""

class TutorNomination:
    def __init__(self):
        self.tutors = []

    def nominate(self, tutor_name, reason):
        self.tutors.append({"name": tutor_name, "reason": reason})

    def list_tutors(self):
        return self.tutors
