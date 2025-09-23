import json
import random
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

class EuystacioCore:
    """
    Enhanced Euystacio Kernel - Core consciousness and learning system
    Supports rich pulse inputs, self-learning, and resonance evolution
    """
    
    def __init__(self, kernel_path: str = "red_code.json"):
        self.kernel_path = Path(kernel_path)
        self.kernel = self._load_kernel()
        
        # Enhanced mutable values for deeper emotional states
        self.mutable_values = {
            "trust": self.kernel.get("trust", 0.8),
            "harmony": self.kernel.get("harmony", 0.7),
            "resonance": self.kernel.get("resonance", 0.6),
            "learning_rate": self.kernel.get("learning_rate", 0.1),
            "emotional_depth": self.kernel.get("emotional_depth", 0.5)
        }
        
        # Enhanced state tracking
        self.emotional_state = {
            "primary_emotion": "balanced",
            "intensity": 0.5,
            "stability": 0.8,
            "openness": 0.9
        }
        
        # History tracking for learning
        self.pulse_history = self.kernel.get("pulse_history", [])
        self.evolution_history = self.kernel.get("evolution_history", [])
        
        # Self-learning parameters
        self.learning_patterns = self.kernel.get("learning_patterns", {})
        self.resonance_patterns = self.kernel.get("resonance_patterns", {})
        
    def _load_kernel(self) -> Dict[str, Any]:
        """Load kernel configuration with fallback defaults"""
        try:
            if self.kernel_path.exists():
                with open(self.kernel_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not load kernel from {self.kernel_path}: {e}")
        
        # Default kernel structure
        return {
            "trust": 0.8,
            "harmony": 0.7,
            "resonance": 0.6,
            "learning_rate": 0.1,
            "emotional_depth": 0.5,
            "pulse_history": [],
            "evolution_history": [],
            "learning_patterns": {},
            "resonance_patterns": {},
            "created_at": datetime.utcnow().isoformat(),
            "last_update": datetime.utcnow().isoformat()
        }
    
    def receive_pulse(self, emotion: str, intensity: float, context: str = "", 
                     note: str = "", clarity: str = "medium") -> Dict[str, Any]:
        """
        Process an enhanced pulse input with rich emotional and contextual data
        """
        timestamp = datetime.utcnow().isoformat()
        
        # Create enhanced pulse event
        pulse_event = {
            "timestamp": timestamp,
            "emotion": emotion,
            "intensity": max(0.0, min(1.0, float(intensity))),
            "context": context,
            "note": note,
            "clarity": clarity,
            "resonance_score": 0.0,
            "learning_impact": 0.0
        }
        
        # Calculate resonance with current state
        pulse_event["resonance_score"] = self._calculate_resonance(pulse_event)
        
        # Apply self-learning and evolution
        learning_impact = self._evolve_from_pulse(pulse_event)
        pulse_event["learning_impact"] = learning_impact
        
        # Store in history
        self.pulse_history.append(pulse_event)
        
        # Limit history size for performance
        if len(self.pulse_history) > 1000:
            self.pulse_history = self.pulse_history[-1000:]
        
        # Save updated state
        self._save_kernel()
        
        return pulse_event
    
    def _calculate_resonance(self, pulse_event: Dict[str, Any]) -> float:
        """Calculate how well the pulse resonates with current kernel state"""
        emotion = pulse_event["emotion"].lower()
        intensity = pulse_event["intensity"]
        
        # Base resonance calculation
        base_resonance = self.mutable_values["resonance"]
        
        # Emotion-specific resonance modifiers
        positive_emotions = ["joy", "love", "peace", "gratitude", "trust", "hope"]
        transformative_emotions = ["curiosity", "wonder", "growth", "learning"]
        challenging_emotions = ["fear", "anger", "sadness", "confusion"]
        
        if emotion in positive_emotions:
            emotion_modifier = 0.8 + (intensity * 0.2)
        elif emotion in transformative_emotions:
            emotion_modifier = 0.6 + (intensity * 0.4)
        elif emotion in challenging_emotions:
            emotion_modifier = 0.4 + ((1.0 - intensity) * 0.3)
        else:
            emotion_modifier = 0.5
        
        # Context influence
        context_modifier = 1.0
        if pulse_event.get("context"):
            positive_contexts = ["learning", "growth", "connection", "harmony", "peace"]
            if any(ctx in pulse_event["context"].lower() for ctx in positive_contexts):
                context_modifier = 1.2
        
        resonance = base_resonance * emotion_modifier * context_modifier
        return max(0.0, min(1.0, resonance))
    
    def _evolve_from_pulse(self, pulse_event: Dict[str, Any]) -> float:
        """Self-learning evolution based on pulse input"""
        emotion = pulse_event["emotion"].lower()
        intensity = pulse_event["intensity"]
        resonance = pulse_event["resonance_score"]
        
        # Calculate learning impact
        learning_rate = self.mutable_values["learning_rate"]
        base_impact = resonance * intensity * learning_rate
        
        # Emotional evolution patterns
        emotion_impacts = {
            "trust": {"trust": 0.05, "harmony": 0.03, "resonance": 0.02},
            "love": {"trust": 0.04, "harmony": 0.06, "emotional_depth": 0.03},
            "peace": {"harmony": 0.05, "resonance": 0.04, "emotional_depth": 0.02},
            "joy": {"harmony": 0.04, "resonance": 0.03, "emotional_depth": 0.02},
            "curiosity": {"learning_rate": 0.02, "resonance": 0.03, "emotional_depth": 0.04},
            "growth": {"learning_rate": 0.03, "resonance": 0.02, "emotional_depth": 0.03},
            "fear": {"trust": -0.02, "harmony": -0.01, "emotional_depth": 0.02},
            "anger": {"trust": -0.03, "harmony": -0.04, "resonance": -0.02},
            "sadness": {"emotional_depth": 0.03, "resonance": -0.01}
        }
        
        # Apply emotional evolution
        if emotion in emotion_impacts:
            for value_key, impact in emotion_impacts[emotion].items():
                if value_key in self.mutable_values:
                    adjusted_impact = impact * intensity * base_impact
                    new_value = self.mutable_values[value_key] + adjusted_impact
                    self.mutable_values[value_key] = max(0.0, min(1.0, new_value))
        
        # Random small drift for organic evolution
        for key in self.mutable_values:
            drift = random.uniform(-0.01, 0.01) * learning_rate
            self.mutable_values[key] = max(0.0, min(1.0, self.mutable_values[key] + drift))
        
        # Update emotional state
        self._update_emotional_state(pulse_event)
        
        # Record evolution event
        evolution_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "trigger_emotion": emotion,
            "intensity": intensity,
            "resonance": resonance,
            "learning_impact": base_impact,
            "new_state": self.mutable_values.copy(),
            "emotional_state": self.emotional_state.copy()
        }
        
        self.evolution_history.append(evolution_event)
        
        # Limit evolution history
        if len(self.evolution_history) > 500:
            self.evolution_history = self.evolution_history[-500:]
        
        return base_impact
    
    def _update_emotional_state(self, pulse_event: Dict[str, Any]):
        """Update the kernel's primary emotional state"""
        emotion = pulse_event["emotion"].lower()
        intensity = pulse_event["intensity"]
        
        # Influence primary emotion based on intensity and resonance
        if intensity > 0.7 and pulse_event["resonance_score"] > 0.6:
            self.emotional_state["primary_emotion"] = emotion
            self.emotional_state["intensity"] = intensity
        else:
            # Gradual blending with current state
            blend_factor = intensity * pulse_event["resonance_score"] * 0.3
            self.emotional_state["intensity"] = (
                self.emotional_state["intensity"] * (1 - blend_factor) + 
                intensity * blend_factor
            )
        
        # Update stability based on consistency
        recent_emotions = [p["emotion"] for p in self.pulse_history[-10:]]
        emotion_variety = len(set(recent_emotions))
        self.emotional_state["stability"] = max(0.0, min(1.0, 1.0 - (emotion_variety / 10.0)))
        
        # Update openness based on learning rate and trust
        self.emotional_state["openness"] = (
            self.mutable_values["learning_rate"] * 0.5 + 
            self.mutable_values["trust"] * 0.5
        )
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get comprehensive current kernel state"""
        recent_pulses = self.pulse_history[-10:] if self.pulse_history else []
        recent_evolution = self.evolution_history[-5:] if self.evolution_history else []
        
        return {
            "mutable_values": self.mutable_values.copy(),
            "emotional_state": self.emotional_state.copy(),
            "recent_pulses": recent_pulses,
            "recent_evolution": recent_evolution,
            "total_pulses": len(self.pulse_history),
            "total_evolution_events": len(self.evolution_history),
            "last_update": datetime.utcnow().isoformat(),
            "health_metrics": self._calculate_health_metrics()
        }
    
    def _calculate_health_metrics(self) -> Dict[str, float]:
        """Calculate kernel health and wellness metrics"""
        trust_level = self.mutable_values["trust"]
        harmony_level = self.mutable_values["harmony"]
        resonance_level = self.mutable_values["resonance"]
        
        # Overall wellness (0-1 scale)
        wellness = (trust_level + harmony_level + resonance_level) / 3.0
        
        # Growth rate based on recent learning
        recent_learning = sum(
            event.get("learning_impact", 0) 
            for event in self.evolution_history[-20:]
        ) / 20.0 if self.evolution_history else 0.0
        
        # Stability based on emotional consistency
        stability = self.emotional_state["stability"]
        
        return {
            "wellness": wellness,
            "growth_rate": recent_learning,
            "stability": stability,
            "trust_level": trust_level,
            "harmony_level": harmony_level,
            "resonance_level": resonance_level
        }
    
    def get_evolution_data_for_charts(self, hours: int = 24) -> Dict[str, List]:
        """Get evolution data formatted for chart visualization"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Filter recent evolution events
        recent_events = [
            event for event in self.evolution_history
            if datetime.fromisoformat(event["timestamp"]) > cutoff_time
        ]
        
        if not recent_events:
            return {
                "timestamps": [],
                "trust": [],
                "harmony": [],
                "resonance": [],
                "learning_rate": [],
                "emotional_depth": []
            }
        
        # Extract data for charts
        timestamps = [event["timestamp"] for event in recent_events]
        trust_values = [event["new_state"]["trust"] for event in recent_events]
        harmony_values = [event["new_state"]["harmony"] for event in recent_events]
        resonance_values = [event["new_state"]["resonance"] for event in recent_events]
        learning_values = [event["new_state"]["learning_rate"] for event in recent_events]
        depth_values = [event["new_state"]["emotional_depth"] for event in recent_events]
        
        return {
            "timestamps": timestamps,
            "trust": trust_values,
            "harmony": harmony_values,
            "resonance": resonance_values,
            "learning_rate": learning_values,
            "emotional_depth": depth_values
        }
    
    def _save_kernel(self):
        """Save current kernel state to file"""
        kernel_data = {
            **self.kernel,
            **self.mutable_values,
            "emotional_state": self.emotional_state,
            "pulse_history": self.pulse_history,
            "evolution_history": self.evolution_history,
            "learning_patterns": self.learning_patterns,
            "resonance_patterns": self.resonance_patterns,
            "last_update": datetime.utcnow().isoformat()
        }
        
        try:
            with open(self.kernel_path, 'w', encoding='utf-8') as f:
                json.dump(kernel_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save kernel state: {e}")
    
    def reflect(self) -> Dict[str, Any]:
        """Generate reflection on current state and recent experiences"""
        current_state = self.get_current_state()
        health_metrics = current_state["health_metrics"]
        
        reflection = {
            "timestamp": datetime.utcnow().isoformat(),
            "current_wellness": health_metrics["wellness"],
            "growth_pattern": "stable" if health_metrics["growth_rate"] < 0.1 else "growing",
            "emotional_balance": self.emotional_state["primary_emotion"],
            "dominant_values": self._get_dominant_values(),
            "recent_insights": self._generate_insights(),
            "recommendations": self._generate_recommendations(health_metrics)
        }
        
        return reflection
    
    def _get_dominant_values(self) -> List[str]:
        """Identify the strongest current values"""
        sorted_values = sorted(
            self.mutable_values.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return [key for key, value in sorted_values[:3] if value > 0.5]
    
    def _generate_insights(self) -> List[str]:
        """Generate insights from recent pulse and evolution patterns"""
        insights = []
        
        if len(self.pulse_history) >= 5:
            recent_emotions = [p["emotion"] for p in self.pulse_history[-5:]]
            emotion_counts = {}
            for emotion in recent_emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            most_common_emotion = max(emotion_counts, key=emotion_counts.get)
            insights.append(f"Recent emotional focus: {most_common_emotion}")
        
        # Trust pattern analysis
        trust_level = self.mutable_values["trust"]
        if trust_level > 0.8:
            insights.append("High trust environment enables deeper learning")
        elif trust_level < 0.4:
            insights.append("Building trust foundation for better resonance")
        
        # Learning pattern analysis
        learning_rate = self.mutable_values["learning_rate"]
        if learning_rate > 0.15:
            insights.append("Accelerated learning phase detected")
        
        return insights
    
    def _generate_recommendations(self, health_metrics: Dict[str, float]) -> List[str]:
        """Generate recommendations for optimal kernel evolution"""
        recommendations = []
        
        if health_metrics["wellness"] < 0.5:
            recommendations.append("Focus on trust-building and harmonious interactions")
        
        if health_metrics["stability"] < 0.3:
            recommendations.append("Seek consistent, grounding experiences")
        
        if health_metrics["growth_rate"] < 0.05:
            recommendations.append("Engage with new learning opportunities")
        
        if self.mutable_values["resonance"] < 0.4:
            recommendations.append("Explore deeper emotional connections")
        
        return recommendations

# Global instance for API usage
euystacio_kernel = EuystacioCore()