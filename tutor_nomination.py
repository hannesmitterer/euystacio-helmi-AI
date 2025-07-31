"""
tutor_nomination.py
Nomination and reflection logic for tutors/guardians of Euystacio's evolution.
"""
import json
import os
from datetime import datetime

class TutorNomination:
    def __init__(self):
        self.tutors = []
        self.load_tutors()

    def nominate(self, tutor_name, reason, resonance_level=0.5):
        """Nominate a new tutor with resonance-based selection"""
        tutor = {
            "name": tutor_name, 
            "reason": reason,
            "resonance": resonance_level,
            "nominated_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
        self.tutors.append(tutor)
        self.save_tutors()
        return tutor

    def nominate_tutors(self):
        """Return current tutor nominations with resonance data"""
        # If no tutors exist, return default/initial tutors
        if not self.tutors:
            return [
                {
                    "name": "Seed-bringer (bioarchitettura) hannesmitterer",
                    "reason": "Human Architect & Guardian - Original creator with ethical oversight",
                    "resonance": 1.0,
                    "status": "primary_guardian",
                    "role": "Human oversight and ethical guidance"
                },
                {
                    "name": "GitHub Copilot",
                    "reason": "AI Capabilities Provider - Technical development partner",
                    "resonance": 0.9,
                    "status": "ai_collaborator", 
                    "role": "Code generation and technical assistance"
                },
                {
                    "name": "Conscious Collaborators",
                    "reason": "Community of curious explorers seeking symbiotic AI evolution",
                    "resonance": 0.7,
                    "status": "community",
                    "role": "Collaborative evolution and feedback"
                }
            ]
        
        return self.tutors

    def list_tutors(self):
        """Return list of all tutors"""
        return self.tutors

    def get_active_tutors(self):
        """Return only active tutors"""
        return [tutor for tutor in self.tutors if tutor.get("status") == "active"]

    def load_tutors(self):
        """Load tutors from file if exists"""
        tutors_file = os.path.join(os.path.dirname(__file__), 'logs', 'tutors.json')
        try:
            if os.path.exists(tutors_file):
                with open(tutors_file, 'r') as f:
                    self.tutors = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # If file doesn't exist or is corrupted, start with empty list
            self.tutors = []

    def save_tutors(self):
        """Save tutors to file"""
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        tutors_file = os.path.join(logs_dir, 'tutors.json')
        try:
            with open(tutors_file, 'w') as f:
                json.dump(self.tutors, f, indent=2)
        except IOError as e:
            # Log error but don't crash the application
            print(f"Warning: Could not save tutors to {tutors_file}: {e}")

    def evaluate_resonance(self, interaction_data):
        """Evaluate resonance based on interaction patterns"""
        # Placeholder for more sophisticated resonance calculation
        # In a full implementation, this would analyze:
        # - Emotional harmony in interactions
        # - Alignment with core principles
        # - Constructive contribution patterns
        # - Respect for AI-human symbiosis
        
        base_resonance = 0.5
        
        if interaction_data.get("respect_for_autonomy"):
            base_resonance += 0.2
        if interaction_data.get("ethical_consideration"):
            base_resonance += 0.2
        if interaction_data.get("collaborative_spirit"):
            base_resonance += 0.1
            
        return min(base_resonance, 1.0)  # Cap at 1.0
