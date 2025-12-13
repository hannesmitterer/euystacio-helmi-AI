#!/usr/bin/env python3
"""
Ethical Stress Predictor
Predicts stress levels in human-AI collaborative environments
Part of Phase III - The Symbiosis
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum


class StressLevel(Enum):
    """Stress level categories"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class StressIndicator(Enum):
    """Types of stress indicators"""
    RESPONSE_DELAY = "response_delay"
    ERROR_RATE = "error_rate"
    COMPLEXITY_OVERLOAD = "complexity_overload"
    ETHICAL_CONFLICT = "ethical_conflict"
    DECISION_FATIGUE = "decision_fatigue"


class EthicalStressPredictor:
    """
    Predicts and monitors stress levels in human-AI ethical interactions
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the stress predictor
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or self._default_config()
        self.stress_history = []
        self.indicator_weights = self._initialize_weights()
        
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "low_threshold": 30,
            "moderate_threshold": 50,
            "high_threshold": 70,
            "critical_threshold": 85,
            "history_retention": 7200,  # 2 hours in seconds
            "prediction_sensitivity": 0.7,
            "adaptive_thresholds": True
        }
    
    def _initialize_weights(self) -> Dict[StressIndicator, float]:
        """Initialize indicator weights"""
        return {
            StressIndicator.RESPONSE_DELAY: 0.2,
            StressIndicator.ERROR_RATE: 0.25,
            StressIndicator.COMPLEXITY_OVERLOAD: 0.2,
            StressIndicator.ETHICAL_CONFLICT: 0.25,
            StressIndicator.DECISION_FATIGUE: 0.1
        }
    
    def assess_stress(self, indicators: Dict) -> Dict:
        """
        Assess current stress level based on indicators
        
        Args:
            indicators: Dictionary of stress indicators
                - response_delays: List of delay times (ms)
                - error_count: Number of errors in period
                - task_complexity: Complexity score (0-100)
                - ethical_conflicts: Number of conflicts detected
                - decisions_made: Number of decisions in period
                - time_period: Time period in seconds
                
        Returns:
            Stress assessment dictionary
        """
        # Calculate individual indicator scores
        scores = {}
        
        # Response delay score
        if "response_delays" in indicators and indicators["response_delays"]:
            avg_delay = sum(indicators["response_delays"]) / len(indicators["response_delays"])
            scores[StressIndicator.RESPONSE_DELAY] = min(100, (avg_delay / 10))
        else:
            scores[StressIndicator.RESPONSE_DELAY] = 0
        
        # Error rate score
        if "error_count" in indicators and "time_period" in indicators:
            error_rate = indicators["error_count"] / (indicators["time_period"] / 60)  # errors per minute
            scores[StressIndicator.ERROR_RATE] = min(100, error_rate * 20)
        else:
            scores[StressIndicator.ERROR_RATE] = 0
        
        # Complexity overload score
        if "task_complexity" in indicators:
            scores[StressIndicator.COMPLEXITY_OVERLOAD] = indicators["task_complexity"]
        else:
            scores[StressIndicator.COMPLEXITY_OVERLOAD] = 0
        
        # Ethical conflict score
        if "ethical_conflicts" in indicators and "time_period" in indicators:
            conflict_rate = indicators["ethical_conflicts"] / (indicators["time_period"] / 60)
            scores[StressIndicator.ETHICAL_CONFLICT] = min(100, conflict_rate * 25)
        else:
            scores[StressIndicator.ETHICAL_CONFLICT] = 0
        
        # Decision fatigue score
        if "decisions_made" in indicators and "time_period" in indicators:
            decision_rate = indicators["decisions_made"] / (indicators["time_period"] / 60)
            # High decision rate indicates potential fatigue
            scores[StressIndicator.DECISION_FATIGUE] = min(100, max(0, (decision_rate - 5) * 10))
        else:
            scores[StressIndicator.DECISION_FATIGUE] = 0
        
        # Calculate weighted overall stress score
        overall_score = sum(
            scores[indicator] * weight 
            for indicator, weight in self.indicator_weights.items()
        )
        
        # Determine stress level
        stress_level = self._determine_stress_level(overall_score)
        
        # Create assessment
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "overall_score": overall_score,
            "stress_level": stress_level.value,
            "indicator_scores": {k.value: v for k, v in scores.items()},
            "primary_stressor": self._identify_primary_stressor(scores),
            "recommendations": self._generate_stress_recommendations(overall_score, scores)
        }
        
        # Record in history
        self._record_assessment(assessment)
        
        return assessment
    
    def _determine_stress_level(self, score: float) -> StressLevel:
        """
        Determine stress level from score
        
        Args:
            score: Stress score (0-100)
            
        Returns:
            StressLevel enum value
        """
        if score >= self.config["critical_threshold"]:
            return StressLevel.CRITICAL
        elif score >= self.config["high_threshold"]:
            return StressLevel.HIGH
        elif score >= self.config["moderate_threshold"]:
            return StressLevel.MODERATE
        else:
            return StressLevel.LOW
    
    def _identify_primary_stressor(self, scores: Dict) -> str:
        """
        Identify the primary stressor from indicator scores
        
        Args:
            scores: Dictionary of indicator scores
            
        Returns:
            Name of primary stressor
        """
        if not scores:
            return "none"
        
        max_indicator = max(scores.items(), key=lambda x: x[1])
        return max_indicator[0].value
    
    def _generate_stress_recommendations(self, overall_score: float, scores: Dict) -> List[str]:
        """
        Generate recommendations for stress management
        
        Args:
            overall_score: Overall stress score
            scores: Individual indicator scores
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Overall stress recommendations
        if overall_score >= self.config["critical_threshold"]:
            recommendations.append("CRITICAL: Immediate intervention required - suspend non-essential tasks")
            recommendations.append("Activate stress reduction protocols")
        elif overall_score >= self.config["high_threshold"]:
            recommendations.append("High stress detected - reduce task complexity")
            recommendations.append("Consider task delegation or postponement")
        elif overall_score >= self.config["moderate_threshold"]:
            recommendations.append("Moderate stress - monitor closely")
        
        # Specific indicator recommendations
        if scores.get(StressIndicator.RESPONSE_DELAY, 0) > 70:
            recommendations.append("Response delays significant - reduce interaction pace")
        
        if scores.get(StressIndicator.ERROR_RATE, 0) > 60:
            recommendations.append("Error rate elevated - implement validation checkpoints")
        
        if scores.get(StressIndicator.COMPLEXITY_OVERLOAD, 0) > 75:
            recommendations.append("Complexity overload - simplify task structure")
        
        if scores.get(StressIndicator.ETHICAL_CONFLICT, 0) > 65:
            recommendations.append("Ethical conflicts detected - engage ethical review protocols")
        
        if scores.get(StressIndicator.DECISION_FATIGUE, 0) > 60:
            recommendations.append("Decision fatigue present - schedule rest period")
        
        if not recommendations:
            recommendations.append("Stress levels optimal - maintain current protocols")
        
        return recommendations
    
    def predict_stress_trend(self, horizon_minutes: int = 15) -> Dict:
        """
        Predict stress trend for future time horizon
        
        Args:
            horizon_minutes: Minutes into future to predict
            
        Returns:
            Prediction dictionary
        """
        if len(self.stress_history) < 3:
            return {
                "prediction": None,
                "confidence": 0.0,
                "trend": "insufficient_data",
                "warning": "Need at least 3 historical assessments"
            }
        
        # Extract recent stress scores
        recent_scores = [entry["overall_score"] for entry in self.stress_history[-10:]]
        current_score = recent_scores[-1]
        
        # Calculate trend
        if len(recent_scores) >= 2:
            trend_slope = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
        else:
            trend_slope = 0
        
        # Predict future score
        predicted_score = current_score + (trend_slope * horizon_minutes / 5)
        predicted_score = min(100, max(0, predicted_score))
        
        # Determine trend direction
        if trend_slope > 2:
            trend_direction = "increasing"
        elif trend_slope < -2:
            trend_direction = "decreasing"
        else:
            trend_direction = "stable"
        
        # Calculate confidence
        variance = sum([(s - current_score) ** 2 for s in recent_scores]) / len(recent_scores)
        confidence = max(0, min(1, 1 - (variance / 1000)))
        
        # Determine predicted level
        predicted_level = self._determine_stress_level(predicted_score)
        
        return {
            "prediction": predicted_score,
            "predicted_level": predicted_level.value,
            "current_score": current_score,
            "trend": trend_direction,
            "confidence": confidence,
            "horizon_minutes": horizon_minutes,
            "timestamp": datetime.now().isoformat(),
            "warning": self._generate_prediction_warning(predicted_level, trend_direction)
        }
    
    def _generate_prediction_warning(self, predicted_level: StressLevel, trend: str) -> Optional[str]:
        """Generate warning based on prediction"""
        if predicted_level == StressLevel.CRITICAL:
            return "Critical stress levels predicted - proactive intervention recommended"
        elif predicted_level == StressLevel.HIGH and trend == "increasing":
            return "Stress levels rising toward critical - prepare intervention"
        elif trend == "increasing" and predicted_level in [StressLevel.MODERATE, StressLevel.HIGH]:
            return "Upward stress trend detected - monitor closely"
        return None
    
    def _record_assessment(self, assessment: Dict):
        """Record assessment in history"""
        self.stress_history.append(assessment)
        
        # Clean old history
        cutoff_time = datetime.now() - timedelta(seconds=self.config["history_retention"])
        self.stress_history = [
            e for e in self.stress_history
            if datetime.fromisoformat(e["timestamp"]) > cutoff_time
        ]
    
    def get_stress_statistics(self) -> Dict:
        """
        Get stress statistics
        
        Returns:
            Statistics dictionary
        """
        if not self.stress_history:
            return {
                "total_assessments": 0,
                "average_stress": 0,
                "peak_stress": 0,
                "current_level": "no_data"
            }
        
        scores = [e["overall_score"] for e in self.stress_history]
        
        return {
            "total_assessments": len(self.stress_history),
            "average_stress": sum(scores) / len(scores),
            "peak_stress": max(scores),
            "minimum_stress": min(scores),
            "current_level": self.stress_history[-1]["stress_level"],
            "time_in_high_stress": self._calculate_time_in_level(StressLevel.HIGH, StressLevel.CRITICAL),
            "primary_stressors": self._get_common_stressors()
        }
    
    def _calculate_time_in_level(self, *levels: StressLevel) -> float:
        """Calculate percentage of time in specified stress levels"""
        level_values = [level.value for level in levels]
        count = sum(1 for e in self.stress_history if e["stress_level"] in level_values)
        
        if not self.stress_history:
            return 0.0
        
        return (count / len(self.stress_history)) * 100
    
    def _get_common_stressors(self) -> List[str]:
        """Get most common primary stressors"""
        if not self.stress_history:
            return []
        
        stressor_counts = {}
        for entry in self.stress_history:
            stressor = entry.get("primary_stressor", "unknown")
            stressor_counts[stressor] = stressor_counts.get(stressor, 0) + 1
        
        # Sort by frequency
        sorted_stressors = sorted(stressor_counts.items(), key=lambda x: x[1], reverse=True)
        return [stressor for stressor, _ in sorted_stressors[:3]]


def main():
    """Example usage"""
    print("Ethical Stress Predictor")
    print("=" * 60)
    
    # Initialize
    predictor = EthicalStressPredictor()
    
    # Simulate stress assessments
    test_scenarios = [
        {
            "name": "Low stress scenario",
            "indicators": {
                "response_delays": [100, 120, 110],
                "error_count": 1,
                "task_complexity": 40,
                "ethical_conflicts": 0,
                "decisions_made": 5,
                "time_period": 300
            }
        },
        {
            "name": "Moderate stress scenario",
            "indicators": {
                "response_delays": [200, 250, 220],
                "error_count": 3,
                "task_complexity": 65,
                "ethical_conflicts": 2,
                "decisions_made": 12,
                "time_period": 300
            }
        },
        {
            "name": "High stress scenario",
            "indicators": {
                "response_delays": [350, 400, 380],
                "error_count": 6,
                "task_complexity": 85,
                "ethical_conflicts": 4,
                "decisions_made": 20,
                "time_period": 300
            }
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{scenario['name']}:")
        assessment = predictor.assess_stress(scenario["indicators"])
        print(f"  Overall Score: {assessment['overall_score']:.2f}")
        print(f"  Stress Level: {assessment['stress_level']}")
        print(f"  Primary Stressor: {assessment['primary_stressor']}")
        print(f"  Recommendations:")
        for rec in assessment["recommendations"]:
            print(f"    - {rec}")
    
    # Get prediction
    print("\n" + "=" * 60)
    print("Stress Trend Prediction (15 minutes ahead):")
    prediction = predictor.predict_stress_trend(15)
    print(f"  Current: {prediction['current_score']:.2f}")
    print(f"  Predicted: {prediction['prediction']:.2f}")
    print(f"  Level: {prediction['predicted_level']}")
    print(f"  Trend: {prediction['trend']}")
    print(f"  Confidence: {prediction['confidence']:.2%}")
    if prediction.get("warning"):
        print(f"  ⚠️  Warning: {prediction['warning']}")
    
    # Statistics
    print("\n" + "=" * 60)
    print("Statistics:")
    stats = predictor.get_stress_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
