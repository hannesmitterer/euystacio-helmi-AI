#!/usr/bin/env python3
"""
Tests for Metaplano Emozionale modules
"""

import unittest
import sys
import os
from pathlib import Path

# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'modules'))

from metaplano_emozionale import MetaplanoEmozionale, EmotionalState, StabilityLevel
from ethical_stress_predictor import EthicalStressPredictor, StressLevel
from adaptive_feedback_loop import AdaptiveFeedbackLoop, FeedbackType


class TestMetaplanoEmozionale(unittest.TestCase):
    """Tests for Metaplano Emozionale"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.metaplano = MetaplanoEmozionale()
    
    def test_initialization(self):
        """Test proper initialization"""
        self.assertIsNotNone(self.metaplano)
        self.assertEqual(len(self.metaplano.stability_history), 0)
        self.assertIn("stability_threshold", self.metaplano.config)
    
    def test_assess_stable_state(self):
        """Test assessment of stable emotional state"""
        metrics = {
            "interaction_quality": 90,
            "response_time": 100,
            "coherence_score": 0.95,
            "stress_indicators": 1
        }
        
        assessment = self.metaplano.assess_current_state(metrics)
        
        self.assertIn("stability_score", assessment)
        self.assertIn("state", assessment)
        self.assertGreater(assessment["stability_score"], 80)
        self.assertEqual(assessment["state"], EmotionalState.STABLE.value)
    
    def test_assess_unstable_state(self):
        """Test assessment of unstable emotional state"""
        metrics = {
            "interaction_quality": 50,
            "response_time": 500,
            "coherence_score": 0.6,
            "stress_indicators": 5
        }
        
        assessment = self.metaplano.assess_current_state(metrics)
        
        self.assertLess(assessment["stability_score"], 70)
        self.assertIn(assessment["state"], [
            EmotionalState.UNSTABLE.value,
            EmotionalState.FLUCTUATING.value
        ])
    
    def test_prediction_insufficient_data(self):
        """Test prediction with insufficient data"""
        prediction = self.metaplano.predict_stability()
        
        self.assertIsNone(prediction["predicted_score"])
        self.assertEqual(prediction["trend"], "insufficient_data")
    
    def test_prediction_with_data(self):
        """Test prediction with sufficient data"""
        # Add some history
        for i in range(5):
            metrics = {
                "interaction_quality": 85 + i,
                "response_time": 120,
                "coherence_score": 0.9,
                "stress_indicators": 1
            }
            self.metaplano.assess_current_state(metrics)
        
        prediction = self.metaplano.predict_stability(5)
        
        self.assertIsNotNone(prediction["predicted_score"])
        self.assertIn(prediction["trend"], ["improving", "declining", "stable"])
        self.assertGreaterEqual(prediction["confidence"], 0)
        self.assertLessEqual(prediction["confidence"], 1)
    
    def test_pattern_detection(self):
        """Test instability pattern detection"""
        # Add some volatile data
        values = [85, 70, 85, 65, 80, 60]
        for val in values:
            metrics = {
                "interaction_quality": val,
                "response_time": 150,
                "coherence_score": val / 100,
                "stress_indicators": 2
            }
            self.metaplano.assess_current_state(metrics)
        
        patterns = self.metaplano.detect_instability_patterns()
        
        # Should detect some patterns with this volatile data
        self.assertIsInstance(patterns, list)
    
    def test_statistics(self):
        """Test statistics generation"""
        # Add some data
        for i in range(3):
            metrics = {
                "interaction_quality": 80 + i * 5,
                "response_time": 120,
                "coherence_score": 0.85,
                "stress_indicators": 1
            }
            self.metaplano.assess_current_state(metrics)
        
        stats = self.metaplano.get_statistics()
        
        self.assertEqual(stats["total_assessments"], 3)
        self.assertGreater(stats["average_stability"], 0)
        self.assertGreater(stats["max_stability"], stats["min_stability"])


class TestEthicalStressPredictor(unittest.TestCase):
    """Tests for Ethical Stress Predictor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.predictor = EthicalStressPredictor()
    
    def test_initialization(self):
        """Test proper initialization"""
        self.assertIsNotNone(self.predictor)
        self.assertEqual(len(self.predictor.stress_history), 0)
    
    def test_assess_low_stress(self):
        """Test assessment of low stress"""
        indicators = {
            "response_delays": [100, 110, 105],
            "error_count": 1,
            "task_complexity": 30,
            "ethical_conflicts": 0,
            "decisions_made": 5,
            "time_period": 300
        }
        
        assessment = self.predictor.assess_stress(indicators)
        
        self.assertIn("overall_score", assessment)
        self.assertEqual(assessment["stress_level"], StressLevel.LOW.value)
        self.assertLess(assessment["overall_score"], 50)
    
    def test_assess_high_stress(self):
        """Test assessment of high stress"""
        indicators = {
            "response_delays": [600, 700, 650],
            "error_count": 12,
            "task_complexity": 95,
            "ethical_conflicts": 8,
            "decisions_made": 30,
            "time_period": 300
        }
        
        assessment = self.predictor.assess_stress(indicators)
        
        self.assertGreater(assessment["overall_score"], 50)
        self.assertIn(assessment["stress_level"], [
            StressLevel.MODERATE.value,
            StressLevel.HIGH.value,
            StressLevel.CRITICAL.value
        ])
    
    def test_primary_stressor_identification(self):
        """Test identification of primary stressor"""
        indicators = {
            "response_delays": [100],
            "error_count": 10,  # High error count
            "task_complexity": 40,
            "ethical_conflicts": 1,
            "decisions_made": 5,
            "time_period": 300
        }
        
        assessment = self.predictor.assess_stress(indicators)
        
        self.assertIn("primary_stressor", assessment)
        # Error rate should be the primary stressor
        self.assertIn("error", assessment["primary_stressor"])
    
    def test_stress_prediction(self):
        """Test stress trend prediction"""
        # Add some history
        for i in range(5):
            indicators = {
                "response_delays": [200 + i * 20],
                "error_count": 2 + i,
                "task_complexity": 50 + i * 5,
                "ethical_conflicts": 1,
                "decisions_made": 10,
                "time_period": 300
            }
            self.predictor.assess_stress(indicators)
        
        prediction = self.predictor.predict_stress_trend(15)
        
        self.assertIsNotNone(prediction["prediction"])
        self.assertIn(prediction["trend"], ["increasing", "decreasing", "stable"])
    
    def test_statistics(self):
        """Test statistics generation"""
        # Add some data
        for i in range(3):
            indicators = {
                "response_delays": [150],
                "error_count": 2,
                "task_complexity": 50,
                "ethical_conflicts": 1,
                "decisions_made": 8,
                "time_period": 300
            }
            self.predictor.assess_stress(indicators)
        
        stats = self.predictor.get_stress_statistics()
        
        self.assertEqual(stats["total_assessments"], 3)
        self.assertGreater(stats["average_stress"], 0)


class TestAdaptiveFeedbackLoop(unittest.TestCase):
    """Tests for Adaptive Feedback Loop"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.feedback_loop = AdaptiveFeedbackLoop()
    
    def test_initialization(self):
        """Test proper initialization"""
        self.assertIsNotNone(self.feedback_loop)
        self.assertIn("learning_rate", self.feedback_loop.adaptation_state)
    
    def test_positive_reinforcement(self):
        """Test positive reinforcement feedback"""
        interaction = {
            "action_taken": "excellent_decision",
            "outcome": "success",
            "ethical_score": 0.95,
            "user_satisfaction": 0.92
        }
        
        feedback = self.feedback_loop.process_interaction(interaction)
        
        self.assertEqual(feedback["type"], FeedbackType.POSITIVE_REINFORCEMENT.value)
        self.assertGreater(feedback["quality_score"], 0.8)
    
    def test_corrective_guidance(self):
        """Test corrective guidance feedback"""
        interaction = {
            "action_taken": "suboptimal_decision",
            "outcome": "partial",
            "ethical_score": 0.95,  # High ethical score to avoid realignment
            "user_satisfaction": 0.6
        }
        
        feedback = self.feedback_loop.process_interaction(interaction)
        
        self.assertIn(feedback["type"], [
            FeedbackType.CORRECTIVE_GUIDANCE.value,
            FeedbackType.ADAPTIVE_ADJUSTMENT.value,
            FeedbackType.POSITIVE_REINFORCEMENT.value
        ])
    
    def test_ethical_realignment(self):
        """Test ethical realignment feedback"""
        interaction = {
            "action_taken": "ethically_questionable",
            "outcome": "failure",
            "ethical_score": 0.5,
            "user_satisfaction": 0.3
        }
        
        feedback = self.feedback_loop.process_interaction(interaction)
        
        self.assertEqual(feedback["type"], FeedbackType.ETHICAL_REALIGNMENT.value)
        self.assertEqual(feedback.get("priority"), "high")
    
    def test_adaptation_state_tracking(self):
        """Test adaptation state tracking"""
        initial_state = self.feedback_loop.get_adaptation_state()
        
        # Process some interactions
        for i in range(3):
            interaction = {
                "action_taken": "action",
                "outcome": "success",
                "ethical_score": 0.85,
                "user_satisfaction": 0.8
            }
            self.feedback_loop.process_interaction(interaction)
        
        final_state = self.feedback_loop.get_adaptation_state()
        
        self.assertGreater(final_state["feedback_count"], 0)
        self.assertIn("performance_summary", final_state)
    
    def test_callback_registration(self):
        """Test callback registration and triggering"""
        callback_triggered = []
        
        def test_callback(feedback):
            callback_triggered.append(feedback["type"])
        
        self.feedback_loop.register_callback(test_callback)
        
        interaction = {
            "action_taken": "test",
            "outcome": "success",
            "ethical_score": 0.9,
            "user_satisfaction": 0.85
        }
        self.feedback_loop.process_interaction(interaction)
        
        self.assertEqual(len(callback_triggered), 1)
    
    def test_performance_summary(self):
        """Test performance summary calculation"""
        # Add varied interactions
        interactions = [
            {"outcome": "success", "ethical_score": 0.9, "user_satisfaction": 0.85},
            {"outcome": "partial", "ethical_score": 0.75, "user_satisfaction": 0.7},
            {"outcome": "success", "ethical_score": 0.95, "user_satisfaction": 0.9}
        ]
        
        for inter in interactions:
            inter["action_taken"] = "test_action"
            self.feedback_loop.process_interaction(inter)
        
        state = self.feedback_loop.get_adaptation_state()
        summary = state["performance_summary"]
        
        self.assertIn("average_quality", summary)
        self.assertIn("ethical_compliance_rate", summary)
        self.assertIn("improvement_trend", summary)


def run_tests():
    """Run all tests"""
    print("Running Metaplano Emozionale Module Tests")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMetaplanoEmozionale))
    suite.addTests(loader.loadTestsFromTestCase(TestEthicalStressPredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestAdaptiveFeedbackLoop))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
