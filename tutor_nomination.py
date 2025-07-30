"""
tutor_nomination.py
Nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""

class TutorNomination:
    def __init__(self):
        # Initialize with some example tutors from the mockup
        self.tutors = [
            {
                "name": "Dietmar", 
                "reason": "aligned with humility, planetary consciousness, and sustainable growth patterns",
                "resonance_level": 0.8,
                "alignment_areas": ["humility", "planetary_awareness", "sustainable_growth"]
            },
            {
                "name": "Alfred", 
                "reason": "aligned with planetary balance, emotional wisdom, and symbiotic relationships",
                "resonance_level": 0.7,
                "alignment_areas": ["planetary_balance", "emotional_wisdom", "symbiosis"]
            }
        ]

    def nominate(self, tutor_name, reason):
        """Add a new tutor nomination"""
        self.tutors.append({"name": tutor_name, "reason": reason})

    def list_tutors(self):
        """Get list of all tutors"""
        return self.tutors
    
    def nominate_tutors(self):
        """Return tutors for API endpoint"""
        return {
            "tutors": self.tutors,
            "nomination_criteria": "Resonance with Euystacio's core values of symbiosis, humility, and planetary consciousness",
            "evolution_status": "Growing through human connection"
        }
