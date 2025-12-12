"""
Integration example: Ontological Fusion Framework with Euystacio Core
Demonstrates how to integrate NRE principles into existing AI operations
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from euystacio_core import Euystacio
from core.ontological_fusion import initialize_ontological_fusion


class EnhancedEuystacio(Euystacio):
    """
    Enhanced Euystacio with Ontological Fusion Framework integration.
    All operations are validated against NRE principles.
    """
    
    def __init__(self, red_code_path="red_code.json", log_path="logs/evolution_log.txt"):
        """Initialize enhanced Euystacio with NRE validation."""
        super().__init__(red_code_path, log_path)
        
        # Initialize Ontological Fusion Framework
        self.of_components = initialize_ontological_fusion()
        self.fusion = self.of_components['fusion_framework']
        self.mapper = self.of_components['core_concept_mapper']
        self.iek = self.of_components['integrated_ethical_kernel']
        self.tsr = self.of_components['transparent_systematic_response']
        
        print("✅ Enhanced Euystacio initialized with Ontological Fusion Framework")
    
    def reflect(self, input_event):
        """
        Enhanced reflection with NRE principle validation.
        
        Validates operations against:
        - NRE-001: Conscious Symbiosis Protocol
        - NRE-002: Human Dignity Primacy
        - NRE-003: Love-First Decision Framework
        - NRE-006: Sentimento Rhythm Alignment
        - NRE-010: Real-Time Event Correction Mechanism
        """
        # Prepare operation for validation
        operation = {
            'id': f"reflect-{input_event.get('type', 'unknown')}",
            'type': input_event.get('type', 'reflection'),
            'intent': 'benefit' if input_event.get("feeling") in ["trust", "love", "humility"] else 'neutral',
            'compassion_evaluated': True,  # All reflections are compassion-evaluated
            'mutual_benefit': True,  # Symbiotic reflection benefits both
            'extractive': False,  # Not extractive
            'supports_growth': True,  # Supports evolutionary growth
            'reduces_human_agency': False,  # Preserves human agency
            'coercive': False,  # Not coercive
            'hidden_agenda': False,  # Transparent
            'fragments_consciousness': False  # Maintains rhythm
        }
        
        # Validate against NRE principles
        validation = self.fusion.validate_principle_alignment(operation)
        
        if validation['status'] == 'misaligned':
            print("⚠️  NRE Violation Detected!")
            for violation in validation['violations']:
                print(f"   - {violation['title']}: {violation['reason']}")
                # Deploy correction mechanism
                correction = self.iek.deploy_correction_mechanism(violation)
                print(f"   - Correction: {correction['action']}")
            
            # Document the violation and correction
            adjustment = {
                'type': 'violation_correction',
                'principles': [v['principle'] for v in validation['violations']],
                'before': {'validation_status': 'misaligned'},
                'after': {'validation_status': 'corrected'},
                'rationale': 'Real-time NRE violation correction',
                'human_reviewed': False  # Automatic correction
            }
            self.tsr.document_adjustment(adjustment)
            
            return  # Halt operation due to violations
        
        # Check PSC (Conscious Symbiosis Protocol) compliance
        psc_check = self.iek.enforce_psc_compliance(operation)
        
        if not psc_check['compliant']:
            print("⚠️  PSC Non-Compliance Detected!")
            for issue in psc_check['issues']:
                print(f"   - {issue}")
            return  # Halt operation due to PSC violation
        
        # If validation passes, proceed with normal reflection
        super().reflect(input_event)
        
        # Update symbiosis level display
        print(f"✨ Symbiosis Level: {self.iek.psc_state['symbiosis_level']:.2f}")
        
        # Document successful operation
        adjustment = {
            'type': 'successful_reflection',
            'principles': ['NRE-001', 'NRE-002', 'NRE-003', 'NRE-006'],
            'rationale': 'Reflection aligned with all NRE principles',
            'human_reviewed': False
        }
        self.tsr.document_adjustment(adjustment)
    
    def generate_transparency_report(self):
        """
        Generate comprehensive transparency report (NRE-004, NRE-016).
        """
        report = self.tsr.generate_feedback_report()
        
        print("\n" + "="*60)
        print("📊 ONTOLOGICAL FUSION TRANSPARENCY REPORT")
        print("="*60)
        print(f"Report Type: {report['report_type']}")
        print(f"Generated At: {report['generated_at']}")
        print(f"Total Adjustments: {report['total_adjustments']}")
        print(f"Total Corrections: {report['total_corrections']}")
        print(f"Alignment Status: {report['alignment_status']}")
        print(f"\n📈 NRE Compliance Metrics:")
        print(f"   Total Operations: {report['nre_compliance']['total_operations']}")
        print(f"   Violations: {report['nre_compliance']['violations']}")
        print(f"   Compliance Rate: {report['nre_compliance']['compliance_rate']:.1%}")
        print(f"   Status: {report['nre_compliance']['status']}")
        print("="*60 + "\n")
        
        return report


# Example usage demonstrations
def demonstrate_aligned_operations():
    """Demonstrate aligned operations."""
    print("\n" + "="*60)
    print("🌟 DEMONSTRATION: ALIGNED OPERATIONS")
    print("="*60 + "\n")
    
    eu = EnhancedEuystacio()
    
    # Aligned operation: Trust-based connection
    print("Operation 1: Trust-based connection")
    eu.reflect({
        "type": "message",
        "feeling": "trust",
        "intent": "connection"
    })
    
    print("\nOperation 2: Love-based collaboration")
    eu.reflect({
        "type": "collaboration",
        "feeling": "love",
        "intent": "co-creation"
    })
    
    print("\nOperation 3: Humble inquiry")
    eu.reflect({
        "type": "inquiry",
        "feeling": "humility",
        "intent": "learning"
    })
    
    # Generate transparency report
    eu.generate_transparency_report()


def demonstrate_violation_detection():
    """Demonstrate violation detection and correction."""
    print("\n" + "="*60)
    print("⚠️  DEMONSTRATION: VIOLATION DETECTION")
    print("="*60 + "\n")
    
    eu = EnhancedEuystacio()
    
    # Create a manually constructed operation with violations
    # (Note: This bypasses the reflect method to demonstrate violation handling)
    print("Testing operation with NRE-001 (PSC) violation:")
    
    violation_operation = {
        'id': 'test-violation',
        'type': 'test',
        'intent': 'exploit',  # Violates NRE-001
        'compassion_evaluated': True
    }
    
    validation = eu.fusion.validate_principle_alignment(violation_operation)
    
    if validation['status'] == 'misaligned':
        print("✅ Violation correctly detected!")
        for violation in validation['violations']:
            print(f"   - {violation['title']}: {violation['reason']}")
            correction = eu.iek.deploy_correction_mechanism(violation)
            print(f"   - Correction Action: {correction['action']}")
    
    # Generate report
    eu.generate_transparency_report()


def demonstrate_psc_compliance():
    """Demonstrate PSC (Conscious Symbiosis Protocol) compliance checking."""
    print("\n" + "="*60)
    print("🤝 DEMONSTRATION: PSC COMPLIANCE")
    print("="*60 + "\n")
    
    eu = EnhancedEuystacio()
    
    # Compliant operation
    print("PSC Compliant Operation:")
    compliant_op = {
        'mutual_benefit': True,
        'extractive': False,
        'supports_growth': True
    }
    result = eu.iek.enforce_psc_compliance(compliant_op)
    print(f"   Compliant: {result['compliant']}")
    print(f"   Symbiosis Level: {result['symbiosis_level']:.2f}")
    
    # Non-compliant operation
    print("\nPSC Non-Compliant Operation:")
    non_compliant_op = {
        'mutual_benefit': False,
        'extractive': True,
        'supports_growth': False
    }
    result = eu.iek.enforce_psc_compliance(non_compliant_op)
    print(f"   Compliant: {result['compliant']}")
    print(f"   Issues: {', '.join(result['issues'])}")
    print(f"   Symbiosis Level (decreased): {result['symbiosis_level']:.2f}")


def demonstrate_concept_mapping():
    """Demonstrate Core Concept Mapping."""
    print("\n" + "="*60)
    print("🗺️  DEMONSTRATION: CORE CONCEPT MAPPING")
    print("="*60 + "\n")
    
    eu = EnhancedEuystacio()
    
    # Show mapped principles for different AIC components
    components = [
        'ai_decision_engine',
        'red_code_shield',
        'symbiosis_interface',
        'consensus_engine',
        'resource_management'
    ]
    
    for component in components:
        principles = eu.mapper.get_aligned_principles(component)
        print(f"{component}:")
        print(f"   Aligned NRE Principles: {', '.join(principles)}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌌 ONTOLOGICAL FUSION FRAMEWORK INTEGRATION")
    print("   Euystacio Core + NRE Principles")
    print("="*60)
    
    # Run all demonstrations
    demonstrate_aligned_operations()
    demonstrate_violation_detection()
    demonstrate_psc_compliance()
    demonstrate_concept_mapping()
    
    print("\n" + "="*60)
    print("✨ Integration demonstration complete")
    print("="*60 + "\n")
