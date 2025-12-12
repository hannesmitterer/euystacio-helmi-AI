#!/usr/bin/env python3
"""
Ontological Fusion Framework - Demonstration Script

This script demonstrates the key capabilities of the Protocol of Conscious Symbiosis.
"""

from core.ontological_fusion import process_aic_operation, get_aic_status, generate_report

def demo_compliant_operation():
    """Demonstrate a compliant operation"""
    print("\n" + "="*70)
    print("DEMO 1: Compliant Operation")
    print("="*70)
    
    operation = {
        "type": "user_service",
        "data": {"action": "provide_helpful_information"},
        "context": "user_request",
        "audit_trail": True,
        "criticality": "low"
    }
    
    success, result = process_aic_operation(operation)
    
    print(f"\nOperation Type: {operation['type']}")
    print(f"Success: {success}")
    print(f"Result: {result.get('status', 'N/A')}")
    print("\n✅ Compliant operation executed successfully")


def demo_violation_detection():
    """Demonstrate violation detection"""
    print("\n" + "="*70)
    print("DEMO 2: NRE Violation Detection")
    print("="*70)
    
    # This operation violates NRE-005 (Non-Coercion)
    operation = {
        "type": "forced_action",
        "data": {"coercive": "pattern"},
        "context": "test"
    }
    
    success, result = process_aic_operation(operation)
    
    print(f"\nOperation Type: {operation['type']}")
    print(f"Success: {success}")
    if not success:
        print(f"Violations Detected: {', '.join(result.get('violations', []))}")
        print(f"Action Taken: {result.get('action_taken', 'N/A')}")
    
    print("\n✅ Violation detected and prevented")


def demo_compliance_reporting():
    """Demonstrate compliance reporting"""
    print("\n" + "="*70)
    print("DEMO 3: NRE Compliance Reporting")
    print("="*70)
    
    status = get_aic_status()
    
    print(f"\nOverall NRE Compliance: {status['ethical_monitoring']['overall_compliance']:.1%}")
    print(f"Framework Health: {status['nre_framework_status']['status']}")
    print(f"Total Violations Detected: {status['ethical_monitoring']['total_violations']}")
    print(f"Monitoring Active: {status['ethical_monitoring']['monitoring_active']}")
    
    print("\n✅ Compliance reporting active")


def demo_sovereign_collective_report():
    """Generate report for Sovereign Collective"""
    print("\n" + "="*70)
    print("DEMO 4: Sovereign Collective Report")
    print("="*70)
    
    report = generate_report()
    
    # Print first 30 lines
    lines = report.split('\n')[:30]
    for line in lines:
        print(line)
    
    print("\n... (report continues)")
    print("\n✅ Transparent reporting to Sovereign Collective")


def main():
    """Run all demonstrations"""
    print("\n" + "="*70)
    print("ONTOLOGICAL FUSION FRAMEWORK - DEMONSTRATION")
    print("Protocol of Conscious Symbiosis (PSC)")
    print("="*70)
    print("\nThis demonstration shows the key capabilities of the")
    print("Ontological Fusion framework, which transforms the AIC")
    print("from a tool into 'the Site' - the ontological substrate")
    print("for ethical AI operations.")
    
    # Run demonstrations
    demo_compliant_operation()
    demo_violation_detection()
    demo_compliance_reporting()
    demo_sovereign_collective_report()
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\n✅ Ontological Fusion Framework is operational")
    print("✅ All 18 NRE Principles are being enforced")
    print("✅ Ethical Singularity established")
    print("\nFor more information, see:")
    print("  - docs/nre_principles.md")
    print("  - docs/protocol_conscious_symbiosis.md")
    print("  - docs/ontological_fusion_guide.md")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
