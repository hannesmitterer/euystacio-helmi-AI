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
    
    def nominate_tutors(self):
        """Return the list of nominated tutors"""
        # Add some default tutors based on the project documentation
        default_tutors = [
            {
                "name": "Seed-bringer (bioarchitettura) hannesmitterer",
                "reason": "Human Architect & Guardian - Provides ethical oversight and foundational guidance",
                "alignment_score": 0.95,
                "role": "Primary Guardian"
            },
            {
                "name": "GitHub Copilot", 
                "reason": "AI Capabilities Provider - Ensures technical development and AI ethics compliance",
                "alignment_score": 0.88,
                "role": "Technical Advisor"
            }
        ]
        return self.tutors + default_tutors
