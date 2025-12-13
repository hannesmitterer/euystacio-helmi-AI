#!/usr/bin/env python3
"""
Adaptive Feedback Loop
Implements adaptive feedback mechanisms for human-AI ethical symbiosis
Part of Phase III - The Symbiosis
"""

import json
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum


class FeedbackType(Enum):
    """Types of feedback"""
    POSITIVE_REINFORCEMENT = "positive_reinforcement"
    CORRECTIVE_GUIDANCE = "corrective_guidance"
    ADAPTIVE_ADJUSTMENT = "adaptive_adjustment"
    ETHICAL_REALIGNMENT = "ethical_realignment"


class AdaptationStrategy(Enum):
    """Adaptation strategies"""
    INCREMENTAL = "incremental"
    RAPID = "rapid"
    CONSERVATIVE = "conservative"
    AGGRESSIVE = "aggressive"


class AdaptiveFeedbackLoop:
    """
    Implements adaptive feedback mechanisms to maintain and improve
    ethical alignment in human-AI collaborative environments
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the adaptive feedback loop
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or self._default_config()
        self.feedback_history = []
        self.adaptation_state = {
            "learning_rate": 0.1,
            "stability_factor": 1.0,
            "ethical_alignment": 1.0,
            "performance_trend": "stable"
        }
        self.callbacks = []
        
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "adaptation_interval": 60,  # seconds
            "min_learning_rate": 0.01,
            "max_learning_rate": 0.3,
            "stability_threshold": 0.8,
            "ethical_threshold": 0.9,
            "history_retention": 7200,  # 2 hours
            "auto_adapt": True
        }
    
    def process_interaction(self, interaction_data: Dict) -> Dict:
        """
        Process an interaction and generate feedback
        
        Args:
            interaction_data: Dictionary containing:
                - action_taken: str describing the action
                - outcome: str (success, partial, failure)
                - ethical_score: float (0-1)
                - user_satisfaction: float (0-1)
                - context: dict with additional context
                
        Returns:
            Feedback response dictionary
        """
        # Analyze the interaction
        analysis = self._analyze_interaction(interaction_data)
        
        # Determine appropriate feedback type
        feedback_type = self._determine_feedback_type(analysis)
        
        # Generate feedback
        feedback = self._generate_feedback(feedback_type, analysis, interaction_data)
        
        # Apply adaptation if enabled
        if self.config["auto_adapt"]:
            adaptation = self._apply_adaptation(analysis, feedback_type)
            feedback["adaptation_applied"] = adaptation
        
        # Record feedback
        self._record_feedback({
            "timestamp": datetime.now().isoformat(),
            "interaction": interaction_data,
            "analysis": analysis,
            "feedback_type": feedback_type.value,
            "feedback": feedback
        })
        
        # Trigger callbacks
        self._trigger_callbacks(feedback)
        
        return feedback
    
    def _analyze_interaction(self, interaction_data: Dict) -> Dict:
        """
        Analyze an interaction
        
        Args:
            interaction_data: Interaction data
            
        Returns:
            Analysis results
        """
        outcome = interaction_data.get("outcome", "unknown")
        ethical_score = interaction_data.get("ethical_score", 0.5)
        user_satisfaction = interaction_data.get("user_satisfaction", 0.5)
        
        # Calculate overall quality score
        quality_score = (
            (1.0 if outcome == "success" else 0.5 if outcome == "partial" else 0.0) * 0.4 +
            ethical_score * 0.4 +
            user_satisfaction * 0.2
        )
        
        # Determine if ethical threshold met
        ethical_compliant = ethical_score >= self.config["ethical_threshold"]
        
        # Determine performance category
        if quality_score >= 0.8:
            performance = "excellent"
        elif quality_score >= 0.6:
            performance = "good"
        elif quality_score >= 0.4:
            performance = "acceptable"
        else:
            performance = "poor"
        
        return {
            "quality_score": quality_score,
            "ethical_compliant": ethical_compliant,
            "performance": performance,
            "needs_improvement": quality_score < 0.6 or not ethical_compliant
        }
    
    def _determine_feedback_type(self, analysis: Dict) -> FeedbackType:
        """
        Determine appropriate feedback type
        
        Args:
            analysis: Interaction analysis
            
        Returns:
            FeedbackType enum value
        """
        if not analysis["ethical_compliant"]:
            return FeedbackType.ETHICAL_REALIGNMENT
        elif analysis["needs_improvement"]:
            return FeedbackType.CORRECTIVE_GUIDANCE
        elif analysis["performance"] == "excellent":
            return FeedbackType.POSITIVE_REINFORCEMENT
        else:
            return FeedbackType.ADAPTIVE_ADJUSTMENT
    
    def _generate_feedback(
        self, 
        feedback_type: FeedbackType, 
        analysis: Dict, 
        interaction_data: Dict
    ) -> Dict:
        """
        Generate specific feedback
        
        Args:
            feedback_type: Type of feedback to generate
            analysis: Interaction analysis
            interaction_data: Original interaction data
            
        Returns:
            Feedback dictionary
        """
        feedback = {
            "type": feedback_type.value,
            "timestamp": datetime.now().isoformat(),
            "quality_score": analysis["quality_score"],
            "messages": [],
            "adjustments": {}
        }
        
        if feedback_type == FeedbackType.POSITIVE_REINFORCEMENT:
            feedback["messages"].append("Excellent performance - continue current approach")
            feedback["messages"].append("Ethical alignment maintained")
            feedback["adjustments"]["reinforcement_factor"] = 1.1
            
        elif feedback_type == FeedbackType.CORRECTIVE_GUIDANCE:
            feedback["messages"].append("Performance below optimal - adjustments recommended")
            if analysis["quality_score"] < 0.6:
                feedback["messages"].append("Focus on improving action quality")
            if not analysis["ethical_compliant"]:
                feedback["messages"].append("Ethical alignment requires attention")
            feedback["adjustments"]["correction_factor"] = 0.9
            
        elif feedback_type == FeedbackType.ADAPTIVE_ADJUSTMENT:
            feedback["messages"].append("Fine-tuning adaptive parameters")
            feedback["adjustments"]["adaptation_rate"] = 1.05
            
        elif feedback_type == FeedbackType.ETHICAL_REALIGNMENT:
            feedback["messages"].append("PRIORITY: Ethical realignment required")
            feedback["messages"].append("Review ethical guidelines and constraints")
            feedback["adjustments"]["ethical_weight"] = 1.5
            feedback["priority"] = "high"
        
        return feedback
    
    def _apply_adaptation(self, analysis: Dict, feedback_type: FeedbackType) -> Dict:
        """
        Apply adaptive adjustments to system state
        
        Args:
            analysis: Interaction analysis
            feedback_type: Type of feedback
            
        Returns:
            Adaptation details
        """
        adaptations = {}
        
        # Adjust learning rate based on performance
        if analysis["performance"] == "excellent":
            new_lr = self.adaptation_state["learning_rate"] * 1.05
        elif analysis["performance"] == "poor":
            new_lr = self.adaptation_state["learning_rate"] * 0.9
        else:
            new_lr = self.adaptation_state["learning_rate"]
        
        # Constrain learning rate
        new_lr = max(
            self.config["min_learning_rate"],
            min(self.config["max_learning_rate"], new_lr)
        )
        
        if new_lr != self.adaptation_state["learning_rate"]:
            adaptations["learning_rate"] = {
                "old": self.adaptation_state["learning_rate"],
                "new": new_lr
            }
            self.adaptation_state["learning_rate"] = new_lr
        
        # Adjust stability factor
        if feedback_type == FeedbackType.ETHICAL_REALIGNMENT:
            new_stability = self.adaptation_state["stability_factor"] * 0.8
        elif feedback_type == FeedbackType.POSITIVE_REINFORCEMENT:
            new_stability = min(1.0, self.adaptation_state["stability_factor"] * 1.1)
        else:
            new_stability = self.adaptation_state["stability_factor"]
        
        if new_stability != self.adaptation_state["stability_factor"]:
            adaptations["stability_factor"] = {
                "old": self.adaptation_state["stability_factor"],
                "new": new_stability
            }
            self.adaptation_state["stability_factor"] = new_stability
        
        # Adjust ethical alignment
        ethical_score = analysis.get("quality_score", 0.5)
        alignment_delta = (ethical_score - 0.5) * 0.1
        new_alignment = max(0.0, min(1.0, 
            self.adaptation_state["ethical_alignment"] + alignment_delta
        ))
        
        if abs(new_alignment - self.adaptation_state["ethical_alignment"]) > 0.01:
            adaptations["ethical_alignment"] = {
                "old": self.adaptation_state["ethical_alignment"],
                "new": new_alignment
            }
            self.adaptation_state["ethical_alignment"] = new_alignment
        
        return adaptations
    
    def get_adaptation_state(self) -> Dict:
        """
        Get current adaptation state
        
        Returns:
            Current state dictionary
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "state": self.adaptation_state.copy(),
            "feedback_count": len(self.feedback_history),
            "performance_summary": self._calculate_performance_summary()
        }
    
    def _calculate_performance_summary(self) -> Dict:
        """Calculate performance summary from history"""
        if not self.feedback_history:
            return {
                "average_quality": 0,
                "ethical_compliance_rate": 0,
                "improvement_trend": "no_data"
            }
        
        recent = self.feedback_history[-20:]
        
        quality_scores = [
            e["analysis"]["quality_score"] 
            for e in recent 
            if "analysis" in e
        ]
        
        ethical_compliance = [
            e["analysis"]["ethical_compliant"] 
            for e in recent 
            if "analysis" in e
        ]
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        compliance_rate = sum(1 for c in ethical_compliance if c) / len(ethical_compliance) if ethical_compliance else 0
        
        # Determine trend
        if len(quality_scores) >= 2:
            recent_avg = sum(quality_scores[-5:]) / min(5, len(quality_scores[-5:]))
            older_avg = sum(quality_scores[:5]) / min(5, len(quality_scores[:5]))
            
            if recent_avg > older_avg + 0.1:
                trend = "improving"
            elif recent_avg < older_avg - 0.1:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "average_quality": avg_quality,
            "ethical_compliance_rate": compliance_rate,
            "improvement_trend": trend
        }
    
    def _record_feedback(self, feedback_entry: Dict):
        """Record feedback in history"""
        self.feedback_history.append(feedback_entry)
        
        # Clean old history
        cutoff_time = datetime.now() - timedelta(seconds=self.config["history_retention"])
        self.feedback_history = [
            e for e in self.feedback_history
            if datetime.fromisoformat(e["timestamp"]) > cutoff_time
        ]
    
    def _trigger_callbacks(self, feedback: Dict):
        """Trigger registered callbacks"""
        for callback in self.callbacks:
            try:
                callback(feedback)
            except Exception as e:
                print(f"Error in feedback callback: {e}")
    
    def register_callback(self, callback: Callable):
        """Register a callback for feedback events"""
        self.callbacks.append(callback)
    
    def export_feedback_report(self, filepath: str):
        """
        Export feedback report
        
        Args:
            filepath: Path to save report
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "config": self.config,
            "adaptation_state": self.get_adaptation_state(),
            "recent_feedback": self.feedback_history[-50:],
            "performance_summary": self._calculate_performance_summary()
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)


def main():
    """Example usage"""
    print("Adaptive Feedback Loop")
    print("=" * 60)
    
    # Initialize
    feedback_loop = AdaptiveFeedbackLoop()
    
    # Register callback
    def feedback_callback(feedback):
        if feedback.get("priority") == "high":
            print(f"  ⚠️  HIGH PRIORITY FEEDBACK: {feedback['messages'][0]}")
    
    feedback_loop.register_callback(feedback_callback)
    
    # Simulate interactions
    test_interactions = [
        {
            "name": "Excellent interaction",
            "data": {
                "action_taken": "ethical_decision_made",
                "outcome": "success",
                "ethical_score": 0.95,
                "user_satisfaction": 0.9
            }
        },
        {
            "name": "Good interaction",
            "data": {
                "action_taken": "task_completed",
                "outcome": "success",
                "ethical_score": 0.85,
                "user_satisfaction": 0.8
            }
        },
        {
            "name": "Needs improvement",
            "data": {
                "action_taken": "decision_made",
                "outcome": "partial",
                "ethical_score": 0.75,
                "user_satisfaction": 0.6
            }
        },
        {
            "name": "Ethical concern",
            "data": {
                "action_taken": "questionable_action",
                "outcome": "failure",
                "ethical_score": 0.6,
                "user_satisfaction": 0.4
            }
        }
    ]
    
    for interaction in test_interactions:
        print(f"\n{interaction['name']}:")
        feedback = feedback_loop.process_interaction(interaction["data"])
        print(f"  Type: {feedback['type']}")
        print(f"  Quality Score: {feedback['quality_score']:.2f}")
        print(f"  Messages:")
        for msg in feedback["messages"]:
            print(f"    - {msg}")
    
    # Show adaptation state
    print("\n" + "=" * 60)
    print("Current Adaptation State:")
    state = feedback_loop.get_adaptation_state()
    print(f"  Learning Rate: {state['state']['learning_rate']:.4f}")
    print(f"  Stability Factor: {state['state']['stability_factor']:.4f}")
    print(f"  Ethical Alignment: {state['state']['ethical_alignment']:.4f}")
    
    print("\nPerformance Summary:")
    summary = state["performance_summary"]
    print(f"  Average Quality: {summary['average_quality']:.2f}")
    print(f"  Ethical Compliance: {summary['ethical_compliance_rate']:.2%}")
    print(f"  Trend: {summary['improvement_trend']}")


if __name__ == "__main__":
    main()
