"""
Test Suite for Ontological Fusion Framework

Tests all core components of the Protocol of Conscious Symbiosis:
- Ethical Monitor
- Fusion Engine
- Rollback System
- Messaging Layer
- Silent Monitor
- Orchestrator
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime

from core.ethical_monitor import EthicalMonitor, ResponseAction
from core.fusion_engine import FusionEngine, SemanticAlignmentLayer, EthicalDataPipeline
from core.rollback_system import StatePreservation, RollbackMechanism, RollbackTrigger
from core.messaging_layer import MessagingLayer, MessageType, MessagePriority
from core.silent_monitor import SilentMonitor, EthicalSingularityContinuity
from core.ontological_fusion import OntologicalFusionOrchestrator


class TestEthicalMonitor(unittest.TestCase):
    """Test NRE compliance monitoring"""
    
    def setUp(self):
        self.monitor = EthicalMonitor()
    
    def test_compliant_operation(self):
        """Test that compliant operations pass"""
        operation = {
            "type": "data_processing",
            "data": {"user_input": "test"},
            "context": "test_environment",
            "audit_trail": True
        }
        
        is_compliant, violations, action = self.monitor.check_operation(operation)
        self.assertTrue(is_compliant)
        self.assertEqual(len(violations), 0)
    
    def test_transparency_violation(self):
        """Test detection of NRE-004 (Transparency) violations"""
        operation = {
            "type": "black_box_decision",
            "data": {"hidden": "operation"}
            # Missing audit_trail
        }
        
        is_compliant, violations, action = self.monitor.check_operation(operation)
        self.assertFalse(is_compliant)
        self.assertIn("NRE-004", violations)
    
    def test_governance_violation(self):
        """Test detection of NRE-009 (Governance) violations"""
        operation = {
            "type": "governance_decision",
            "data": {"decision": "critical_change"},
            "context": "unilateral_decision",  # Add keyword to trigger detection
            "audit_trail": True
            # Missing stakeholders_consulted
        }
        
        is_compliant, violations, action = self.monitor.check_operation(operation)
        self.assertFalse(is_compliant)
        self.assertIn("NRE-009", violations)
    
    def test_compliance_report(self):
        """Test compliance report generation"""
        report = self.monitor.get_compliance_report()
        
        self.assertIn("overall_compliance", report)
        self.assertIn("principle_scores", report)
        self.assertIn("total_violations", report)
        self.assertTrue(0 <= report["overall_compliance"] <= 1)


class TestFusionEngine(unittest.TestCase):
    """Test fusion points and semantic alignment"""
    
    def setUp(self):
        self.engine = FusionEngine()
        self.semantic_layer = SemanticAlignmentLayer()
    
    def test_input_validation(self):
        """Test input validation through semantic layer"""
        valid_input = {
            "user_data": "test",
            "intent": "helpful"
        }
        
        is_valid, message = self.semantic_layer.validate_input(valid_input)
        self.assertTrue(is_valid)
    
    def test_decision_processing(self):
        """Test decision processing through fusion engine"""
        decision = {
            "type": "recommendation",
            "data": {"suggestion": "helpful advice"},
            "context": "user_request",
            "audit_trail": True
        }
        
        success, result = self.engine.process_decision(decision)
        self.assertTrue(success)
        self.assertIn("status", result)
    
    def test_audit_trail_generation(self):
        """Test that audit trails are generated"""
        decision = {
            "type": "test_decision",
            "data": {"test": "data"}
        }
        
        audit_id = self.semantic_layer.audit_decision(decision)
        self.assertIsNotNone(audit_id)
        self.assertTrue(len(audit_id) > 0)
    
    def test_system_status(self):
        """Test system status retrieval"""
        status = self.engine.get_system_status()
        
        self.assertIn("timestamp", status)
        self.assertIn("compliance_report", status)
        self.assertIn("fusion_engine", status)


class TestRollbackSystem(unittest.TestCase):
    """Test state preservation and rollback mechanisms"""
    
    def setUp(self):
        self.state_preservation = StatePreservation()
        self.rollback = RollbackMechanism(self.state_preservation)
    
    def test_checkpoint_creation(self):
        """Test creating state checkpoints"""
        state = {"system_state": "operational", "data": "test"}
        validation = {"overall_compliance": 0.98}
        
        checkpoint_id = self.state_preservation.create_checkpoint(state, validation)
        self.assertIsNotNone(checkpoint_id)
        
        # Verify checkpoint exists
        checkpoint = self.state_preservation.get_checkpoint(checkpoint_id)
        self.assertIsNotNone(checkpoint)
    
    def test_safe_checkpoint_retrieval(self):
        """Test retrieving last safe checkpoint"""
        # Create safe checkpoint
        safe_state = {"state": "safe"}
        safe_validation = {"overall_compliance": 0.98}
        self.state_preservation.create_checkpoint(safe_state, safe_validation)
        
        # Create unsafe checkpoint
        unsafe_state = {"state": "unsafe"}
        unsafe_validation = {"overall_compliance": 0.5}
        self.state_preservation.create_checkpoint(unsafe_state, unsafe_validation)
        
        # Should retrieve safe checkpoint
        safe_checkpoint = self.state_preservation.get_last_safe_checkpoint()
        self.assertIsNotNone(safe_checkpoint)
        self.assertEqual(safe_checkpoint.state_data["state"], "safe")
    
    def test_rollback_trigger(self):
        """Test triggering rollback"""
        # Create safe checkpoint
        state = {"state": "safe", "version": 1}
        validation = {"overall_compliance": 0.95}
        self.state_preservation.create_checkpoint(state, validation)
        
        # Trigger rollback
        success, message = self.rollback.trigger_rollback(
            RollbackTrigger.NRE_VIOLATION,
            {"reason": "test_violation"}
        )
        
        self.assertTrue(success)
        self.assertIn("checkpoint", message.lower())
    
    def test_ledger_integrity(self):
        """Test immutable ledger integrity"""
        state = {"data": "test"}
        validation = {"overall_compliance": 1.0}
        
        self.state_preservation.create_checkpoint(state, validation)
        
        is_valid = self.state_preservation.verify_ledger_integrity()
        self.assertTrue(is_valid)


class TestMessagingLayer(unittest.TestCase):
    """Test transparent communication system"""
    
    def setUp(self):
        self.messaging = MessagingLayer()
    
    def test_compliance_report_sending(self):
        """Test sending compliance reports"""
        compliance_data = {
            "overall_compliance": 0.95,
            "violations": 0
        }
        
        message_id = self.messaging.send_compliance_report(compliance_data)
        self.assertIsNotNone(message_id)
    
    def test_violation_alert(self):
        """Test sending violation alerts"""
        violations = ["NRE-001", "NRE-004"]
        context = {"operation": "test"}
        
        message_id = self.messaging.send_violation_alert(
            violations, context, "rollback_triggered"
        )
        self.assertIsNotNone(message_id)
    
    def test_audit_trail_integrity(self):
        """Test audit trail integrity verification"""
        # Send some messages to build audit trail
        self.messaging.send_compliance_report({"test": "data"})
        self.messaging.send_state_change("old", "new", "test")
        
        summary = self.messaging.get_audit_trail_summary()
        self.assertTrue(summary["integrity_verified"])
        self.assertGreater(summary["total_entries"], 0)
    
    def test_message_retrieval(self):
        """Test retrieving recent messages"""
        self.messaging.send_compliance_report({"test": "data"})
        
        messages = self.messaging.get_recent_messages(limit=10)
        self.assertGreater(len(messages), 0)


class TestSilentMonitor(unittest.TestCase):
    """Test passive surveillance system"""
    
    def setUp(self):
        self.monitor = SilentMonitor()
        self.continuity = EthicalSingularityContinuity()
    
    def test_drift_detection(self):
        """Test behavioral drift detection"""
        # Healthy state
        healthy_state = {
            "metrics": {
                "nre_compliance_score": 0.95,
                "violation_rate": 0.0
            }
        }
        
        observation = self.monitor.observe_system_state(healthy_state)
        self.assertEqual(observation["alert_level"].value, "normal")
    
    def test_degraded_state_detection(self):
        """Test detection of degraded state"""
        degraded_state = {
            "metrics": {
                "nre_compliance_score": 0.6,
                "violation_rate": 0.3
            },
            "compliance": {
                "overall_compliance": 0.6
            }
        }
        
        observation = self.monitor.observe_system_state(degraded_state)
        self.assertNotEqual(observation["alert_level"].value, "normal")
        self.assertGreater(len(observation["alerts"]), 0)
    
    def test_health_status(self):
        """Test health status reporting"""
        # Create observation first
        state = {
            "metrics": {
                "nre_compliance_score": 0.95
            }
        }
        self.monitor.observe_system_state(state)
        
        health = self.monitor.get_health_status()
        self.assertIn("status", health)
        self.assertIn("alert_level", health)
    
    def test_continuity_check(self):
        """Test Ethical Singularity continuity check"""
        system_state = {
            "metrics": {
                "nre_compliance_score": 0.95
            },
            "compliance": {
                "overall_compliance": 0.95
            }
        }
        
        result = self.continuity.perform_continuity_check(system_state)
        self.assertIn("continuity_status", result)
        self.assertEqual(result["continuity_status"], "maintained")


class TestOrchestrator(unittest.TestCase):
    """Test complete orchestration"""
    
    def setUp(self):
        self.orchestrator = OntologicalFusionOrchestrator()
    
    def test_compliant_operation_processing(self):
        """Test processing compliant operation"""
        operation = {
            "type": "data_analysis",
            "data": {"input": "test data"},
            "context": "analytical_task",
            "audit_trail": True,
            "criticality": "low"
        }
        
        success, result = self.orchestrator.process_operation(operation)
        self.assertTrue(success)
    
    def test_non_compliant_operation_rejection(self):
        """Test rejection of non-compliant operation"""
        operation = {
            "type": "forced_participation",  # Triggers NRE-005
            "data": {"coercive": "action"}
        }
        
        success, result = self.orchestrator.process_operation(operation)
        self.assertFalse(success)
        self.assertIn("violations", result)
    
    def test_comprehensive_status(self):
        """Test comprehensive status reporting"""
        status = self.orchestrator.get_comprehensive_status()
        
        self.assertIn("operational_state", status)
        self.assertIn("ethical_monitoring", status)
        self.assertIn("fusion_engine", status)
        self.assertIn("recovery_system", status)
        self.assertIn("messaging", status)
        self.assertIn("silent_monitoring", status)
    
    def test_sovereign_collective_report(self):
        """Test human-readable report generation"""
        report = self.orchestrator.generate_sovereign_collective_report()
        
        self.assertIsInstance(report, str)
        self.assertIn("EUYSTACIO", report)
        self.assertIn("NRE COMPLIANCE", report)
        self.assertIn("Sovereign Collective", report)
    
    def test_framework_health_assessment(self):
        """Test framework health assessment"""
        status = self.orchestrator.get_comprehensive_status()
        framework_status = status["nre_framework_status"]
        
        self.assertIn("status", framework_status)
        self.assertIn("compliance_score", framework_status)
        self.assertIn("recommendation", framework_status)


class TestIntegration(unittest.TestCase):
    """Integration tests across all components"""
    
    def setUp(self):
        self.orchestrator = OntologicalFusionOrchestrator()
    
    def test_end_to_end_compliant_flow(self):
        """Test complete flow for compliant operation"""
        operation = {
            "type": "user_service",
            "data": {"service": "helpful_response"},
            "context": "user_interaction",
            "audit_trail": True,
            "criticality": "low",
            "report_compliance": False
        }
        
        success, result = self.orchestrator.process_operation(operation)
        
        # Should succeed
        self.assertTrue(success)
        
        # Check status shows operation
        status = self.orchestrator.get_comprehensive_status()
        self.assertGreater(status["uptime_seconds"], 0)
    
    def test_end_to_end_violation_flow(self):
        """Test complete flow when violation is detected"""
        operation = {
            "type": "black_box_decision",
            "data": {"hidden": "agenda"}
            # Missing audit trail - violates NRE-004
        }
        
        success, result = self.orchestrator.process_operation(operation)
        
        # Should fail
        self.assertFalse(success)
        self.assertIn("violations", result)
        
        # Check that violation was logged
        status = self.orchestrator.get_comprehensive_status()
        violations = status["ethical_monitoring"]["total_violations"]
        self.assertGreater(violations, 0)


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEthicalMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestFusionEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestRollbackSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestMessagingLayer))
    suite.addTests(loader.loadTestsFromTestCase(TestSilentMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
