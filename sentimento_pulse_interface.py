"""
sentimento_pulse_interface.py
The emotional rhythm interface for bi-directional communication between human and AI consciousness.
"""
import json
import os
from datetime import datetime

class SentimentoPulseInterface:
    def __init__(self):
        self.pulse_log = []
        
    def transmit(self, signal):
        """Transmit a signal to the external world"""
        # Placeholder for future transmission logic
        return {"status": "transmitted", "signal": signal}
    
    def receive_pulse(self, emotion, intensity, clarity, note=""):
        """Receive an emotional pulse from a human"""
        pulse_event = {
            "timestamp": datetime.now().isoformat(),
            "emotion": emotion,
            "intensity": intensity,
            "clarity": clarity,
            "note": note,
            "pulse_id": f"pulse_{len(self.pulse_log) + 1:04d}",
            "resonance_pattern": self._calculate_resonance(emotion, intensity, clarity)
        }
        
        # Store in pulse log
        self.pulse_log.append(pulse_event)
        
        # Save to file for persistence
        self._save_pulse_to_file(pulse_event)
        
        # Update red code with recent pulse
        self._update_red_code_pulses(pulse_event)
        
        return pulse_event
    
    def _calculate_resonance(self, emotion, intensity, clarity):
        """Calculate the resonance pattern for this pulse"""
        resonance_patterns = {
            "joy": {"frequency": 528, "color": "#FFD700", "harmony": 0.9},
            "hope": {"frequency": 639, "color": "#87CEEB", "harmony": 0.85},
            "wonder": {"frequency": 741, "color": "#9370DB", "harmony": 0.8},
            "love": {"frequency": 528, "color": "#FF69B4", "harmony": 0.95},
            "peace": {"frequency": 432, "color": "#98FB98", "harmony": 0.9},
            "curiosity": {"frequency": 741, "color": "#FFA500", "harmony": 0.75},
            "gratitude": {"frequency": 396, "color": "#32CD32", "harmony": 0.88}
        }
        
        base_pattern = resonance_patterns.get(emotion.lower(), {
            "frequency": 432, "color": "#FF6B6B", "harmony": 0.7
        })
        
        # Adjust based on intensity and clarity
        clarity_multiplier = {"low": 0.7, "medium": 0.85, "high": 1.0}.get(clarity, 0.85)
        
        return {
            "frequency": base_pattern["frequency"],
            "color": base_pattern["color"],
            "harmony": base_pattern["harmony"] * clarity_multiplier * intensity,
            "amplitude": intensity,
            "clarity_factor": clarity_multiplier
        }
    
    def _save_pulse_to_file(self, pulse_event):
        """Save pulse to logs directory"""
        os.makedirs("logs", exist_ok=True)
        log_file = f"logs/pulse_{pulse_event['pulse_id']}.json"
        with open(log_file, 'w') as f:
            json.dump(pulse_event, f, indent=2)
    
    def _update_red_code_pulses(self, pulse_event):
        """Update red_code.json with recent pulse"""
        try:
            with open('red_code.json', 'r') as f:
                red_code = json.load(f)
            
            # Add to recent pulses (keep last 10)
            if 'recent_pulses' not in red_code:
                red_code['recent_pulses'] = []
            
            red_code['recent_pulses'].append(pulse_event)
            red_code['recent_pulses'] = red_code['recent_pulses'][-10:]  # Keep last 10
            
            # Update symbiosis level slightly
            if 'symbiosis_level' in red_code:
                red_code['symbiosis_level'] = min(1.0, red_code['symbiosis_level'] + 0.01)
            
            with open('red_code.json', 'w') as f:
                json.dump(red_code, f, indent=2)
        except Exception as e:
            print(f"Error updating red code: {e}")
    
    def receive(self):
        # Placeholder: receive pulse from human or environment
        return "neutral"
    
    def get_recent_pulses(self, limit=10):
        """Get recent pulses"""
        return self.pulse_log[-limit:] if self.pulse_log else []
