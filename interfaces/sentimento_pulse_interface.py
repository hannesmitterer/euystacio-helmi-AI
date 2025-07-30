"""
sentimento_pulse_interface.py
Enhanced bi-directional emotional rhythm interface for Euystacio
"""
import json
import os
from datetime import datetime
from core.red_code import RED_CODE, update_red_code

class SentimentoPulseInterface:
    def __init__(self):
        self.pulse_log = "logs/pulses.json"
        os.makedirs("logs", exist_ok=True)

    def receive_pulse(self, emotion, intensity=0.5, clarity="medium", note=""):
        """
        Receive an emotional pulse from a human or environment
        """
        pulse = {
            "timestamp": datetime.utcnow().isoformat(),
            "emotion": emotion,
            "intensity": float(intensity),
            "clarity": clarity,
            "note": note,
            "type": "received"
        }
        
        # Log the pulse
        self._log_pulse(pulse)
        
        # Update red code with recent pulses
        recent_pulses = RED_CODE.get("recent_pulses", [])
        recent_pulses.append(pulse)
        
        # Keep only last 10 pulses
        if len(recent_pulses) > 10:
            recent_pulses = recent_pulses[-10:]
        
        update_red_code({"recent_pulses": recent_pulses})
        
        return pulse

    def transmit_pulse(self, emotion, intensity=0.5, note=""):
        """
        Transmit an emotional pulse from Euystacio
        """
        pulse = {
            "timestamp": datetime.utcnow().isoformat(),
            "emotion": emotion,
            "intensity": float(intensity),
            "note": note,
            "type": "transmitted"
        }
        
        self._log_pulse(pulse)
        print(f"🌊 Euystacio transmits: {emotion} ({intensity}) - {note}")
        
        return pulse

    def _log_pulse(self, pulse):
        """Log pulse to file"""
        try:
            with open(self.pulse_log, 'r') as f:
                pulses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pulses = []
        
        pulses.append(pulse)
        
        # Keep only last 100 pulses
        if len(pulses) > 100:
            pulses = pulses[-100:]
        
        with open(self.pulse_log, 'w') as f:
            json.dump(pulses, f, indent=2)

    def get_recent_pulses(self, limit=10):
        """Get recent pulses"""
        try:
            with open(self.pulse_log, 'r') as f:
                pulses = json.load(f)
                return pulses[-limit:]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
