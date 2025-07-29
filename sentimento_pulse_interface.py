"""
sentimento_pulse_interface.py
Emotional rhythm interface – bi-directional communication layer for Euystacio
"""
import json
from datetime import datetime
import os

class SentimentoPulseInterface:
    def __init__(self):
        self.pulse_counter = 0

    def transmit(self, signal):
        # Send emotional rhythm or pulse
        print(f"Transmitting pulse: {signal}")

    def receive(self):
        # Receive pulse from human or environment
        return "neutral"
    
    def receive_pulse(self, emotion, intensity, clarity, note):
        """
        Receive and process a pulse from human interaction
        """
        self.pulse_counter += 1
        pulse_event = {
            "pulse_id": f"PULSE-{self.pulse_counter:04d}",
            "timestamp": datetime.utcnow().isoformat(),
            "emotion": emotion,
            "intensity": intensity,
            "clarity": clarity,
            "note": note,
            "resonance": intensity * 0.8,  # Simple resonance calculation
            "category": "human_interaction",
            "trigger": "direct_input",
            "action": f"received_{emotion}_pulse",
            "effect": f"resonance_shift_{intensity}"
        }
        
        # Log the pulse
        os.makedirs("logs", exist_ok=True)
        log_filename = f"logs/log_{datetime.utcnow().strftime('%Y%m%d')}.json"
        
        if os.path.exists(log_filename):
            with open(log_filename, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {}
        
        log_data[pulse_event["pulse_id"]] = pulse_event
        
        with open(log_filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return pulse_event
