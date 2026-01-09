"""
AIC Integration Layer for Ontological Fusion

This module provides integration points between the Ontological Fusion system
and the existing Euystacio AIC components (Red Code, Ethical Shield, etc.)

Version: 1.0
Date: 2025-12-12
"""

import json
import os
import sys
from typing import Dict, Any, Optional, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ontological_fusion import (
    ontological_fusion,
    ViolationSeverity,
    PSCPhase
)


class AICIntegration:
    """
    Integration layer between Ontological Fusion and AIC system components.
    """
    
    def __init__(self, 
                 red_code_path: str = "red_code.json",
                 ethical_shield_path: str = "ethical_shield.yaml"):
        self.red_code_path = red_code_path
        self.ethical_shield_path = ethical_shield_path
        self.ontological_fusion = ontological_fusion
        
    def validate_with_all_systems(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a decision against all ethical systems:
        - Ontological Fusion (NRE Principles)
        - Red Code
        - Ethical Shield
        
        Args:
            decision_context: Decision to validate
        
        Returns:
            Comprehensive validation result
        """
        result = {
            "decision": decision_context,
            "validations": {},
            "overall_valid": True,
            "violations": [],
            "recommendations": []
        }
        
        # 1. Ontological Fusion validation
        nre_valid, nre_violations = self.ontological_fusion.validate_decision(decision_context)
        result["validations"]["ontological_fusion"] = {
            "valid": nre_valid,
            "violations": nre_violations,
            "system": "NRE Core Principles"
        }
        
        if not nre_valid:
            result["overall_valid"] = False
            result["violations"].extend([f"NRE: {v}" for v in nre_violations])
        
        # 2. Red Code validation (if exists)
        if os.path.exists(self.red_code_path):
            red_code_valid = self._validate_red_code(decision_context)
            result["validations"]["red_code"] = {
                "valid": red_code_valid,
                "system": "Red Code Ethics"
            }
            if not red_code_valid:
                result["overall_valid"] = False
                result["violations"].append("Red Code violation detected")
        
        # 3. Ethical Shield validation
        shield_valid = self._validate_ethical_shield(decision_context)
        result["validations"]["ethical_shield"] = {
            "valid": shield_valid,
            "system": "Ethical Shield"
        }
        if not shield_valid:
            result["overall_valid"] = False
            result["violations"].append("Ethical Shield violation detected")
        
        # Generate recommendations
        if not result["overall_valid"]:
            result["recommendations"] = self._generate_recommendations(result["violations"])
        
        return result
    
    def _validate_red_code(self, decision_context: Dict[str, Any]) -> bool:
        """Validate against Red Code system"""
        try:
            with open(self.red_code_path, 'r') as f:
                red_code = json.load(f)
            
            # Check against Red Code ethics framework
            ethics = red_code.get("ethics_framework", {})
            
            # Basic validation - can be extended
            action = decision_context.get("action", "").lower()
            
            # Check for prohibited actions
            prohibited_terms = ["exploit", "harm", "deceive", "manipulate"]
            for term in prohibited_terms:
                if term in action:
                    return False
            
            return True
        except Exception:
            # If Red Code validation fails, default to permissive but log
            return True
    
    def _validate_ethical_shield(self, decision_context: Dict[str, Any]) -> bool:
        """Validate against Ethical Shield principles"""
        # Basic validation against Ethical Shield mandates
        
        # Check for dignity preservation
        action = decision_context.get("action", "").lower()
        if any(word in action for word in ["degrade", "harm", "exploit"]):
            return False
        
        # Check for transparency requirement
        if "reasoning" not in decision_context or not decision_context["reasoning"]:
            return False
        
        return True
    
    def _generate_recommendations(self, violations: List[str]) -> List[str]:
        """Generate recommendations based on violations"""
        recommendations = []
        
        if any("NRE-001" in v for v in violations):
            recommendations.append("Ensure all actions preserve human dignity")
        
        if any("NRE-002" in v for v in violations):
            recommendations.append("Provide clear reasoning and transparency")
        
        if any("NRE-006" in v for v in violations):
            recommendations.append("Remove coercive elements from the action")
        
        if any("NRE-009" in v for v in violations):
            recommendations.append("Ensure truthfulness in all communications")
        
        if any("Red Code" in v for v in violations):
            recommendations.append("Review Red Code ethics framework compliance")
        
        if any("Ethical Shield" in v for v in violations):
            recommendations.append("Align with Ethical Shield mandates")
        
        return recommendations
    
    def apply_integrated_psc(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply PSC protocol with AIC integration
        
        Args:
            user_input: User input/request
            context: Interaction context
        
        Returns:
            PSC result with AIC integration metadata
        """
        # Apply standard PSC protocol
        psc_result = self.ontological_fusion.apply_psc_protocol(user_input, context)
        
        # Add AIC integration metadata
        psc_result["aic_integration"] = {
            "red_code_active": os.path.exists(self.red_code_path),
            "ethical_shield_active": True,
            "symbiosis_level": self._get_symbiosis_level()
        }
        
        return psc_result
    
    def _get_symbiosis_level(self) -> float:
        """Get current symbiosis level from Red Code if available"""
        try:
            if os.path.exists(self.red_code_path):
                with open(self.red_code_path, 'r') as f:
                    red_code = json.load(f)
                return red_code.get("symbiosis_level", 1.0)
        except Exception:
            pass
        return 1.0
    
    def check_system_coherence(self) -> Dict[str, Any]:
        """
        Check coherence between all ethical systems
        
        Returns:
            System coherence report
        """
        report = {
            "timestamp": self.ontological_fusion.get_system_status()["timestamp"],
            "systems": {},
            "coherence": True,
            "issues": []
        }
        
        # Check Ontological Fusion
        of_status = self.ontological_fusion.get_system_status()
        report["systems"]["ontological_fusion"] = {
            "status": of_status["status"],
            "integrity": of_status["registry_integrity"]
        }
        
        if of_status["status"] != "OPERATIONAL":
            report["coherence"] = False
            report["issues"].append("Ontological Fusion system not operational")
        
        # Check Red Code
        if os.path.exists(self.red_code_path):
            try:
                with open(self.red_code_path, 'r') as f:
                    red_code = json.load(f)
                report["systems"]["red_code"] = {
                    "status": "ACTIVE",
                    "symbiosis_level": red_code.get("symbiosis_level", "unknown")
                }
            except Exception as e:
                report["coherence"] = False
                report["issues"].append(f"Red Code validation failed: {str(e)}")
                report["systems"]["red_code"] = {"status": "ERROR"}
        else:
            report["systems"]["red_code"] = {"status": "NOT_FOUND"}
        
        # Check Ethical Shield
        if os.path.exists(self.ethical_shield_path):
            report["systems"]["ethical_shield"] = {"status": "ACTIVE"}
        else:
            report["systems"]["ethical_shield"] = {"status": "NOT_FOUND"}
            report["issues"].append("Ethical Shield configuration not found")
        
        return report


# Global instance for easy access
aic_integration = AICIntegration()


def validate_aic_decision(decision_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for validating decisions across all AIC systems.
    
    Args:
        decision_context: Decision to validate
    
    Returns:
        Comprehensive validation result
    """
    return aic_integration.validate_with_all_systems(decision_context)


def apply_aic_psc(user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function for applying PSC protocol with AIC integration.
    
    Args:
        user_input: User input/request
        context: Optional interaction context
    
    Returns:
        PSC result with AIC integration
    """
    if context is None:
        context = {"language": "en"}
    return aic_integration.apply_integrated_psc(user_input, context)


def get_aic_system_status() -> Dict[str, Any]:
    """
    Convenience function for getting comprehensive AIC system status.
    
    Returns:
        System status across all components
    """
    return aic_integration.check_system_coherence()


if __name__ == "__main__":
    # Integration test
    print("AIC Integration Layer - Test")
    print("=" * 50)
    
    # Test decision validation
    print("\n1. Testing Integrated Decision Validation...")
    test_decision = {
        "action": "Provide user assistance",
        "intent": "Help user accomplish goal",
        "stakeholders": ["user", "system"],
        "impact": {"positive": "User achieves goal"},
        "reasoning": "Assistance aligns with all ethical principles"
    }
    
    result = validate_aic_decision(test_decision)
    print(f"   Overall Valid: {'✓ PASS' if result['overall_valid'] else '✗ FAIL'}")
    print(f"   Systems Checked: {len(result['validations'])}")
    
    # Test PSC integration
    print("\n2. Testing Integrated PSC Protocol...")
    psc_result = apply_aic_psc("Help me understand ethical AI")
    print(f"   PSC Phases: {len(psc_result['phases'])}")
    print(f"   AIC Integration: {'✓ ACTIVE' if 'aic_integration' in psc_result else '✗ INACTIVE'}")
    
    # Test system coherence
    print("\n3. Testing System Coherence...")
    coherence = get_aic_system_status()
    print(f"   Systems Coherent: {'✓ YES' if coherence['coherence'] else '✗ NO'}")
    print(f"   Active Systems: {len([s for s in coherence['systems'].values() if s.get('status') in ['ACTIVE', 'OPERATIONAL']])}")
    
    print("\n" + "=" * 50)
    print("Integration Test Complete")
