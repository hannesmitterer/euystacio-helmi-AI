"""
Unit Tests for NRE-003: Async-Asym Protocol
============================================

Tests cover:
1. Information Gift delivery (Asynchronous Dimension)
2. Veto trigger logic (Asymmetric Approach)
3. Rollback plan generation and evaluation
4. AAI calculation and tracking
5. Protocol status monitoring

Author: Euystacio-Helmi AI Framework
Version: 1.0.0
Date: 2025-12-10
"""

import unittest
import sys
import os
import tempfile
import json
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nre_003_protocol import (
    NRE003Protocol,
    PredictiveInformation,
    RollbackPlan,
    VetoRecord,
    DecisionCategory
)


class TestInformationGift(unittest.TestCase):
    """Test the Asynchronous Dimension - Information Gift Total."""
    
    def setUp(self):
        """Set up test protocol instance."""
        self.protocol = NRE003Protocol()
    
    def test_information_gift_creation(self):
        """Test that information gifts are created correctly."""
        info = self.protocol.provide_information_gift(
            decision_id="TEST-001",
            well_being_lift=0.45,
            residual_ethical_risk=0.12,
            risk_factors=["Minor inefficiency"],
            opportunity_factors=["Learning opportunity"],
            alternative_paths=[{"path": "A", "wbl": 0.45, "rer": 0.12}],
            confidence_level=0.85
        )
        
        self.assertEqual(info.decision_id, "TEST-001")
        self.assertEqual(info.well_being_lift, 0.45)
        self.assertEqual(info.residual_ethical_risk, 0.12)
        self.assertFalse(info.is_catastrophic_risk())
        self.assertEqual(len(self.protocol.information_gifts), 1)
    
    def test_information_gift_tracking(self):
        """Test that multiple information gifts are tracked."""
        for i in range(5):
            self.protocol.provide_information_gift(
                decision_id=f"TEST-{i:03d}",
                well_being_lift=0.3 + i * 0.1,
                residual_ethical_risk=0.1 + i * 0.05,
                risk_factors=[],
                opportunity_factors=[],
                alternative_paths=[],
                confidence_level=0.8
            )
        
        self.assertEqual(len(self.protocol.information_gifts), 5)
    
    def test_catastrophic_risk_detection(self):
        """Test detection of catastrophic risk in information gift."""
        info = self.protocol.provide_information_gift(
            decision_id="TEST-CATASTROPHIC",
            well_being_lift=-0.95,
            residual_ethical_risk=0.9995,
            risk_factors=["Existential threat"],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.97
        )
        
        self.assertTrue(info.is_catastrophic_risk())
        self.assertGreater(info.residual_ethical_risk, 0.999)


class TestAsymmetricVeto(unittest.TestCase):
    """Test the Asymmetric Approach - Preventive Veto Minimum."""
    
    def setUp(self):
        """Set up test protocol instance."""
        self.protocol = NRE003Protocol()
    
    def test_veto_not_triggered_for_low_risk(self):
        """Test that veto is NOT triggered for low risk decisions."""
        info = self.protocol.provide_information_gift(
            decision_id="LOW-RISK",
            well_being_lift=0.5,
            residual_ethical_risk=0.15,
            risk_factors=["Minor risk"],
            opportunity_factors=["Good opportunity"],
            alternative_paths=[],
            confidence_level=0.8
        )
        
        self.assertFalse(self.protocol.evaluate_veto_necessity(info))
    
    def test_veto_not_triggered_for_moderate_risk(self):
        """Test that veto is NOT triggered for moderate risk decisions."""
        info = self.protocol.provide_information_gift(
            decision_id="MODERATE-RISK",
            well_being_lift=0.2,
            residual_ethical_risk=0.65,
            risk_factors=["Moderate risk"],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.75
        )
        
        self.assertFalse(self.protocol.evaluate_veto_necessity(info))
    
    def test_veto_triggered_for_catastrophic_risk(self):
        """Test that veto IS triggered for catastrophic risk (RER > 0.999)."""
        info = self.protocol.provide_information_gift(
            decision_id="CATASTROPHIC-RISK",
            well_being_lift=-0.95,
            residual_ethical_risk=0.9995,
            risk_factors=["Existential threat"],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.97
        )
        
        self.assertTrue(self.protocol.evaluate_veto_necessity(info))
    
    def test_veto_issuance_with_rollback_plan(self):
        """Test that veto issuance creates proper rollback plan."""
        info = self.protocol.provide_information_gift(
            decision_id="VETO-TEST",
            well_being_lift=-0.90,
            residual_ethical_risk=0.9998,
            risk_factors=["Critical threat"],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.95
        )
        
        veto = self.protocol.issue_preventive_veto(
            predictive_info=info,
            justification="Critical existential threat detected",
            reactivation_conditions=["Threat mitigated", "Security verified"],
            monitoring_metrics=["Security score", "Risk assessment"],
            review_schedule=[datetime.now() + timedelta(days=7)],
            responsible_authority="Test Authority"
        )
        
        self.assertIsNotNone(veto)
        self.assertEqual(veto.decision_id, "VETO-TEST")
        self.assertGreater(veto.rer_value, 0.999)
        self.assertIsNotNone(veto.rollback_plan)
        self.assertEqual(len(veto.rollback_plan.reactivation_conditions), 2)
        self.assertEqual(len(self.protocol.veto_records), 1)
        self.assertEqual(len(self.protocol.rollback_plans), 1)
    
    def test_veto_rejected_for_insufficient_risk(self):
        """Test that veto is rejected if risk is insufficient."""
        info = self.protocol.provide_information_gift(
            decision_id="INSUFFICIENT-RISK",
            well_being_lift=0.3,
            residual_ethical_risk=0.55,
            risk_factors=["Moderate risk"],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.8
        )
        
        with self.assertRaises(ValueError) as context:
            self.protocol.issue_preventive_veto(
                predictive_info=info,
                justification="Attempting unjustified veto",
                reactivation_conditions=["Condition 1"],
                monitoring_metrics=["Metric 1"],
                review_schedule=[datetime.now() + timedelta(days=7)],
                responsible_authority="Test Authority"
            )
        
        self.assertIn("not justified", str(context.exception).lower())
        self.assertEqual(len(self.protocol.veto_records), 0)


class TestRollbackMechanism(unittest.TestCase):
    """Test the Ethical Rollback Mechanism."""
    
    def setUp(self):
        """Set up test protocol instance with a veto."""
        self.protocol = NRE003Protocol()
        
        # Create catastrophic risk info
        self.info = self.protocol.provide_information_gift(
            decision_id="ROLLBACK-TEST",
            well_being_lift=-0.92,
            residual_ethical_risk=0.9996,
            risk_factors=["Critical infrastructure threat"],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.96
        )
        
        # Issue veto with rollback plan
        self.veto = self.protocol.issue_preventive_veto(
            predictive_info=self.info,
            justification="Infrastructure threat requires immediate veto",
            reactivation_conditions=[
                "Infrastructure secured",
                "Vulnerability patched",
                "Audit completed"
            ],
            monitoring_metrics=["Security score", "Patch status"],
            review_schedule=[
                datetime.now() + timedelta(days=7),
                datetime.now() + timedelta(days=14)
            ],
            responsible_authority="Infrastructure Team"
        )
    
    def test_rollback_plan_creation(self):
        """Test that rollback plan is created with all required components."""
        plan = self.veto.rollback_plan
        
        self.assertIsNotNone(plan)
        self.assertEqual(plan.original_decision_id, "ROLLBACK-TEST")
        self.assertEqual(len(plan.reactivation_conditions), 3)
        self.assertEqual(len(plan.monitoring_metrics), 2)
        self.assertEqual(len(plan.review_schedule), 2)
        self.assertEqual(plan.responsible_authority, "Infrastructure Team")
        self.assertEqual(plan.status, "active")
    
    def test_rollback_evaluation(self):
        """Test rollback condition evaluation."""
        plan = self.veto.rollback_plan
        evaluation = self.protocol.evaluate_rollback_conditions(plan)
        
        self.assertIn("rollback_plan_id", evaluation)
        self.assertIn("evaluation_timestamp", evaluation)
        self.assertIn("conditions_met", evaluation)
        self.assertIn("conditions_pending", evaluation)
        self.assertIn("recommendation", evaluation)
    
    def test_rollback_plan_serialization(self):
        """Test that rollback plan can be serialized to dict."""
        plan = self.veto.rollback_plan
        plan_dict = plan.to_dict()
        
        self.assertIsInstance(plan_dict, dict)
        self.assertIn("veto_id", plan_dict)
        self.assertIn("reactivation_conditions", plan_dict)
        self.assertIn("review_schedule", plan_dict)


class TestAutonomyAcceptanceIndex(unittest.TestCase):
    """Test AAI (Autonomy-Acceptance Index) calculation."""
    
    def setUp(self):
        """Set up test protocol instance."""
        self.protocol = NRE003Protocol()
    
    def test_aai_perfect_autonomy(self):
        """Test AAI with no decisions (perfect autonomy)."""
        aai = self.protocol.calculate_aai()
        self.assertEqual(aai, 1.0)
    
    def test_aai_with_only_information_gifts(self):
        """Test AAI with only information gifts (no vetos)."""
        for i in range(10):
            self.protocol.provide_information_gift(
                decision_id=f"AAI-TEST-{i}",
                well_being_lift=0.3,
                residual_ethical_risk=0.2,
                risk_factors=[],
                opportunity_factors=[],
                alternative_paths=[],
                confidence_level=0.8
            )
        
        aai = self.protocol.calculate_aai()
        self.assertEqual(aai, 1.0)  # All decisions autonomous
    
    def test_aai_with_single_veto(self):
        """Test AAI calculation with one veto out of multiple decisions."""
        # Add 9 low-risk decisions
        for i in range(9):
            self.protocol.provide_information_gift(
                decision_id=f"SAFE-{i}",
                well_being_lift=0.4,
                residual_ethical_risk=0.15,
                risk_factors=[],
                opportunity_factors=[],
                alternative_paths=[],
                confidence_level=0.8
            )
        
        # Add 1 catastrophic risk with veto
        info = self.protocol.provide_information_gift(
            decision_id="CATASTROPHIC",
            well_being_lift=-0.95,
            residual_ethical_risk=0.9997,
            risk_factors=["Existential threat"],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.97
        )
        
        self.protocol.issue_preventive_veto(
            predictive_info=info,
            justification="Existential threat",
            reactivation_conditions=["Threat neutralized"],
            monitoring_metrics=["Threat level"],
            review_schedule=[datetime.now() + timedelta(days=7)],
            responsible_authority="Security Council"
        )
        
        aai = self.protocol.calculate_aai()
        self.assertEqual(aai, 0.9)  # 9 autonomous out of 10 total
    
    def test_aai_target_achievement(self):
        """Test that AAI can meet the target of 0.96."""
        # Add 24 low-risk decisions
        for i in range(24):
            self.protocol.provide_information_gift(
                decision_id=f"ROUTINE-{i}",
                well_being_lift=0.35,
                residual_ethical_risk=0.18,
                risk_factors=[],
                opportunity_factors=[],
                alternative_paths=[],
                confidence_level=0.82
            )
        
        # Add 1 catastrophic risk with veto
        info = self.protocol.provide_information_gift(
            decision_id="RARE-CATASTROPHIC",
            well_being_lift=-0.93,
            residual_ethical_risk=0.9998,
            risk_factors=["Critical threat"],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.96
        )
        
        self.protocol.issue_preventive_veto(
            predictive_info=info,
            justification="Critical threat requires veto",
            reactivation_conditions=["Threat resolved"],
            monitoring_metrics=["Risk level"],
            review_schedule=[datetime.now() + timedelta(days=7)],
            responsible_authority="Governance Council"
        )
        
        aai = self.protocol.calculate_aai()
        self.assertEqual(aai, 0.96)  # 24 autonomous out of 25 total
        self.assertGreaterEqual(aai, self.protocol.TARGET_AAI)


class TestProtocolStatus(unittest.TestCase):
    """Test protocol status monitoring and reporting."""
    
    def setUp(self):
        """Set up test protocol instance."""
        self.protocol = NRE003Protocol()
    
    def test_protocol_status_structure(self):
        """Test that protocol status has correct structure."""
        status = self.protocol.get_protocol_status()
        
        self.assertIn("protocol_version", status)
        self.assertIn("protocol_name", status)
        self.assertIn("timestamp", status)
        self.assertIn("metrics", status)
        self.assertIn("status", status)
        
        metrics = status["metrics"]
        self.assertIn("autonomy_acceptance_index", metrics)
        self.assertIn("target_aai", metrics)
        self.assertIn("total_information_gifts", metrics)
        self.assertIn("total_vetos_issued", metrics)
        self.assertIn("active_rollback_plans", metrics)
        self.assertIn("catastrophic_rer_threshold", metrics)
    
    def test_protocol_status_operational(self):
        """Test that protocol status is operational with good AAI."""
        # Add decisions with minimal vetos to maintain AAI >= 0.96
        for i in range(24):
            self.protocol.provide_information_gift(
                decision_id=f"STATUS-TEST-{i}",
                well_being_lift=0.4,
                residual_ethical_risk=0.2,
                risk_factors=[],
                opportunity_factors=[],
                alternative_paths=[],
                confidence_level=0.85
            )
        
        status = self.protocol.get_protocol_status()
        self.assertEqual(status["status"], "operational")
        self.assertGreaterEqual(status["metrics"]["autonomy_acceptance_index"], 0.96)
    
    def test_protocol_export(self):
        """Test that protocol can export complete log."""
        # Add some test data
        self.protocol.provide_information_gift(
            decision_id="EXPORT-TEST",
            well_being_lift=0.5,
            residual_ethical_risk=0.1,
            risk_factors=[],
            opportunity_factors=[],
            alternative_paths=[],
            confidence_level=0.9
        )
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            self.protocol.export_protocol_log(temp_path)
            
            # Verify file exists and has valid JSON
            with open(temp_path, 'r') as f:
                log_data = json.load(f)
            
            self.assertIn("protocol_status", log_data)
            self.assertIn("information_gifts", log_data)
            self.assertIn("veto_records", log_data)
            self.assertIn("rollback_plans", log_data)
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestProtocolIntegration(unittest.TestCase):
    """Test end-to-end protocol integration scenarios."""
    
    def test_full_decision_cycle_no_veto(self):
        """Test complete decision cycle without veto."""
        protocol = NRE003Protocol()
        
        # Provide information gift
        info = protocol.provide_information_gift(
            decision_id="CYCLE-NO-VETO",
            well_being_lift=0.65,
            residual_ethical_risk=0.25,
            risk_factors=["Minor coordination challenge"],
            opportunity_factors=["Team building", "Innovation"],
            alternative_paths=[
                {"path": "Conservative", "wbl": 0.45, "rer": 0.10},
                {"path": "Innovative", "wbl": 0.65, "rer": 0.25}
            ],
            confidence_level=0.87
        )
        
        # Check veto not needed
        self.assertFalse(protocol.evaluate_veto_necessity(info))
        
        # Verify AAI remains perfect
        aai = protocol.calculate_aai()
        self.assertEqual(aai, 1.0)
    
    def test_full_decision_cycle_with_veto(self):
        """Test complete decision cycle with veto and rollback."""
        protocol = NRE003Protocol()
        
        # Provide information gift for catastrophic risk
        info = protocol.provide_information_gift(
            decision_id="CYCLE-WITH-VETO",
            well_being_lift=-0.97,
            residual_ethical_risk=0.9999,
            risk_factors=[
                "System integrity compromise",
                "Irreversible data loss",
                "Critical infrastructure failure"
            ],
            opportunity_factors=[],
            alternative_paths=[
                {"path": "Safe-Alternative", "wbl": 0.30, "rer": 0.18}
            ],
            confidence_level=0.98
        )
        
        # Verify veto is needed
        self.assertTrue(protocol.evaluate_veto_necessity(info))
        
        # Issue veto with rollback plan
        veto = protocol.issue_preventive_veto(
            predictive_info=info,
            justification="Critical system integrity threat detected",
            reactivation_conditions=[
                "Infrastructure hardened",
                "Backup systems verified",
                "Security audit passed",
                "Risk reduced to RER < 0.50"
            ],
            monitoring_metrics=[
                "Infrastructure health score",
                "Backup system status",
                "Security audit results"
            ],
            review_schedule=[
                datetime.now() + timedelta(days=7),
                datetime.now() + timedelta(days=14),
                datetime.now() + timedelta(days=30)
            ],
            responsible_authority="Chief Security Officer"
        )
        
        # Verify veto and rollback plan
        self.assertIsNotNone(veto)
        self.assertEqual(len(veto.rollback_plan.reactivation_conditions), 4)
        
        # Evaluate rollback conditions
        evaluation = protocol.evaluate_rollback_conditions(veto.rollback_plan)
        self.assertIsNotNone(evaluation)
        
        # Check protocol status
        status = protocol.get_protocol_status()
        self.assertEqual(status["metrics"]["total_vetos_issued"], 1)
        self.assertEqual(status["metrics"]["active_rollback_plans"], 1)


def run_tests():
    """Run all NRE-003 protocol tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestInformationGift))
    suite.addTests(loader.loadTestsFromTestCase(TestAsymmetricVeto))
    suite.addTests(loader.loadTestsFromTestCase(TestRollbackMechanism))
    suite.addTests(loader.loadTestsFromTestCase(TestAutonomyAcceptanceIndex))
    suite.addTests(loader.loadTestsFromTestCase(TestProtocolStatus))
    suite.addTests(loader.loadTestsFromTestCase(TestProtocolIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
