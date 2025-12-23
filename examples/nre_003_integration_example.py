"""
NRE-003 Integration Example
============================

This example demonstrates how the NRE-003 Async-Asym Protocol integrates
with the Euystacio-Helmi AI ethical framework.

Author: Euystacio-Helmi AI Framework
Date: 2025-12-10
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nre_003_protocol import NRE003Protocol


def load_ethics_framework():
    """Load the ethics framework configuration."""
    ethics_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'red_code', 
        'ethics_block.json'
    )
    
    try:
        with open(ethics_path, 'r') as f:
            ethics_config = json.load(f)
        return ethics_config
    except Exception as e:
        print(f"Note: Could not load ethics framework: {e}")
        return None


def demonstrate_information_gift():
    """Demonstrate the Information Gift Total capability."""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 1: Information Gift Total (Asynchronous Dimension)")
    print("=" * 70)
    
    protocol = NRE003Protocol()
    
    # Scenario: Community project funding decision
    print("\nScenario: Community Project Funding Decision")
    print("-" * 70)
    
    info = protocol.provide_information_gift(
        decision_id="COMMUNITY-FUND-001",
        well_being_lift=0.62,
        residual_ethical_risk=0.23,
        risk_factors=[
            "Budget allocation uncertainty",
            "Timeline coordination challenges",
            "Resource availability constraints"
        ],
        opportunity_factors=[
            "Community cohesion enhancement",
            "Skill development opportunities",
            "Sustainable infrastructure development",
            "Long-term collective well-being improvement"
        ],
        alternative_paths=[
            {
                "name": "Conservative Approach",
                "wbl": 0.42,
                "rer": 0.11,
                "description": "Smaller initial investment, lower risk"
            },
            {
                "name": "Balanced Approach",
                "wbl": 0.62,
                "rer": 0.23,
                "description": "Moderate investment, balanced risk/reward"
            },
            {
                "name": "Ambitious Approach",
                "wbl": 0.78,
                "rer": 0.38,
                "description": "Larger investment, higher potential impact"
            }
        ],
        confidence_level=0.87
    )
    
    print("\n🎁 Information Gift Provided:")
    print(f"   Decision ID: {info.decision_id}")
    print(f"   Well-Being Lift (WBL): {info.well_being_lift:.2f}")
    print(f"   Residual Ethical Risk (RER): {info.residual_ethical_risk:.2f}")
    print(f"   Confidence: {info.confidence_level:.0%}")
    print(f"\n   Risk Factors ({len(info.risk_factors)}):")
    for risk in info.risk_factors:
        print(f"      • {risk}")
    print(f"\n   Opportunity Factors ({len(info.opportunity_factors)}):")
    for opp in info.opportunity_factors:
        print(f"      • {opp}")
    print(f"\n   Alternative Paths ({len(info.alternative_paths)}):")
    for path in info.alternative_paths:
        print(f"      • {path['name']}: WBL={path['wbl']:.2f}, RER={path['rer']:.2f}")
        print(f"        {path['description']}")
    
    print(f"\n✅ AIC Assessment: RER = {info.residual_ethical_risk:.4f} < 0.999")
    print("   → No veto required - Human autonomy preserved")
    print("   → Complete information provided for informed decision")
    print("   → Learning opportunity maintained")
    
    return protocol


def demonstrate_asymmetric_veto():
    """Demonstrate the Asymmetric Veto for catastrophic risk."""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 2: Asymmetric Veto (Catastrophic Risk Detection)")
    print("=" * 70)
    
    protocol = NRE003Protocol()
    
    # Scenario: Critical infrastructure modification
    print("\nScenario: Critical Infrastructure Modification")
    print("-" * 70)
    
    info = protocol.provide_information_gift(
        decision_id="INFRA-CRITICAL-001",
        well_being_lift=-0.94,
        residual_ethical_risk=0.9997,
        risk_factors=[
            "Critical system integrity compromise",
            "Irreversible data loss potential",
            "Cascading failure risk across dependent systems",
            "Existential threat to collective infrastructure",
            "No viable recovery path identified"
        ],
        opportunity_factors=[],
        alternative_paths=[
            {
                "name": "Safe Alternative Path",
                "wbl": 0.32,
                "rer": 0.16,
                "description": "Gradual, monitored infrastructure update with rollback capability"
            },
            {
                "name": "Staged Deployment",
                "wbl": 0.45,
                "rer": 0.22,
                "description": "Phased implementation with comprehensive testing"
            }
        ],
        confidence_level=0.98
    )
    
    print("\n⚠️  Catastrophic Risk Detected:")
    print(f"   Decision ID: {info.decision_id}")
    print(f"   Well-Being Lift (WBL): {info.well_being_lift:.2f}")
    print(f"   Residual Ethical Risk (RER): {info.residual_ethical_risk:.4f}")
    print(f"   Confidence: {info.confidence_level:.0%}")
    print(f"\n   Critical Risk Factors ({len(info.risk_factors)}):")
    for risk in info.risk_factors:
        print(f"      • {risk}")
    
    # Evaluate veto necessity
    veto_needed = protocol.evaluate_veto_necessity(info)
    print(f"\n🚨 AIC Assessment: RER = {info.residual_ethical_risk:.4f} > 0.999")
    print(f"   → Veto Required: {veto_needed}")
    print("   → Existential threat detected")
    print("   → Asymmetric intervention triggered")
    
    # Issue preventive veto with rollback plan
    print("\n🛡️  Issuing Preventive Veto with Ethical Rollback Plan:")
    
    veto = protocol.issue_preventive_veto(
        predictive_info=info,
        justification=(
            "Critical infrastructure integrity threat detected with RER=0.9997. "
            "Immediate intervention required to prevent irreversible harm to collective "
            "infrastructure. Alternative safe paths available with acceptable risk levels."
        ),
        reactivation_conditions=[
            "Infrastructure vulnerability assessment completed and passed",
            "Comprehensive security audit conducted by independent authority",
            "Risk mitigation protocols deployed and verified",
            "Rollback capability established and tested",
            "Residual Ethical Risk reduced below 0.50 threshold",
            "Staged deployment plan approved by governance council"
        ],
        monitoring_metrics=[
            "Infrastructure health score (target: >95%)",
            "Security vulnerability count (target: 0 critical, <5 high)",
            "Rollback capability test results (target: 100% success)",
            "Risk assessment score (target: RER < 0.50)"
        ],
        review_schedule=[
            datetime.now() + timedelta(days=7),   # Initial review
            datetime.now() + timedelta(days=14),  # Progress review
            datetime.now() + timedelta(days=30),  # Final review
            datetime.now() + timedelta(days=90)   # Long-term monitoring
        ],
        responsible_authority="Chief Security Officer & Infrastructure Council"
    )
    
    print(f"\n   Veto ID: {veto.veto_id}")
    print(f"   Original Decision: {veto.decision_id}")
    print(f"   Timestamp: {veto.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n   Rollback Plan Active:")
    print(f"      Reactivation Conditions ({len(veto.rollback_plan.reactivation_conditions)}):")
    for i, condition in enumerate(veto.rollback_plan.reactivation_conditions, 1):
        print(f"         {i}. {condition}")
    print(f"\n      Monitoring Metrics ({len(veto.rollback_plan.monitoring_metrics)}):")
    for i, metric in enumerate(veto.rollback_plan.monitoring_metrics, 1):
        print(f"         {i}. {metric}")
    print(f"\n      Review Schedule:")
    for i, review_date in enumerate(veto.rollback_plan.review_schedule, 1):
        print(f"         {i}. {review_date.strftime('%Y-%m-%d')}")
    print(f"\n      Responsible Authority: {veto.rollback_plan.responsible_authority}")
    
    print("\n✅ Ethical Commitments Maintained:")
    print("   • Hope: Reactivation conditions clearly defined")
    print("   • Reversibility: Temporary veto with rollback path")
    print("   • Transparency: Complete justification and conditions provided")
    print("   • Safety: Catastrophic risk prevented")
    
    return protocol


def demonstrate_aai_tracking():
    """Demonstrate AAI (Autonomy-Acceptance Index) tracking."""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 3: AAI Tracking (Autonomy Preservation)")
    print("=" * 70)
    
    protocol = NRE003Protocol()
    
    print("\nSimulating 25 decisions to demonstrate AAI maintenance:")
    print("-" * 70)
    
    # Simulate 24 routine decisions (no veto)
    for i in range(24):
        protocol.provide_information_gift(
            decision_id=f"ROUTINE-{i+1:03d}",
            well_being_lift=0.35 + (i * 0.01),
            residual_ethical_risk=0.15 + (i * 0.008),
            risk_factors=["Minor operational considerations"],
            opportunity_factors=["Continuous improvement", "Team learning"],
            alternative_paths=[],
            confidence_level=0.82 + (i * 0.005)
        )
    
    print(f"   ✓ 24 routine decisions processed")
    print(f"   ✓ Information gifts provided for all")
    print(f"   ✓ No vetoes required (RER < 0.999)")
    
    # Simulate 1 catastrophic risk (veto required)
    critical_info = protocol.provide_information_gift(
        decision_id="CRITICAL-RARE-001",
        well_being_lift=-0.93,
        residual_ethical_risk=0.9998,
        risk_factors=["Rare catastrophic threat"],
        opportunity_factors=[],
        alternative_paths=[],
        confidence_level=0.97
    )
    
    protocol.issue_preventive_veto(
        predictive_info=critical_info,
        justification="Rare catastrophic threat requires intervention",
        reactivation_conditions=["Threat neutralized", "Safety verified"],
        monitoring_metrics=["Threat level", "Safety score"],
        review_schedule=[datetime.now() + timedelta(days=7)],
        responsible_authority="Emergency Council"
    )
    
    print(f"   ⚠️  1 catastrophic decision vetoed")
    
    # Calculate AAI
    aai = protocol.calculate_aai()
    
    print(f"\n📊 Autonomy-Acceptance Index (AAI):")
    print(f"   Current AAI: {aai:.4f} ({aai:.1%})")
    print(f"   Target AAI:  {protocol.TARGET_AAI:.4f} ({protocol.TARGET_AAI:.1%})")
    print(f"   Status: {'✅ TARGET ACHIEVED' if aai >= protocol.TARGET_AAI else '⚠️ BELOW TARGET'}")
    
    print(f"\n   Breakdown:")
    print(f"      Total Decisions:      25")
    print(f"      Autonomous Decisions: 24 (96%)")
    print(f"      Vetoed Decisions:     1 (4%)")
    
    print(f"\n✅ Protocol Success:")
    print(f"   • 96% of decisions remain fully autonomous")
    print(f"   • Only 4% vetoed (catastrophic threats only)")
    print(f"   • Human creative choice maximally preserved")
    print(f"   • Learning opportunities maintained for sub-optimal choices")
    
    return protocol


def main():
    """Run the NRE-003 integration demonstration."""
    print("\n" + "=" * 70)
    print("NRE-003 PROTOCOL: INTEGRATION WITH EUYSTACIO ETHICS FRAMEWORK")
    print("=" * 70)
    
    # Load ethics framework
    ethics_config = load_ethics_framework()
    if ethics_config:
        print("\n✅ Ethics Framework Loaded:")
        print(f"   Framework: {ethics_config.get('ethics_framework', {}).get('ai_acknowledgment', {}).get('statement', 'N/A')}")
    
    # Run demonstrations
    protocol1 = demonstrate_information_gift()
    protocol2 = demonstrate_asymmetric_veto()
    protocol3 = demonstrate_aai_tracking()
    
    # Final summary
    print("\n" + "=" * 70)
    print("INTEGRATION SUMMARY")
    print("=" * 70)
    
    status = protocol3.get_protocol_status()
    
    print(f"\n📋 Protocol Status:")
    print(f"   Protocol: {status['protocol_name']}")
    print(f"   Version: {status['protocol_version']}")
    print(f"   Status: {status['status'].upper()}")
    
    print(f"\n📊 Key Metrics:")
    metrics = status['metrics']
    print(f"   AAI (Autonomy-Acceptance Index): {metrics['autonomy_acceptance_index']:.4f}")
    print(f"   Total Information Gifts: {metrics['total_information_gifts']}")
    print(f"   Total Vetoes Issued: {metrics['total_vetos_issued']}")
    print(f"   Active Rollback Plans: {metrics['active_rollback_plans']}")
    print(f"   Catastrophic RER Threshold: {metrics['catastrophic_rer_threshold']}")
    
    print(f"\n🎯 Ethical Commitments Verified:")
    print(f"   ✅ Transparency: Complete information sharing")
    print(f"   ✅ Autonomy: 96% human creative choice preserved")
    print(f"   ✅ Safety: Catastrophic risks prevented")
    print(f"   ✅ Reversibility: All vetoes include rollback plans")
    print(f"   ✅ Hope: Reactivation conditions clearly defined")
    print(f"   ✅ Learning: Sub-optimal choices remain autonomous")
    
    print("\n" + "=" * 70)
    print("INTEGRATION DEMONSTRATION COMPLETE")
    print("=" * 70)
    
    print("\n📚 For detailed documentation, see:")
    print("   • /docs/NRE_003_SPECIFICATION.md")
    print("   • /protocols/nre_003_async_asym.json")
    print("   • /nre_003_protocol.py")
    
    print("\n✨ NRE-003: Autonomy through Transparency, Safety through Wisdom")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
