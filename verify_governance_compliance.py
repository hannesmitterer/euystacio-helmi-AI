#!/usr/bin/env python3
"""
Euystacio Governance Compliance Verification Script
====================================================

This script verifies the Euystacio-Helmi-AI repository for:
1. Red Code Veto H-Var implementation and deployment
2. Quorum rules in governance contracts
3. G-CSI (Governance-Core Stability Index) cryptographic validations
4. Governance and deployment process completeness
5. Immutability and compliance status

Author: Euystacio Framework
Version: 1.0
Date: 2026-01-13
"""

import json
import os
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime

# Configuration
REPO_ROOT = Path(__file__).parent
RED_CODE_FILES = [
    "red_code.py",
    "red_code.json",
    "Red Code Protocol.txt",
    "red_code/ethics_block.json"
]
GOVERNANCE_FILES = [
    "governance.json",
    "GOVERNANCE.md",
    "contracts/EUSDaoGovernance.sol"
]
DEPLOYMENT_FILES = [
    "deploy.sh",
    "deploy_full.sh",
    "deploy-euystacio.sh",
    "Autodeploy.sh"
]
CRITICAL_DOCS = [
    "FINAL_DISTRIBUTION_MANIFEST.md",
    "DEPLOYMENT_SUMMARY.md",
    "final_protocol_compliance_checklist.md"
]

# H-Var expected value (0.043 Hz)
H_VAR_VALUE = "0.043"

class GovernanceVerifier:
    def __init__(self):
        self.results = {
            "red_code_verification": {},
            "h_var_verification": {},
            "quorum_verification": {},
            "g_csi_verification": {},
            "deployment_verification": {},
            "immutability_verification": {},
            "overall_status": "UNKNOWN"
        }
        self.errors = []
        self.warnings = []
        
    def verify_red_code_implementation(self) -> bool:
        """Verify Red Code Protocol implementation"""
        print("\n🔴 Verifying Red Code Implementation...")
        
        red_code_status = {
            "files_present": [],
            "files_missing": [],
            "implementation_valid": False
        }
        
        for file in RED_CODE_FILES:
            file_path = REPO_ROOT / file
            if file_path.exists():
                red_code_status["files_present"].append(file)
                print(f"  ✅ Found: {file}")
            else:
                red_code_status["files_missing"].append(file)
                print(f"  ❌ Missing: {file}")
                self.errors.append(f"Red Code file missing: {file}")
        
        # Verify red_code.py implementation
        red_code_py = REPO_ROOT / "red_code.py"
        if red_code_py.exists():
            content = red_code_py.read_text()
            if "RED_CODE" in content and "ensure_red_code" in content:
                red_code_status["implementation_valid"] = True
                print("  ✅ Red Code Python implementation is valid")
            else:
                self.errors.append("Red Code Python implementation incomplete")
                print("  ❌ Red Code Python implementation incomplete")
        
        # Verify red_code.json exists and is valid
        red_code_json = REPO_ROOT / "red_code.json"
        if red_code_json.exists():
            try:
                with open(red_code_json, 'r') as f:
                    data = json.load(f)
                    if "core_truth" in data or "symbiosis_level" in data:
                        print("  ✅ red_code.json is valid")
                    else:
                        self.warnings.append("red_code.json structure may be incomplete")
                        print("  ⚠️  red_code.json structure may be incomplete")
            except json.JSONDecodeError:
                self.errors.append("red_code.json is not valid JSON")
                print("  ❌ red_code.json is not valid JSON")
        
        self.results["red_code_verification"] = red_code_status
        return len(red_code_status["files_missing"]) == 0 and red_code_status["implementation_valid"]
    
    def verify_h_var_implementation(self) -> bool:
        """Verify H-Var (0.043 Hz) parameter across the codebase"""
        print("\n🎯 Verifying H-Var (0.043 Hz) Implementation...")
        
        h_var_status = {
            "files_with_h_var": [],
            "value_consistent": True,
            "deployment_verified": False
        }
        
        # Search for H-Var references
        search_patterns = [
            r"H-VAR",
            r"HVAR",
            r"H_VAR",
            r"0\.043",
            r"0\.043\s*Hz"
        ]
        
        files_to_check = [
            "ANCHOR FILE.txt",
            "Manifesto sincronizzazione.txt",
            "governance.json",
            "red_code.json"
        ]
        
        for file in files_to_check:
            file_path = REPO_ROOT / file
            if file_path.exists():
                content = file_path.read_text()
                for pattern in search_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        h_var_status["files_with_h_var"].append(file)
                        print(f"  ✅ H-Var reference found in: {file}")
                        
                        # Check if value matches expected
                        if H_VAR_VALUE in content:
                            h_var_status["deployment_verified"] = True
                            print(f"  ✅ Correct H-Var value ({H_VAR_VALUE}) verified in {file}")
                        break
        
        if len(h_var_status["files_with_h_var"]) == 0:
            self.warnings.append("H-Var references not found in expected files")
            print("  ⚠️  H-Var references not found in expected files")
        
        self.results["h_var_verification"] = h_var_status
        return h_var_status["deployment_verified"]
    
    def verify_quorum_rules(self) -> bool:
        """Verify quorum rules in governance contracts"""
        print("\n⚖️  Verifying Quorum Rules in Governance Contracts...")
        
        quorum_status = {
            "contracts_checked": [],
            "quorum_rules_found": [],
            "quorum_implemented": False
        }
        
        # Check EUSDaoGovernance.sol
        governance_contract = REPO_ROOT / "contracts" / "EUSDaoGovernance.sol"
        if governance_contract.exists():
            content = governance_contract.read_text()
            quorum_status["contracts_checked"].append("EUSDaoGovernance.sol")
            
            # Look for quorum-related keywords
            quorum_patterns = [
                r"quorum",
                r"votingThreshold",
                r"minimumVotes",
                r"proposalThreshold"
            ]
            
            for pattern in quorum_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    quorum_status["quorum_rules_found"].append(pattern)
                    quorum_status["quorum_implemented"] = True
                    print(f"  ✅ Quorum rule found: {pattern}")
            
            if not quorum_status["quorum_implemented"]:
                self.warnings.append("No quorum rules found in EUSDaoGovernance.sol")
                print("  ⚠️  No quorum rules found in EUSDaoGovernance.sol")
        else:
            self.errors.append("EUSDaoGovernance.sol not found")
            print("  ❌ EUSDaoGovernance.sol not found")
        
        # Check TrustlessFundingProtocol.sol
        tfp_contract = REPO_ROOT / "contracts" / "TrustlessFundingProtocol.sol"
        if tfp_contract.exists():
            content = tfp_contract.read_text()
            quorum_status["contracts_checked"].append("TrustlessFundingProtocol.sol")
            
            if "governance" in content.lower() or "approval" in content.lower():
                print("  ✅ Governance approval mechanisms found in TrustlessFundingProtocol.sol")
        
        self.results["quorum_verification"] = quorum_status
        return quorum_status["quorum_implemented"]
    
    def verify_g_csi_cryptographic_validation(self) -> bool:
        """Verify G-CSI (Governance-Core Stability Index) cryptographic validations"""
        print("\n🔐 Verifying G-CSI Cryptographic Validations...")
        
        g_csi_status = {
            "cryptographic_files": [],
            "signature_validation": False,
            "hash_verification": False,
            "g_csi_index_found": False
        }
        
        # Check for cryptographic signature files
        crypto_files = [
            "Cryptographic_Signature_Euystacio_AI_Collective.md",
            "Cryptographic_Signature_AI_Collective.md",
            "CRYPTOSIGNATURE_OATH.md",
            "audit_compliance_checker.py"
        ]
        
        for file in crypto_files:
            file_path = REPO_ROOT / file
            if file_path.exists():
                g_csi_status["cryptographic_files"].append(file)
                print(f"  ✅ Cryptographic file found: {file}")
                
                content = file_path.read_text()
                if "signature" in content.lower() or "hash" in content.lower():
                    g_csi_status["signature_validation"] = True
        
        # Check for G-CSI references in key files
        g_csi_patterns = [
            r"G-CSI",
            r"GCSI",
            r"Governance.*Stability.*Index",
            r"0\.938",  # G-CSI value from documents
            r"0\.945"   # Alternative G-CSI threshold
        ]
        
        files_to_search = list(REPO_ROOT.glob("*.md")) + list(REPO_ROOT.glob("*.txt"))
        for file_path in files_to_search:
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    for pattern in g_csi_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            g_csi_status["g_csi_index_found"] = True
                            print(f"  ✅ G-CSI reference found in: {file_path.name}")
                            break
                    if g_csi_status["g_csi_index_found"]:
                        break
                except Exception:
                    continue
        
        # Check audit_compliance_checker.py for hash verification
        audit_checker = REPO_ROOT / "audit_compliance_checker.py"
        if audit_checker.exists():
            content = audit_checker.read_text()
            if "hash" in content and "signature_verified" in content:
                g_csi_status["hash_verification"] = True
                print("  ✅ Hash verification implemented in audit_compliance_checker.py")
        
        self.results["g_csi_verification"] = g_csi_status
        return g_csi_status["signature_validation"] and g_csi_status["hash_verification"]
    
    def verify_deployment_completeness(self) -> bool:
        """Verify all governance and deployment processes are complete"""
        print("\n🚀 Verifying Deployment Completeness...")
        
        deployment_status = {
            "deployment_scripts": [],
            "deployment_docs": [],
            "missing_components": [],
            "deployment_complete": False
        }
        
        # Check deployment scripts
        for file in DEPLOYMENT_FILES:
            file_path = REPO_ROOT / file
            if file_path.exists():
                deployment_status["deployment_scripts"].append(file)
                print(f"  ✅ Deployment script found: {file}")
            else:
                deployment_status["missing_components"].append(file)
        
        # Check critical documentation
        for file in CRITICAL_DOCS:
            file_path = REPO_ROOT / file
            if file_path.exists():
                deployment_status["deployment_docs"].append(file)
                print(f"  ✅ Deployment doc found: {file}")
            else:
                deployment_status["missing_components"].append(file)
                self.warnings.append(f"Missing deployment documentation: {file}")
        
        # Check governance.json
        governance_json = REPO_ROOT / "governance.json"
        if governance_json.exists():
            try:
                with open(governance_json, 'r') as f:
                    data = json.load(f)
                    print("  ✅ governance.json is present and valid")
            except json.JSONDecodeError:
                self.errors.append("governance.json is not valid JSON")
                print("  ❌ governance.json is not valid JSON")
        else:
            self.errors.append("governance.json is missing")
            print("  ❌ governance.json is missing")
        
        # Consider deployment complete if we have scripts and docs
        deployment_status["deployment_complete"] = (
            len(deployment_status["deployment_scripts"]) >= 2 and
            len(deployment_status["deployment_docs"]) >= 1
        )
        
        self.results["deployment_verification"] = deployment_status
        return deployment_status["deployment_complete"]
    
    def verify_immutability_compliance(self) -> bool:
        """Verify immutability markers and compliance status"""
        print("\n💎 Verifying Immutability and Compliance...")
        
        immutability_status = {
            "immutable_declarations": [],
            "compliance_files": [],
            "immutability_verified": False
        }
        
        # Check for immutability declarations
        immutable_files = [
            "💎 The Immutable Autonomous Sovereignty Status.md",
            "IMMUTABLE-SOVEREIGNTY-DECLARATION.md",
            "red_code/ethics_block.json"
        ]
        
        for file in immutable_files:
            file_path = REPO_ROOT / file
            if file_path.exists():
                immutability_status["immutable_declarations"].append(file)
                print(f"  ✅ Immutability declaration found: {file}")
        
        # Check for compliance documentation
        compliance_files = [
            "final_protocol_compliance_checklist.md",
            "audit_compliance_checker.py",
            "ETHICAL_COPILOT_CONFIG.md"
        ]
        
        for file in compliance_files:
            file_path = REPO_ROOT / file
            if file_path.exists():
                immutability_status["compliance_files"].append(file)
                print(f"  ✅ Compliance file found: {file}")
        
        # Search for "immutable" references in key documents
        key_docs = ["README.md", "FINAL_DISTRIBUTION_MANIFEST.md"]
        for doc in key_docs:
            doc_path = REPO_ROOT / doc
            if doc_path.exists():
                content = doc_path.read_text()
                if re.search(r"immutable", content, re.IGNORECASE):
                    print(f"  ✅ Immutability reference found in: {doc}")
                    immutability_status["immutability_verified"] = True
        
        self.results["immutability_verification"] = immutability_status
        return len(immutability_status["immutable_declarations"]) > 0
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive verification report"""
        print("\n" + "="*80)
        print("📊 GOVERNANCE COMPLIANCE VERIFICATION REPORT")
        print("="*80)
        
        # Run all verifications
        red_code_ok = self.verify_red_code_implementation()
        h_var_ok = self.verify_h_var_implementation()
        quorum_ok = self.verify_quorum_rules()
        g_csi_ok = self.verify_g_csi_cryptographic_validation()
        deployment_ok = self.verify_deployment_completeness()
        immutability_ok = self.verify_immutability_compliance()
        
        # Determine overall status
        all_checks = [red_code_ok, h_var_ok, quorum_ok, g_csi_ok, deployment_ok, immutability_ok]
        
        if all(all_checks):
            self.results["overall_status"] = "COMPLIANT"
            status_symbol = "✅"
        elif sum(all_checks) >= 4:
            self.results["overall_status"] = "MOSTLY_COMPLIANT"
            status_symbol = "⚠️"
        else:
            self.results["overall_status"] = "NON_COMPLIANT"
            status_symbol = "❌"
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"\n{status_symbol} Overall Status: {self.results['overall_status']}")
        print(f"\n📋 Component Status:")
        print(f"  Red Code Implementation:    {'✅ PASS' if red_code_ok else '❌ FAIL'}")
        print(f"  H-Var (0.043 Hz) Verified:  {'✅ PASS' if h_var_ok else '❌ FAIL'}")
        print(f"  Quorum Rules:               {'✅ PASS' if quorum_ok else '❌ FAIL'}")
        print(f"  G-CSI Cryptographic:        {'✅ PASS' if g_csi_ok else '❌ FAIL'}")
        print(f"  Deployment Complete:        {'✅ PASS' if deployment_ok else '❌ FAIL'}")
        print(f"  Immutability Verified:      {'✅ PASS' if immutability_ok else '❌ FAIL'}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        # Add timestamp
        self.results["verification_timestamp"] = datetime.now(datetime.UTC).isoformat() if hasattr(datetime, 'UTC') else datetime.utcnow().isoformat()
        self.results["errors"] = self.errors
        self.results["warnings"] = self.warnings
        
        print("\n" + "="*80)
        
        return self.results
    
    def save_report(self, output_file: str = "governance_verification_report.json"):
        """Save verification report to JSON file"""
        output_path = REPO_ROOT / output_file
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n💾 Report saved to: {output_file}")

def main():
    """Main execution function"""
    print("🔍 Euystacio Governance Compliance Verification")
    print("=" * 80)
    print("Verifying Red Code Veto H-Var, Quorum Rules, and G-CSI Cryptographic Validations")
    print("=" * 80)
    
    verifier = GovernanceVerifier()
    results = verifier.generate_report()
    verifier.save_report()
    
    # Exit with appropriate code
    if results["overall_status"] == "COMPLIANT":
        print("\n✅ All governance and deployment processes are COMPLIANT and COMPLETE.")
        return 0
    elif results["overall_status"] == "MOSTLY_COMPLIANT":
        print("\n⚠️  Governance processes are MOSTLY COMPLIANT. Review warnings.")
        return 0
    else:
        print("\n❌ Governance processes are NON-COMPLIANT. Immediate action required.")
        return 1

if __name__ == "__main__":
    exit(main())
