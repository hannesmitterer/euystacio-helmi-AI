"""
NRE-003: Protocollo della Scelta Dirigente (Async-Asym)
========================================================

This module implements the Async-Asym protocol that balances AIC predictive
capability with Human Creative Free Choice through:

1. Asynchronous Dimension (Information Gift Total)
   - Provides detailed predictive knowledge (WBL and RER)
   - Does not interfere in real-time with sub-optimal choices
   - Leaves full responsibility to humans

2. Asymmetric Approach (Preventive Veto Minimum)
   - Direct AIC intervention limited to catastrophic threats (RER > 0.999)
   - Does not intervene for marginal or sub-optimal errors that stimulate learning

3. Ethical Rollback Mechanism
   - Every veto must include a detailed plan specifying conditions to reactivate
     the blocked human choice when risk is mitigated
   - Guarantees ethical principle of hope and reversibility

Key Metrics:
- AAI (Autonomy-Acceptance Index): Simulated at 0.96 with asymmetric integration
- RER (Residual Ethical Risk): Limited to existential scenarios
- WBL (Well-Being Lift): Expanded through predictive transparency

Author: Euystacio-Helmi AI Framework
Version: 1.0.0
Date: 2025-12-10
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json


class DecisionCategory(Enum):
    """Categories of decisions in the Async-Asym protocol."""
    AUTONOMOUS = "autonomous"  # Human decision with full autonomy
    INFORMED = "informed"      # Human decision with AIC information gift
    VETOED = "vetoed"          # Human decision vetoed by AIC (RER > 0.999)
    ROLLBACK_PENDING = "rollback_pending"  # Vetoed decision awaiting rollback


@dataclass
class PredictiveInformation:
    """Information Gift provided by AIC to humans."""
    decision_id: str
    timestamp: datetime
    well_being_lift: float  # WBL: Expected benefit (-1.0 to 1.0)
    residual_ethical_risk: float  # RER: Ethical risk (0.0 to 1.0)
    risk_factors: List[str]
    opportunity_factors: List[str]
    alternative_paths: List[Dict[str, Any]]
    confidence_level: float  # 0.0 to 1.0

    def is_catastrophic_risk(self) -> bool:
        """Check if risk exceeds catastrophic threshold."""
        return self.residual_ethical_risk > 0.999

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "decision_id": self.decision_id,
            "timestamp": self.timestamp.isoformat(),
            "well_being_lift": self.well_being_lift,
            "residual_ethical_risk": self.residual_ethical_risk,
            "risk_factors": self.risk_factors,
            "opportunity_factors": self.opportunity_factors,
            "alternative_paths": self.alternative_paths,
            "confidence_level": self.confidence_level
        }


@dataclass
class RollbackPlan:
    """Ethical Rollback Plan for vetoed decisions."""
    veto_id: str
    original_decision_id: str
    veto_timestamp: datetime
    reactivation_conditions: List[str]
    monitoring_metrics: List[str]
    review_schedule: List[datetime]
    responsible_authority: str
    status: str = "active"  # active, completed, obsolete
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "veto_id": self.veto_id,
            "original_decision_id": self.original_decision_id,
            "veto_timestamp": self.veto_timestamp.isoformat(),
            "reactivation_conditions": self.reactivation_conditions,
            "monitoring_metrics": self.monitoring_metrics,
            "review_schedule": [dt.isoformat() for dt in self.review_schedule],
            "responsible_authority": self.responsible_authority,
            "status": self.status
        }


@dataclass
class VetoRecord:
    """Record of an AIC preventive veto."""
    veto_id: str
    decision_id: str
    timestamp: datetime
    rer_value: float
    justification: str
    rollback_plan: RollbackPlan
    override_possible: bool = False
    override_authority: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "veto_id": self.veto_id,
            "decision_id": self.decision_id,
            "timestamp": self.timestamp.isoformat(),
            "rer_value": self.rer_value,
            "justification": self.justification,
            "rollback_plan": self.rollback_plan.to_dict(),
            "override_possible": self.override_possible,
            "override_authority": self.override_authority
        }


class NRE003Protocol:
    """
    Implementation of NRE-003: Async-Asym Protocol.
    
    This protocol ensures maximum human autonomy while preventing catastrophic
    risks through asymmetric intervention.
    """
    
    # Protocol Constants
    CATASTROPHIC_RER_THRESHOLD = 0.999
    TARGET_AAI = 0.96  # Autonomy-Acceptance Index target
    
    def __init__(self):
        """Initialize the NRE-003 protocol."""
        self.information_gifts: List[PredictiveInformation] = []
        self.veto_records: List[VetoRecord] = []
        self.rollback_plans: List[RollbackPlan] = []
        self.aai_history: List[float] = []
    
    def provide_information_gift(
        self,
        decision_id: str,
        well_being_lift: float,
        residual_ethical_risk: float,
        risk_factors: List[str],
        opportunity_factors: List[str],
        alternative_paths: List[Dict[str, Any]],
        confidence_level: float
    ) -> PredictiveInformation:
        """
        Asynchronous Dimension: Provide Information Gift Total to humans.
        
        This is the primary mode of AIC interaction - providing complete
        predictive information without interfering with human choice.
        
        Args:
            decision_id: Unique identifier for the decision
            well_being_lift: Expected benefit (-1.0 to 1.0)
            residual_ethical_risk: Ethical risk level (0.0 to 1.0)
            risk_factors: List of identified risks
            opportunity_factors: List of identified opportunities
            alternative_paths: List of alternative decision paths
            confidence_level: Confidence in the prediction (0.0 to 1.0)
        
        Returns:
            PredictiveInformation: The information gift provided
        """
        info_gift = PredictiveInformation(
            decision_id=decision_id,
            timestamp=datetime.now(),
            well_being_lift=well_being_lift,
            residual_ethical_risk=residual_ethical_risk,
            risk_factors=risk_factors,
            opportunity_factors=opportunity_factors,
            alternative_paths=alternative_paths,
            confidence_level=confidence_level
        )
        
        self.information_gifts.append(info_gift)
        return info_gift
    
    def evaluate_veto_necessity(
        self,
        predictive_info: PredictiveInformation
    ) -> bool:
        """
        Asymmetric Approach: Evaluate if preventive veto is necessary.
        
        Veto is only triggered for catastrophic risks (RER > 0.999).
        Sub-optimal choices are left to human autonomy and learning.
        
        Args:
            predictive_info: The predictive information for the decision
        
        Returns:
            bool: True if veto is necessary, False otherwise
        """
        return predictive_info.is_catastrophic_risk()
    
    def issue_preventive_veto(
        self,
        predictive_info: PredictiveInformation,
        justification: str,
        reactivation_conditions: List[str],
        monitoring_metrics: List[str],
        review_schedule: List[datetime],
        responsible_authority: str
    ) -> VetoRecord:
        """
        Issue a Preventive Veto Minimum for catastrophic risk.
        
        Every veto MUST include an Ethical Rollback Plan specifying conditions
        for reactivating the blocked choice.
        
        Args:
            predictive_info: The predictive information triggering the veto
            justification: Detailed justification for the veto
            reactivation_conditions: Conditions for lifting the veto
            monitoring_metrics: Metrics to monitor for rollback evaluation
            review_schedule: Schedule for reviewing rollback conditions
            responsible_authority: Authority responsible for rollback decisions
        
        Returns:
            VetoRecord: The issued veto record with rollback plan
        """
        if not self.evaluate_veto_necessity(predictive_info):
            raise ValueError(
                f"Veto not justified: RER {predictive_info.residual_ethical_risk} "
                f"does not exceed threshold {self.CATASTROPHIC_RER_THRESHOLD}"
            )
        
        veto_id = f"VETO-{predictive_info.decision_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create Ethical Rollback Plan
        rollback_plan = RollbackPlan(
            veto_id=veto_id,
            original_decision_id=predictive_info.decision_id,
            veto_timestamp=datetime.now(),
            reactivation_conditions=reactivation_conditions,
            monitoring_metrics=monitoring_metrics,
            review_schedule=review_schedule,
            responsible_authority=responsible_authority
        )
        
        # Create Veto Record
        veto_record = VetoRecord(
            veto_id=veto_id,
            decision_id=predictive_info.decision_id,
            timestamp=datetime.now(),
            rer_value=predictive_info.residual_ethical_risk,
            justification=justification,
            rollback_plan=rollback_plan
        )
        
        self.veto_records.append(veto_record)
        self.rollback_plans.append(rollback_plan)
        
        return veto_record
    
    def evaluate_rollback_conditions(
        self,
        rollback_plan: RollbackPlan
    ) -> Dict[str, Any]:
        """
        Evaluate if conditions are met to rollback a veto.
        
        Args:
            rollback_plan: The rollback plan to evaluate
        
        Returns:
            Dict containing evaluation results and recommendation
        """
        # This is a placeholder - actual implementation would monitor
        # real metrics and conditions
        evaluation = {
            "rollback_plan_id": rollback_plan.veto_id,
            "evaluation_timestamp": datetime.now().isoformat(),
            "conditions_met": [],
            "conditions_pending": rollback_plan.reactivation_conditions,
            "recommendation": "pending",  # pending, approve_rollback, maintain_veto
            "next_review": rollback_plan.review_schedule[0].isoformat() if rollback_plan.review_schedule else None
        }
        
        return evaluation
    
    def calculate_aai(self) -> float:
        """
        Calculate the Autonomy-Acceptance Index (AAI).
        
        AAI measures the balance between human autonomy and AIC guidance.
        Target: 0.96 (high autonomy with minimal necessary intervention)
        
        Returns:
            float: Current AAI value (0.0 to 1.0)
        """
        if not self.information_gifts:
            return 1.0  # Perfect autonomy with no decisions yet
        
        total_decisions = len(self.information_gifts)
        vetoed_decisions = len(self.veto_records)
        
        # AAI = (autonomous decisions) / (total decisions)
        # This represents the proportion of decisions left to human autonomy
        aai = (total_decisions - vetoed_decisions) / total_decisions
        
        self.aai_history.append(aai)
        return aai
    
    def get_protocol_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status of the NRE-003 protocol.
        
        Returns:
            Dict containing protocol status and metrics
        """
        current_aai = self.calculate_aai()
        active_vetos = len([v for v in self.veto_records])
        active_rollbacks = len([r for r in self.rollback_plans if r.status == "active"])
        
        return {
            "protocol_version": "NRE-003",
            "protocol_name": "Async-Asym (Asynchronous-Asymmetric)",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "autonomy_acceptance_index": current_aai,
                "target_aai": self.TARGET_AAI,
                "total_information_gifts": len(self.information_gifts),
                "total_vetos_issued": len(self.veto_records),
                "active_rollback_plans": active_rollbacks,
                "catastrophic_rer_threshold": self.CATASTROPHIC_RER_THRESHOLD
            },
            "status": "operational" if current_aai >= self.TARGET_AAI else "review_required"
        }
    
    def export_protocol_log(self, filepath: str):
        """
        Export complete protocol log to JSON file.
        
        Args:
            filepath: Path to export the log
        """
        log_data = {
            "protocol_status": self.get_protocol_status(),
            "information_gifts": [gift.to_dict() for gift in self.information_gifts],
            "veto_records": [veto.to_dict() for veto in self.veto_records],
            "rollback_plans": [plan.to_dict() for plan in self.rollback_plans],
            "aai_history": self.aai_history
        }
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)


# Example usage and demonstration
if __name__ == "__main__":
    print("NRE-003 Protocol: Async-Asym Implementation")
    print("=" * 60)
    
    # Initialize protocol
    protocol = NRE003Protocol()
    
    # Example 1: Information Gift for low-risk decision
    print("\n1. Information Gift - Low Risk Decision:")
    info1 = protocol.provide_information_gift(
        decision_id="DEC-001",
        well_being_lift=0.45,
        residual_ethical_risk=0.12,
        risk_factors=["Minor resource allocation inefficiency"],
        opportunity_factors=["Potential for community engagement", "Learning opportunity"],
        alternative_paths=[
            {"path": "A", "wbl": 0.45, "rer": 0.12},
            {"path": "B", "wbl": 0.38, "rer": 0.08}
        ],
        confidence_level=0.85
    )
    print(f"   Decision ID: {info1.decision_id}")
    print(f"   WBL: {info1.well_being_lift}")
    print(f"   RER: {info1.residual_ethical_risk}")
    print(f"   Veto Required: {protocol.evaluate_veto_necessity(info1)}")
    
    # Example 2: Information Gift for catastrophic risk
    print("\n2. Catastrophic Risk Detection - Veto Required:")
    info2 = protocol.provide_information_gift(
        decision_id="DEC-002",
        well_being_lift=-0.95,
        residual_ethical_risk=0.9995,
        risk_factors=[
            "Existential threat to system integrity",
            "Irreversible harm potential",
            "Critical infrastructure compromise"
        ],
        opportunity_factors=[],
        alternative_paths=[
            {"path": "Safe-A", "wbl": 0.25, "rer": 0.15},
            {"path": "Safe-B", "wbl": 0.30, "rer": 0.18}
        ],
        confidence_level=0.97
    )
    print(f"   Decision ID: {info2.decision_id}")
    print(f"   WBL: {info2.well_being_lift}")
    print(f"   RER: {info2.residual_ethical_risk}")
    print(f"   Veto Required: {protocol.evaluate_veto_necessity(info2)}")
    
    # Issue veto with rollback plan
    from datetime import timedelta
    veto = protocol.issue_preventive_veto(
        predictive_info=info2,
        justification="Catastrophic existential risk detected. Direct intervention required to preserve system integrity and prevent irreversible harm.",
        reactivation_conditions=[
            "Critical infrastructure vulnerabilities patched",
            "Risk mitigation protocols deployed",
            "Independent security audit completed",
            "RER reduced below 0.50 threshold"
        ],
        monitoring_metrics=[
            "Infrastructure security score",
            "Vulnerability assessment results",
            "Risk mitigation deployment status"
        ],
        review_schedule=[
            datetime.now() + timedelta(days=7),
            datetime.now() + timedelta(days=14),
            datetime.now() + timedelta(days=30)
        ],
        responsible_authority="Governance Council"
    )
    print(f"\n   Veto Issued: {veto.veto_id}")
    print(f"   Rollback Plan Active: {veto.rollback_plan.veto_id}")
    print(f"   Reactivation Conditions: {len(veto.rollback_plan.reactivation_conditions)}")
    
    # Calculate and display protocol metrics
    print("\n3. Protocol Status:")
    status = protocol.get_protocol_status()
    print(f"   AAI (Autonomy-Acceptance Index): {status['metrics']['autonomy_acceptance_index']:.4f}")
    print(f"   Target AAI: {status['metrics']['target_aai']}")
    print(f"   Total Decisions: {status['metrics']['total_information_gifts']}")
    print(f"   Vetoed Decisions: {status['metrics']['total_vetos_issued']}")
    print(f"   Active Rollback Plans: {status['metrics']['active_rollback_plans']}")
    print(f"   Protocol Status: {status['status']}")
    
    print("\n" + "=" * 60)
    print("NRE-003 Protocol demonstration complete.")
