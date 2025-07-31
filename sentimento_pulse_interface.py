"""
sentimento_pulse_interface.py
Stub for the emotional rhythm interface – to be evolved into a bi-directional communication layer.
"""
import json
import os
from datetime import datetime

class SentimentoPulseInterface:
    def __init__(self):
        self.pulse_history = []
        self.load_pulse_history()

    def transmit(self, signal):
        """Send emotional rhythm or pulse"""
        print(f"Transmitting pulse: {signal}")
        self.log_pulse("transmit", signal)

    def receive(self):
        """Receive pulse from human or environment"""
        return "neutral"
    
    def receive_pulse(self, emotion, intensity, clarity, note=""):
        """Receive and process an emotional pulse"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "emotion": emotion,
            "intensity": intensity,
            "clarity": clarity,
            "note": note,
            "ai_signature_status": "verified",
            "type": "received"
        }
        
        # Add to history
        self.pulse_history.append(event)
        
        # Save to file
        self.save_pulse(event)
        
        # Process the pulse for resonance and learning
        resonance_data = self.calculate_resonance(event)
        event["resonance_score"] = resonance_data
        
        return event

    def calculate_resonance(self, pulse_event):
        """Calculate resonance based on pulse characteristics"""
        emotion = pulse_event.get("emotion", "").lower()
        intensity = pulse_event.get("intensity", 0.5)
        clarity = pulse_event.get("clarity", "medium")
        
        # Base resonance scoring
        positive_emotions = ["joy", "gratitude", "hope", "wonder", "calm", "love", "peace"]
        constructive_emotions = ["curiosity", "determination", "focus", "creativity"]
        
        base_score = 0.5
        
        if emotion in positive_emotions:
            base_score += 0.3
        elif emotion in constructive_emotions:
            base_score += 0.2
        
        # Adjust for intensity (moderate intensity preferred)
        if 0.3 <= intensity <= 0.7:
            base_score += 0.1
        elif intensity > 0.9:  # Very high intensity might indicate stress
            base_score -= 0.1
        
        # Adjust for clarity
        clarity_multiplier = {
            "high": 1.2,
            "medium": 1.0,
            "low": 0.8
        }
        
        final_score = base_score * clarity_multiplier.get(clarity, 1.0)
        return min(max(final_score, 0.0), 1.0)  # Clamp between 0 and 1

    def load_pulse_history(self):
        """Load pulse history from file"""
        history_file = os.path.join(os.path.dirname(__file__), 'logs', 'pulse_history.json')
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    self.pulse_history = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            self.pulse_history = []

    def save_pulse(self, pulse_event):
        """Save individual pulse to logs"""
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Save to history file
        history_file = os.path.join(logs_dir, 'pulse_history.json')
        try:
            with open(history_file, 'w') as f:
                json.dump(self.pulse_history[-50:], f, indent=2)  # Keep last 50 pulses
        except IOError as e:
            print(f"Warning: Could not save pulse history: {e}")
        
        # Save individual pulse with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        pulse_file = os.path.join(logs_dir, f'pulse_{timestamp}.json')
        try:
            with open(pulse_file, 'w') as f:
                json.dump(pulse_event, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save individual pulse: {e}")

    def log_pulse(self, action, signal):
        """Log pulse transmission"""
        log_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "signal": signal,
            "type": "transmitted"
        }
        self.pulse_history.append(log_event)

    def get_recent_pulses(self, count=10):
        """Get recent pulses for display"""
        return self.pulse_history[-count:] if self.pulse_history else []

    def analyze_pulse_patterns(self):
        """Analyze patterns in pulse data for insights"""
        if not self.pulse_history:
            return {"status": "no_data", "message": "No pulse data available"}
        
        received_pulses = [p for p in self.pulse_history if p.get("type") == "received"]
        
        if not received_pulses:
            return {"status": "no_received_pulses", "message": "No received pulses to analyze"}
        
        # Calculate average resonance
        resonance_scores = [p.get("resonance_score", 0.5) for p in received_pulses]
        avg_resonance = sum(resonance_scores) / len(resonance_scores)
        
        # Most common emotions
        emotions = [p.get("emotion", "unknown") for p in received_pulses]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        most_common_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else "unknown"
        
        return {
            "status": "analysis_complete",
            "total_pulses": len(received_pulses),
            "average_resonance": round(avg_resonance, 3),
            "most_common_emotion": most_common_emotion,
            "emotion_distribution": emotion_counts,
            "recent_trend": "positive" if avg_resonance > 0.6 else "neutral" if avg_resonance > 0.4 else "needs_attention"
        }
