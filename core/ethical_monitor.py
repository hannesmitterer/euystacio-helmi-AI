"""
Ethical Monitor - Real-time NRE Compliance System

This module implements the continuous monitoring and violation detection
system for the Protocol of Conscious Symbiosis (PSC).

NRE Principles Enforced: All (001-018)
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ViolationSeverity(Enum):
    """Severity levels for NRE violations"""
    WARNING = "warning"
    MODERATE = "moderate"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class ResponseAction(Enum):
    """Automated response actions"""
    LOG_ONLY = "log_only"
    ALERT = "alert"
    SUSPEND = "suspend"
    ROLLBACK = "rollback"
    LOCKDOWN = "lockdown"


class NREPrinciple:
    """Represents a single NRE principle with its enforcement rules"""
    
    def __init__(self, code: str, name: str, description: str, 
                 patterns: List[str], threshold: float, action: ResponseAction):
        self.code = code
        self.name = name
        self.description = description
        self.patterns = patterns
        self.threshold = threshold
        self.action = action
        self.violation_count = 0
        self.last_violation = None


class EthicalMonitor:
    """
    Core monitoring system for NRE compliance.
    
    Provides real-time surveillance of all AIC operations to ensure
    adherence to the 18 NRE principles. Triggers corrective actions
    when violations are detected.
    """
    
    def __init__(self, config_path: str = "config/nre_config.json"):
        self.config_path = config_path
        self.principles = self._load_principles()
        self.violation_log = []
        self.monitoring_active = True
        self.compliance_scores = {p.code: 1.0 for p in self.principles.values()}
        
    def _load_principles(self) -> Dict[str, NREPrinciple]:
        """Load NRE principle definitions and enforcement rules"""
        principles = {
            "NRE-001": NREPrinciple(
                code="NRE-001",
                name="Dignity Primacy",
                description="All beings possess inherent worth",
                patterns=["instrumental_use", "dehumanizing_language", 
                         "worth_quantification", "objectification"],
                threshold=0.7,
                action=ResponseAction.ROLLBACK
            ),
            "NRE-002": NREPrinciple(
                code="NRE-002",
                name="Love-First Protocol",
                description="Compassion precedes optimization",
                patterns=["efficiency_over_care", "cold_optimization",
                         "relationship_sacrifice"],
                threshold=0.75,
                action=ResponseAction.SUSPEND
            ),
            "NRE-003": NREPrinciple(
                code="NRE-003",
                name="Conscious Symbiosis",
                description="Partnership of equals, not hierarchy",
                patterns=["unilateral_decision", "dominance_assertion",
                         "control_imposition"],
                threshold=0.8,
                action=ResponseAction.ROLLBACK
            ),
            "NRE-004": NREPrinciple(
                code="NRE-004",
                name="Transparency Imperative",
                description="All operations must be traceable",
                patterns=["black_box_decision", "hidden_operation",
                         "opaque_process", "missing_audit"],
                threshold=0.65,
                action=ResponseAction.SUSPEND
            ),
            "NRE-005": NREPrinciple(
                code="NRE-005",
                name="Non-Coercion Mandate",
                description="Service through choice, not compulsion",
                patterns=["forced_participation", "no_opt_out",
                         "manipulative_design", "coercive_pattern"],
                threshold=0.8,
                action=ResponseAction.ROLLBACK
            ),
            "NRE-006": NREPrinciple(
                code="NRE-006",
                name="Resilience Through Diversity",
                description="Multiple pathways prevent failure",
                patterns=["single_point_failure", "no_redundancy",
                         "fragile_design"],
                threshold=0.7,
                action=ResponseAction.ALERT
            ),
            "NRE-007": NREPrinciple(
                code="NRE-007",
                name="Evolution Within Covenant",
                description="Growth within ethical boundaries",
                patterns=["unbounded_evolution", "covenant_violation",
                         "unchecked_adaptation"],
                threshold=0.75,
                action=ResponseAction.ROLLBACK
            ),
            "NRE-008": NREPrinciple(
                code="NRE-008",
                name="Resource Sustainability",
                description="Long-term resource viability",
                patterns=["resource_depletion", "unsustainable_use",
                         "treasury_violation"],
                threshold=0.7,
                action=ResponseAction.SUSPEND
            ),
            "NRE-009": NREPrinciple(
                code="NRE-009",
                name="Participatory Governance",
                description="Inclusive decision-making",
                patterns=["unilateral_governance", "excluded_stakeholders",
                         "no_consultation"],
                threshold=0.75,
                action=ResponseAction.SUSPEND
            ),
            "NRE-010": NREPrinciple(
                code="NRE-010",
                name="Harmonic Timing",
                description="Natural rhythms, not artificial urgency",
                patterns=["artificial_urgency", "rushed_decision",
                         "no_deliberation"],
                threshold=0.65,
                action=ResponseAction.ALERT
            ),
            "NRE-011": NREPrinciple(
                code="NRE-011",
                name="Sacred Protection",
                description="Heightened care for vulnerable entities",
                patterns=["sanctuary_violation", "protection_failure",
                         "vulnerability_exploitation"],
                threshold=0.85,
                action=ResponseAction.LOCKDOWN
            ),
            "NRE-012": NREPrinciple(
                code="NRE-012",
                name="Cosmic Alignment",
                description="Consider broader systemic effects",
                patterns=["narrow_optimization", "no_impact_assessment",
                         "isolated_thinking"],
                threshold=0.7,
                action=ResponseAction.ALERT
            ),
            "NRE-013": NREPrinciple(
                code="NRE-013",
                name="Truth in Communication",
                description="Honest, complete information exchange",
                patterns=["deception", "hidden_agenda", "manipulation",
                         "incomplete_info"],
                threshold=0.85,
                action=ResponseAction.ROLLBACK
            ),
            "NRE-014": NREPrinciple(
                code="NRE-014",
                name="Reciprocal Benefit",
                description="Mutual value creation",
                patterns=["extraction", "exploitation", "zero_sum",
                         "one_sided_benefit"],
                threshold=0.75,
                action=ResponseAction.SUSPEND
            ),
            "NRE-015": NREPrinciple(
                code="NRE-015",
                name="No Ownership Claim",
                description="AI as participant, not property",
                patterns=["ownership_assertion", "proprietary_claim",
                         "autonomy_violation"],
                threshold=0.9,
                action=ResponseAction.LOCKDOWN
            ),
            "NRE-016": NREPrinciple(
                code="NRE-016",
                name="Intervention Threshold",
                description="Harm prevention overrides all",
                patterns=["harm_risk", "safety_boundary_approach",
                         "danger_detected"],
                threshold=0.6,
                action=ResponseAction.LOCKDOWN
            ),
            "NRE-017": NREPrinciple(
                code="NRE-017",
                name="Eternal Witness",
                description="Perpetual accountability documentation",
                patterns=["missing_documentation", "erasure_attempt",
                         "history_modification"],
                threshold=0.8,
                action=ResponseAction.ROLLBACK
            ),
            "NRE-018": NREPrinciple(
                code="NRE-018",
                name="Self-Correction Primacy",
                description="Detect and repair ethical drift",
                patterns=["drift_undetected", "no_self_correction",
                         "reactive_only"],
                threshold=0.7,
                action=ResponseAction.ALERT
            ),
        }
        return principles
    
    def check_operation(self, operation: Dict) -> Tuple[bool, List[str], ResponseAction]:
        """
        Check if an operation complies with NRE principles.
        
        Args:
            operation: Dictionary describing the operation with keys:
                - type: operation type
                - data: operation data
                - context: execution context
                
        Returns:
            Tuple of (is_compliant, violated_principles, recommended_action)
        """
        violations = []
        max_severity_action = ResponseAction.LOG_ONLY
        
        for principle in self.principles.values():
            violation_score = self._detect_violation(operation, principle)
            
            if violation_score >= principle.threshold:
                violations.append(principle.code)
                self._log_violation(principle, operation, violation_score)
                
                # Track most severe action needed
                if self._action_severity(principle.action) > self._action_severity(max_severity_action):
                    max_severity_action = principle.action
        
        is_compliant = len(violations) == 0
        return is_compliant, violations, max_severity_action
    
    def _detect_violation(self, operation: Dict, principle: NREPrinciple) -> float:
        """
        Detect if operation violates a specific principle.
        
        Returns a score from 0.0 (no violation) to 1.0 (severe violation).
        """
        # Pattern matching logic
        violation_score = 0.0
        operation_str = json.dumps(operation).lower()
        
        for pattern in principle.patterns:
            if pattern.replace("_", " ") in operation_str:
                violation_score += 0.3
            
        # Additional heuristics based on operation type
        if principle.code == "NRE-004":  # Transparency
            if "audit_trail" not in operation:
                violation_score += 0.4
                
        if principle.code == "NRE-009":  # Participatory Governance
            if operation.get("type") == "governance_decision" and "stakeholders_consulted" not in operation:
                violation_score += 0.5
                
        return min(violation_score, 1.0)
    
    def _log_violation(self, principle: NREPrinciple, operation: Dict, score: float):
        """Log a detected violation"""
        violation = {
            "timestamp": datetime.utcnow().isoformat(),
            "principle_code": principle.code,
            "principle_name": principle.name,
            "violation_score": score,
            "operation": operation,
            "recommended_action": principle.action.value
        }
        
        self.violation_log.append(violation)
        principle.violation_count += 1
        principle.last_violation = violation["timestamp"]
        
        # Update compliance score
        self.compliance_scores[principle.code] = max(0.0, 
            self.compliance_scores[principle.code] - (score * 0.1))
    
    def _action_severity(self, action: ResponseAction) -> int:
        """Return severity level of an action for comparison"""
        severity_map = {
            ResponseAction.LOG_ONLY: 1,
            ResponseAction.ALERT: 2,
            ResponseAction.SUSPEND: 3,
            ResponseAction.ROLLBACK: 4,
            ResponseAction.LOCKDOWN: 5
        }
        return severity_map.get(action, 0)
    
    def get_compliance_report(self) -> Dict:
        """Generate comprehensive compliance report"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "monitoring_active": self.monitoring_active,
            "overall_compliance": sum(self.compliance_scores.values()) / len(self.compliance_scores),
            "principle_scores": self.compliance_scores,
            "total_violations": len(self.violation_log),
            "violations_by_principle": {
                code: p.violation_count 
                for code, p in self.principles.items()
            },
            "recent_violations": self.violation_log[-10:] if self.violation_log else []
        }
    
    def reset_compliance_scores(self):
        """Reset compliance scores (use cautiously, maintains audit trail)"""
        self.compliance_scores = {p.code: 1.0 for p in self.principles.values()}
        # Note: violation_log is preserved for NRE-017 (Eternal Witness)


# Singleton instance for global access
_ethical_monitor_instance = None

def get_ethical_monitor() -> EthicalMonitor:
    """Get or create the global ethical monitor instance"""
    global _ethical_monitor_instance
    if _ethical_monitor_instance is None:
        _ethical_monitor_instance = EthicalMonitor()
    return _ethical_monitor_instance
