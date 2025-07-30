"""
sentimento_pulse_interface.py
Emotional rhythm interface for bi-directional communication with humans
"""
import json
import os
from datetime import datetime

class SentimentoPulseInterface:
    def __init__(self):
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)

    def transmit(self, signal):
        # Send emotional rhythm or pulse
        print(f"Transmitting pulse: {signal}")

    def receive(self):
        # Receive pulse from human or environment
        return "neutral"
    
    def receive_pulse(self, emotion, intensity, clarity, note=""):
        """Receive and process an emotional pulse from a human"""
        pulse_event = {
            "timestamp": datetime.now().isoformat(),
            "emotion": emotion,
            "intensity": intensity,
            "clarity": clarity,
            "note": note,
            "source": "human_interface"
        }
        
        # Save pulse to logs
        log_filename = f"logs/log_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Load existing log or create new one
        if os.path.exists(log_filename):
            with open(log_filename, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {}
        
        # Add pulse with unique key
        pulse_key = f"pulse_{len(log_data)}"
        log_data[pulse_key] = pulse_event
        
        # Save updated log
        with open(log_filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return pulse_event
