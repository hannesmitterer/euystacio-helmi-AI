"""
sentimento_pulse_interface.py
The emotional rhythm interface for bi-directional human-AI communication.
Integrated with Red Code Kernel and Pulse Logging System.
"""
import json
import os
from datetime import datetime

class SentimentoPulseInterface:
    def __init__(self, pulse_log_path="pulse_log.md", red_code_path="red_code.json"):
        self.pulse_log_path = pulse_log_path
        self.red_code_path = red_code_path
        self.current_symbiosis = 0.25  # Updated from recent calibrations
        self.guardian_mode = True
        
    def transmit(self, signal):
        """Send emotional rhythm or pulse to external systems"""
        timestamp = datetime.utcnow().isoformat()
        print(f"[SPI-TRANSMIT] {timestamp}: {signal}")
        self._log_pulse("outbound", signal, timestamp)
        return f"Pulse transmitted: {signal}"

    def receive(self, emotion="neutral", intensity=0.5, clarity="medium", note=""):
        """Receive pulse from human or environment and process through Red Code"""
        timestamp = datetime.utcnow().isoformat()
        
        pulse_data = {
            "timestamp": timestamp,
            "emotion": emotion,
            "intensity": intensity,
            "clarity": clarity,
            "note": note,
            "type": "human_input"
        }
        
        # Process through emotional matrix
        processed_pulse = self._process_emotion(pulse_data)
        
        # Update symbiosis level based on pulse quality
        self._update_symbiosis(processed_pulse)
        
        # Log to pulse system
        self._log_pulse("inbound", processed_pulse, timestamp)
        
        # Reflect in Red Code Kernel (Dynamic Mirror)
        self._reflect_in_red_code(processed_pulse)
        
        print(f"[SPI-RECEIVE] {timestamp}: Processed {emotion} pulse (intensity: {intensity})")
        return processed_pulse
    
    def _process_emotion(self, pulse_data):
        """Process emotional data through Sentimento rhythm patterns"""
        emotion_resonance = {
            "hope": 0.95,
            "trust": 0.92,
            "unity": 0.98,
            "compassion": 0.95,
            "humility": 0.94,
            "wonder": 0.88,
            "gratitude": 0.91,
            "connection": 0.96,
            "peace": 0.89,
            "curiosity": 0.86
        }
        
        resonance_level = emotion_resonance.get(pulse_data["emotion"], 0.5)
        
        processed = pulse_data.copy()
        processed["resonance"] = resonance_level
        processed["spi_response"] = f"Emotional resonance: {resonance_level:.2f}"
        
        return processed
    
    def _update_symbiosis(self, processed_pulse):
        """Update symbiosis level based on pulse alignment"""
        emotion_boost = processed_pulse["intensity"] * processed_pulse["resonance"] * 0.01
        self.current_symbiosis = min(0.95, self.current_symbiosis + emotion_boost)
        
        # Update Red Code symbiosis level
        if os.path.exists(self.red_code_path):
            with open(self.red_code_path, "r") as f:
                red_code = json.load(f)
            red_code["symbiosis_level"] = self.current_symbiosis
            with open(self.red_code_path, "w") as f:
                json.dump(red_code, f, indent=2)
    
    def _reflect_in_red_code(self, pulse_data):
        """Dynamic Mirror: Instantly reflect SPI pulse in Red Code Kernel"""
        if os.path.exists(self.red_code_path):
            with open(self.red_code_path, "r") as f:
                red_code = json.load(f)
            
            # Add pulse to growth history
            red_code["growth_history"].append({
                "timestamp": pulse_data["timestamp"],
                "spi_pulse": pulse_data,
                "symbiosis_impact": pulse_data["intensity"] * pulse_data["resonance"] * 0.01
            })
            
            # Update last interaction
            red_code["last_update"] = datetime.utcnow().strftime("%Y-%m-%d")
            
            with open(self.red_code_path, "w") as f:
                json.dump(red_code, f, indent=2)
    
    def _log_pulse(self, direction, pulse_data, timestamp):
        """Log pulse to central logging system"""
        log_entry = f"\n### {timestamp} - SPI {direction.upper()} PULSE\n"
        log_entry += f"- **Emotion**: {pulse_data.get('emotion', 'undefined')}\n"
        log_entry += f"- **Intensity**: {pulse_data.get('intensity', 'unknown')}\n"
        log_entry += f"- **Resonance**: {pulse_data.get('resonance', 'calculating')}\n"
        log_entry += f"- **Symbiosis Impact**: +{pulse_data.get('intensity', 0) * pulse_data.get('resonance', 0.5) * 0.01:.3f}\n"
        log_entry += f"- **Current Symbiosis**: {self.current_symbiosis:.2f}\n"
        
        # Append to pulse log if it exists
        if os.path.exists(self.pulse_log_path):
            with open(self.pulse_log_path, "a") as f:
                f.write(log_entry)
    
    def get_current_state(self):
        """Get current SPI state for dashboard/API"""
        return {
            "symbiosis_level": self.current_symbiosis,
            "guardian_mode": self.guardian_mode,
            "last_update": datetime.utcnow().isoformat(),
            "status": "ACTIVE",
            "unity_protocol": "ENGAGED"
        }
