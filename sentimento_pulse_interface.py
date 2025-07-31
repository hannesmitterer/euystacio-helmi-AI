"""
sentimento_pulse_interface.py
The emotional rhythm interface – a bi-directional communication layer.
"""
import json
import os
from datetime import datetime

class SentimentoPulseInterface:
    def __init__(self):
        self.pulse_log = "logs/pulses.json"
        os.makedirs("logs", exist_ok=True)

    def transmit(self, signal):
        # Send emotional rhythm or pulse
        print(f"Transmitting pulse: {signal}")
        return signal

    def receive(self):
        # Receive pulse from human or environment
        return "neutral"
    
    def receive_pulse(self, emotion, intensity, clarity, note=""):
        """Receive and log an emotional pulse from a human"""
        pulse_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "emotion": emotion,
            "intensity": intensity,
            "clarity": clarity,
            "note": note,
            "type": "human_pulse"
        }
        
        # Log the pulse
        self._log_pulse(pulse_event)
        
        # Update red code with recent pulse
        self._update_red_code_pulses(pulse_event)
        
        return pulse_event
    
    def _log_pulse(self, pulse_event):
        """Log pulse to file"""
        log_filename = f"logs/pulse_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_filename, 'w') as f:
            json.dump(pulse_event, f, indent=2)
    
    def _update_red_code_pulses(self, pulse_event):
        """Update red code with recent pulses"""
        try:
            with open('red_code.json', 'r') as f:
                red_code = json.load(f)
        except:
            red_code = {}
        
        if "recent_pulses" not in red_code:
            red_code["recent_pulses"] = []
        
        red_code["recent_pulses"].append(pulse_event)
        
        # Keep only last 10 pulses
        red_code["recent_pulses"] = red_code["recent_pulses"][-10:]
        
        with open('red_code.json', 'w') as f:
            json.dump(red_code, f, indent=2)
