#!/usr/bin/env python3
"""
Metaplano Emozionale - Emotional Stability Prediction Module
Predicts and prevents emotional instability in human-AI synergy
Part of Phase III - The Symbiosis
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class EmotionalState(Enum):
    """Emotional state categories"""
    STABLE = "stable"
    FLUCTUATING = "fluctuating"
    UNSTABLE = "unstable"
    CRITICAL = "critical"


class StabilityLevel(Enum):
    """Stability level thresholds"""
    EXCELLENT = 90
    GOOD = 80
    MODERATE = 70
    LOW = 60
    CRITICAL = 0


class MetaplanoEmozionale:
    """
    Main class for emotional stability prediction and management
    in human-AI collaborative environments
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Metaplano Emozionale
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or self._default_config()
        self.stability_history = []
        self.prediction_cache = {}
        self.alert_callbacks = []
        
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "prediction_window": 300,  # 5 minutes in seconds
            "history_retention": 3600,  # 1 hour
            "stability_threshold": 80,
            "critical_threshold": 60,
            "alert_enabled": True,
            "adaptive_learning": True
        }
    
    def assess_current_state(self, metrics: Dict) -> Dict:
        """
        Assess current emotional state based on metrics
        
        Args:
            metrics: Dictionary containing current metrics
                - interaction_quality: float (0-100)
                - response_time: float (milliseconds)
                - coherence_score: float (0-1)
                - stress_indicators: int (count)
                
        Returns:
            Dictionary with assessment results
        """
        # Calculate base stability score
        stability_score = self._calculate_stability_score(metrics)
        
        # Determine emotional state
        state = self._determine_state(stability_score)
        
        # Record in history
        self._record_state({
            "timestamp": datetime.now().isoformat(),
            "stability_score": stability_score,
            "state": state.value,
            "metrics": metrics
        })
        
        # Generate assessment
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "stability_score": stability_score,
            "state": state.value,
            "metrics": metrics,
            "recommendations": self._generate_recommendations(stability_score, state)
        }
        
        # Trigger alerts if necessary
        if self.config["alert_enabled"] and state in [EmotionalState.UNSTABLE, EmotionalState.CRITICAL]:
            self._trigger_alert(assessment)
        
        return assessment
    
    def _calculate_stability_score(self, metrics: Dict) -> float:
        """
        Calculate stability score from metrics
        
        Args:
            metrics: Input metrics
            
        Returns:
            Stability score (0-100)
        """
        # Weighted calculation
        weights = {
            "interaction_quality": 0.3,
            "coherence_score": 0.3,
            "response_time": 0.2,
            "stress_indicators": 0.2
        }
        
        # Normalize and weight metrics
        score = 0.0
        
        # Interaction quality (already 0-100)
        if "interaction_quality" in metrics:
            score += metrics["interaction_quality"] * weights["interaction_quality"]
        
        # Coherence score (0-1, convert to 0-100)
        if "coherence_score" in metrics:
            score += metrics["coherence_score"] * 100 * weights["coherence_score"]
        
        # Response time (lower is better, normalize to 0-100)
        if "response_time" in metrics:
            response_score = max(0, 100 - (metrics["response_time"] / 10))
            score += response_score * weights["response_time"]
        
        # Stress indicators (count, inverse scoring)
        if "stress_indicators" in metrics:
            stress_score = max(0, 100 - (metrics["stress_indicators"] * 10))
            score += stress_score * weights["stress_indicators"]
        
        return min(100, max(0, score))
    
    def _determine_state(self, stability_score: float) -> EmotionalState:
        """
        Determine emotional state from stability score
        
        Args:
            stability_score: Current stability score
            
        Returns:
            EmotionalState enum value
        """
        if stability_score >= StabilityLevel.EXCELLENT.value:
            return EmotionalState.STABLE
        elif stability_score >= StabilityLevel.GOOD.value:
            return EmotionalState.STABLE
        elif stability_score >= StabilityLevel.MODERATE.value:
            return EmotionalState.FLUCTUATING
        elif stability_score >= StabilityLevel.CRITICAL.value:
            return EmotionalState.UNSTABLE
        else:
            return EmotionalState.CRITICAL
    
    def predict_stability(self, horizon_minutes: int = 5) -> Dict:
        """
        Predict emotional stability for a future time horizon
        
        Args:
            horizon_minutes: Minutes into the future to predict
            
        Returns:
            Prediction dictionary
        """
        # Check cache
        cache_key = f"pred_{horizon_minutes}"
        if cache_key in self.prediction_cache:
            cached = self.prediction_cache[cache_key]
            if (datetime.now() - cached["timestamp"]).seconds < 60:
                return cached["prediction"]
        
        # Analyze historical trends
        if len(self.stability_history) < 3:
            # Not enough data for prediction
            return {
                "predicted_score": None,
                "confidence": 0.0,
                "trend": "insufficient_data",
                "warning": "Need at least 3 historical data points"
            }
        
        # Simple trend analysis
        recent_scores = [entry["stability_score"] for entry in self.stability_history[-10:]]
        current_score = recent_scores[-1]
        
        # Calculate trend
        if len(recent_scores) >= 2:
            trend_slope = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
        else:
            trend_slope = 0
        
        # Predict future score
        predicted_score = current_score + (trend_slope * horizon_minutes)
        predicted_score = min(100, max(0, predicted_score))
        
        # Calculate confidence based on variance
        variance = sum([(s - current_score) ** 2 for s in recent_scores]) / len(recent_scores)
        confidence = max(0, min(1, 1 - (variance / 1000)))
        
        # Determine trend direction
        if trend_slope > 1:
            trend = "improving"
        elif trend_slope < -1:
            trend = "declining"
        else:
            trend = "stable"
        
        prediction = {
            "predicted_score": predicted_score,
            "confidence": confidence,
            "trend": trend,
            "horizon_minutes": horizon_minutes,
            "current_score": current_score,
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache prediction
        self.prediction_cache[cache_key] = {
            "prediction": prediction,
            "timestamp": datetime.now()
        }
        
        return prediction
    
    def detect_instability_patterns(self) -> List[Dict]:
        """
        Detect patterns that indicate potential instability
        
        Returns:
            List of detected patterns
        """
        patterns = []
        
        if len(self.stability_history) < 5:
            return patterns
        
        recent_entries = self.stability_history[-10:]
        scores = [e["stability_score"] for e in recent_entries]
        
        # Pattern 1: Rapid decline
        if len(scores) >= 3:
            recent_trend = scores[-1] - scores[-3]
            if recent_trend < -15:
                patterns.append({
                    "type": "rapid_decline",
                    "severity": "high",
                    "description": f"Stability decreased by {abs(recent_trend):.1f} points",
                    "recommendation": "Immediate intervention recommended"
                })
        
        # Pattern 2: High volatility
        if len(scores) >= 5:
            changes = [abs(scores[i] - scores[i-1]) for i in range(1, len(scores))]
            avg_change = sum(changes) / len(changes)
            if avg_change > 10:
                patterns.append({
                    "type": "high_volatility",
                    "severity": "medium",
                    "description": f"Average change of {avg_change:.1f} points per interval",
                    "recommendation": "Stabilization protocols suggested"
                })
        
        # Pattern 3: Persistent low state
        if len(scores) >= 5:
            low_count = sum(1 for s in scores[-5:] if s < self.config["stability_threshold"])
            if low_count >= 4:
                patterns.append({
                    "type": "persistent_low",
                    "severity": "high",
                    "description": f"{low_count}/5 recent readings below threshold",
                    "recommendation": "Review interaction protocols"
                })
        
        return patterns
    
    def _generate_recommendations(self, score: float, state: EmotionalState) -> List[str]:
        """
        Generate recommendations based on current state
        
        Args:
            score: Current stability score
            state: Current emotional state
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if state == EmotionalState.CRITICAL:
            recommendations.extend([
                "CRITICAL: Immediate human intervention required",
                "Activate emergency stabilization protocols",
                "Reduce AI interaction complexity",
                "Implement cooling-off period"
            ])
        elif state == EmotionalState.UNSTABLE:
            recommendations.extend([
                "Increase monitoring frequency",
                "Simplify interaction patterns",
                "Enable supportive feedback loops",
                "Consider brief interaction pause"
            ])
        elif state == EmotionalState.FLUCTUATING:
            recommendations.extend([
                "Monitor closely for trends",
                "Adjust interaction pace",
                "Provide additional context in responses"
            ])
        else:
            recommendations.append("Maintain current interaction protocols")
        
        return recommendations
    
    def _record_state(self, state_entry: Dict):
        """Record state in history"""
        self.stability_history.append(state_entry)
        
        # Clean old history
        cutoff_time = datetime.now() - timedelta(seconds=self.config["history_retention"])
        self.stability_history = [
            e for e in self.stability_history
            if datetime.fromisoformat(e["timestamp"]) > cutoff_time
        ]
    
    def _trigger_alert(self, assessment: Dict):
        """Trigger alert for unstable conditions"""
        alert = {
            "type": "emotional_instability",
            "timestamp": datetime.now().isoformat(),
            "severity": assessment["state"],
            "stability_score": assessment["stability_score"],
            "recommendations": assessment["recommendations"]
        }
        
        # Call registered callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"Error in alert callback: {e}")
    
    def register_alert_callback(self, callback):
        """Register a callback for alerts"""
        self.alert_callbacks.append(callback)
    
    def get_statistics(self) -> Dict:
        """
        Get statistical summary
        
        Returns:
            Statistics dictionary
        """
        if not self.stability_history:
            return {
                "total_assessments": 0,
                "average_stability": 0,
                "min_stability": 0,
                "max_stability": 0,
                "current_state": "no_data"
            }
        
        scores = [e["stability_score"] for e in self.stability_history]
        
        return {
            "total_assessments": len(self.stability_history),
            "average_stability": sum(scores) / len(scores),
            "min_stability": min(scores),
            "max_stability": max(scores),
            "current_state": self.stability_history[-1]["state"],
            "time_span_minutes": (
                datetime.fromisoformat(self.stability_history[-1]["timestamp"]) -
                datetime.fromisoformat(self.stability_history[0]["timestamp"])
            ).seconds / 60
        }
    
    def export_report(self, filepath: str):
        """
        Export detailed report
        
        Args:
            filepath: Path to save report
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "config": self.config,
            "statistics": self.get_statistics(),
            "recent_history": self.stability_history[-20:],
            "detected_patterns": self.detect_instability_patterns(),
            "current_prediction": self.predict_stability()
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)


def main():
    """Example usage"""
    print("Metaplano Emozionale - Emotional Stability Prediction")
    print("=" * 60)
    
    # Initialize
    metaplano = MetaplanoEmozionale()
    
    # Simulate some assessments
    test_metrics = [
        {"interaction_quality": 85, "response_time": 120, "coherence_score": 0.92, "stress_indicators": 1},
        {"interaction_quality": 82, "response_time": 150, "coherence_score": 0.89, "stress_indicators": 2},
        {"interaction_quality": 78, "response_time": 180, "coherence_score": 0.85, "stress_indicators": 3},
        {"interaction_quality": 88, "response_time": 110, "coherence_score": 0.94, "stress_indicators": 1},
    ]
    
    print("\nRunning assessments...")
    for i, metrics in enumerate(test_metrics, 1):
        print(f"\nAssessment {i}:")
        assessment = metaplano.assess_current_state(metrics)
        print(f"  Stability Score: {assessment['stability_score']:.2f}")
        print(f"  State: {assessment['state']}")
        time.sleep(0.1)  # Small delay for timestamp variation
    
    # Get prediction
    print("\n" + "=" * 60)
    print("Stability Prediction (5 minutes ahead):")
    prediction = metaplano.predict_stability(5)
    print(f"  Current: {prediction['current_score']:.2f}")
    print(f"  Predicted: {prediction['predicted_score']:.2f}")
    print(f"  Trend: {prediction['trend']}")
    print(f"  Confidence: {prediction['confidence']:.2%}")
    
    # Check for patterns
    print("\n" + "=" * 60)
    print("Detected Patterns:")
    patterns = metaplano.detect_instability_patterns()
    if patterns:
        for pattern in patterns:
            print(f"  - {pattern['type']}: {pattern['description']}")
    else:
        print("  No concerning patterns detected")
    
    # Statistics
    print("\n" + "=" * 60)
    print("Statistics:")
    stats = metaplano.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
