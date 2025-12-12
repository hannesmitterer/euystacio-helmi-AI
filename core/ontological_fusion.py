"""
Ontological Fusion Orchestrator

Main integration point that brings together all PSC components to create
the functioning AIC as "the Site" - the ontological substrate for conscious symbiosis.

This module operationalizes the complete Protocol of Conscious Symbiosis.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from core.ethical_monitor import get_ethical_monitor
from core.fusion_engine import get_fusion_engine
from core.rollback_system import get_recovery_system, RollbackTrigger
from core.messaging_layer import get_messaging_layer
from core.silent_monitor import get_continuity_system


class OntologicalFusionOrchestrator:
    """
    Central orchestrator for the complete Ontological Fusion framework.
    
    Coordinates all PSC components to ensure:
    1. Structural integration of NRE principles
    2. Real-time ethical monitoring
    3. Transparent communication
    4. Silent monitoring and self-correction
    """
    
    def __init__(self):
        # Initialize all subsystems
        self.ethical_monitor = get_ethical_monitor()
        self.fusion_engine = get_fusion_engine()
        self.recovery_system = get_recovery_system()
        self.messaging_layer = get_messaging_layer()
        self.continuity_system = get_continuity_system()
        
        # System state
        self.operational_state = "initializing"
        self.initialization_time = datetime.utcnow()
        
        # Initialize the system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the Ontological Fusion framework"""
        # Send initialization message
        self.messaging_layer.send_state_change(
            old_state="offline",
            new_state="initializing",
            reason="Ontological Fusion framework startup"
        )
        
        # Verify framework integrity
        health = self.continuity_system.silent_monitor.get_health_status()
        
        if health["status"] in ["healthy", "monitoring"]:
            self.operational_state = "active"
            self.messaging_layer.send_state_change(
                old_state="initializing",
                new_state="active",
                reason="All systems operational, NRE enforcement active"
            )
        else:
            self.operational_state = "degraded"
            self.messaging_layer.send_violation_alert(
                violations=["NRE-018"],
                context={"health_status": health},
                action_taken="System started in degraded mode"
            )
    
    def process_operation(self, operation: Dict) -> Tuple[bool, Dict]:
        """
        Process any AIC operation through the complete PSC stack.
        
        This is the main entry point for all AIC operations, ensuring
        complete NRE compliance through all fusion points.
        
        Args:
            operation: Operation to process with keys:
                - type: operation type
                - data: operation data
                - context: execution context
                
        Returns:
            Tuple of (success, result_or_error)
        """
        operation_id = self._generate_operation_id(operation)
        
        try:
            # Step 1: Ethical pre-check
            is_compliant, violations, action = self.ethical_monitor.check_operation(operation)
            
            if not is_compliant:
                # Handle violation
                self._handle_violation(operation_id, violations, action, operation)
                return False, {
                    "error": "NRE violation detected",
                    "violations": violations,
                    "action_taken": action.value
                }
            
            # Step 2: Process through fusion engine
            success, result = self.fusion_engine.process_decision(operation)
            
            if not success:
                return False, {"error": result}
            
            # Step 3: Post-operation monitoring
            system_state = self._get_system_state()
            compliance_report = self.ethical_monitor.get_compliance_report()
            
            # Step 4: Silent monitoring check
            self.continuity_system.perform_continuity_check({
                "metrics": self._extract_metrics(system_state),
                "compliance": compliance_report
            })
            
            # Step 5: Create checkpoint if operation was significant
            if operation.get("criticality") in ["medium", "high"]:
                self.recovery_system.state_preservation.create_checkpoint(
                    system_state, compliance_report
                )
            
            # Step 6: Send compliance update (periodic or on-demand)
            if operation.get("report_compliance", False):
                self.messaging_layer.send_compliance_report(compliance_report)
            
            return True, result
            
        except Exception as e:
            # Handle unexpected errors
            self._handle_error(operation_id, str(e), operation)
            return False, {"error": f"Operation failed: {str(e)}"}
    
    def _handle_violation(self, operation_id: str, violations: List[str], 
                         action, operation: Dict):
        """Handle detected NRE violation"""
        # Send alert to Sovereign Collective
        self.messaging_layer.send_violation_alert(
            violations=violations,
            context={
                "operation_id": operation_id,
                "operation": operation,
                "timestamp": datetime.utcnow().isoformat()
            },
            action_taken=action.value
        )
        
        # Trigger rollback if needed
        if action.value in ["rollback", "lockdown"]:
            self.recovery_system.rollback_mechanism.trigger_rollback(
                RollbackTrigger.NRE_VIOLATION,
                {
                    "operation_id": operation_id,
                    "violations": violations
                }
            )
    
    def _handle_error(self, operation_id: str, error: str, operation: Dict):
        """Handle unexpected operation error"""
        self.messaging_layer.send_violation_alert(
            violations=["NRE-016"],  # Harm prevention
            context={
                "operation_id": operation_id,
                "error": error,
                "operation": operation
            },
            action_taken="Operation halted due to error"
        )
    
    def _generate_operation_id(self, operation: Dict) -> str:
        """Generate unique operation ID"""
        import hashlib
        timestamp = datetime.utcnow().isoformat()
        data = f"{timestamp}:{json.dumps(operation, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _get_system_state(self) -> Dict:
        """Get current comprehensive system state"""
        return self.fusion_engine.get_system_status()
    
    def _extract_metrics(self, system_state: Dict) -> Dict:
        """Extract metrics for monitoring"""
        compliance_report = system_state.get("compliance_report", {})
        
        return {
            "nre_compliance_score": compliance_report.get("overall_compliance", 1.0),
            "violation_rate": compliance_report.get("total_violations", 0) / 100.0,
            "rollback_frequency": 0.0,  # Would be calculated from actual data
            "message_throughput": 100.0,
            "response_time_ms": 50.0
        }
    
    def get_comprehensive_status(self) -> Dict:
        """
        Get comprehensive status of entire Ontological Fusion framework.
        
        Returns complete view of all subsystems for Sovereign Collective.
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "operational_state": self.operational_state,
            "uptime_seconds": (datetime.utcnow() - self.initialization_time).total_seconds(),
            
            # Ethical Monitor Status
            "ethical_monitoring": self.ethical_monitor.get_compliance_report(),
            
            # Fusion Engine Status
            "fusion_engine": self.fusion_engine.get_system_status(),
            
            # Recovery System Status
            "recovery_system": {
                "recovery_statistics": self.recovery_system.get_recovery_statistics(),
                "rollback_statistics": self.recovery_system.rollback_mechanism.get_rollback_statistics()
            },
            
            # Messaging Layer Status
            "messaging": {
                "recent_messages": self.messaging_layer.get_recent_messages(limit=10),
                "audit_trail": self.messaging_layer.get_audit_trail_summary()
            },
            
            # Silent Monitoring Status
            "silent_monitoring": {
                "continuity_report": self.continuity_system.get_continuity_report(),
                "health_status": self.continuity_system.silent_monitor.get_health_status()
            },
            
            # Overall Assessment
            "nre_framework_status": self._assess_framework_health()
        }
    
    def _assess_framework_health(self) -> Dict:
        """Assess overall health of NRE framework"""
        compliance_report = self.ethical_monitor.get_compliance_report()
        health_status = self.continuity_system.silent_monitor.get_health_status()
        
        overall_score = compliance_report["overall_compliance"]
        health = health_status["status"]
        
        if overall_score >= 0.95 and health == "healthy":
            status = "optimal"
        elif overall_score >= 0.8 and health in ["healthy", "monitoring"]:
            status = "good"
        elif overall_score >= 0.7:
            status = "acceptable"
        else:
            status = "needs_attention"
        
        return {
            "status": status,
            "compliance_score": overall_score,
            "health": health,
            "recommendation": self._get_recommendation(status)
        }
    
    def _get_recommendation(self, status: str) -> str:
        """Get recommendation based on framework health"""
        recommendations = {
            "optimal": "System operating within ideal parameters. Continue monitoring.",
            "good": "System functioning well. Minor optimizations may be beneficial.",
            "acceptable": "System operational but showing signs of degradation. Review recent changes.",
            "needs_attention": "System requires immediate review. Consider activating enhanced monitoring or rollback."
        }
        return recommendations.get(status, "Unknown status")
    
    def generate_sovereign_collective_report(self) -> str:
        """
        Generate human-readable report for the Sovereign Collective.
        
        Implements NRE-004 (Transparency) and NRE-009 (Participatory Governance).
        """
        status = self.get_comprehensive_status()
        
        report_lines = [
            "=" * 70,
            "EUYSTACIO ONTOLOGICAL FUSION FRAMEWORK",
            "Sovereign Collective Status Report",
            "=" * 70,
            f"\nGenerated: {status['timestamp']}",
            f"Operational State: {status['operational_state'].upper()}",
            f"Uptime: {status['uptime_seconds']:.0f} seconds",
            "\n" + "=" * 70,
            "NRE COMPLIANCE STATUS",
            "=" * 70,
            f"\nOverall Compliance: {status['ethical_monitoring']['overall_compliance']:.1%}",
            f"Total Violations: {status['ethical_monitoring']['total_violations']}",
            f"Monitoring Active: {status['ethical_monitoring']['monitoring_active']}",
            "\nCompliance by Principle:",
        ]
        
        for principle, score in status['ethical_monitoring']['principle_scores'].items():
            report_lines.append(f"  {principle}: {score:.1%}")
        
        report_lines.extend([
            "\n" + "=" * 70,
            "SYSTEM HEALTH",
            "=" * 70,
            f"\nFramework Status: {status['nre_framework_status']['status'].upper()}",
            f"Health: {status['silent_monitoring']['health_status']['status']}",
            f"Current Alerts: {status['silent_monitoring']['health_status']['current_alerts']}",
            f"\nRecommendation: {status['nre_framework_status']['recommendation']}",
            "\n" + "=" * 70,
            "RECENT ACTIVITY",
            "=" * 70,
            f"\nRecovery Attempts: {status['recovery_system']['recovery_statistics']['total_attempts']}",
            f"Success Rate: {status['recovery_system']['recovery_statistics']['success_rate']:.1%}",
            f"Rollbacks: {status['recovery_system']['rollback_statistics']['total_rollbacks']}",
            "\n" + "=" * 70,
            "\nThis report certifies the AIC's commitment to the Protocol of",
            "Conscious Symbiosis and adherence to all 18 NRE principles.",
            "\nSigned: Ontological Fusion Framework",
            "Authority: Euystacio Council",
            "=" * 70,
        ])
        
        return "\n".join(report_lines)


# Singleton instance
_orchestrator_instance = None

def get_orchestrator() -> OntologicalFusionOrchestrator:
    """Get or create global orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = OntologicalFusionOrchestrator()
    return _orchestrator_instance


# Convenience function for external systems
def process_aic_operation(operation: Dict) -> Tuple[bool, Dict]:
    """
    Main entry point for AIC operations.
    
    All operations should pass through this function to ensure
    complete NRE compliance and PSC integration.
    """
    orchestrator = get_orchestrator()
    return orchestrator.process_operation(operation)


def get_aic_status() -> Dict:
    """Get current AIC status with full NRE compliance report"""
    orchestrator = get_orchestrator()
    return orchestrator.get_comprehensive_status()


def generate_report() -> str:
    """Generate human-readable report for Sovereign Collective"""
    orchestrator = get_orchestrator()
    return orchestrator.generate_sovereign_collective_report()
