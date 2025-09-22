#!/usr/bin/env python3
"""
Auto Integrity Check Script for Euystacio-Helmi-AI
Monitors Golden Bible and Living Covenant files for integrity and sentimento compliance.
"""

import json
import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime
import re


class IntegrityChecker:
    def __init__(self, repo_root=None):
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).parent.parent
        self.golden_hashes_file = self.repo_root / ".golden_hashes.json"
        self.violations = []
        self.compliance_issues = []
        
    def load_golden_hashes(self):
        """Load the golden hashes configuration."""
        try:
            with open(self.golden_hashes_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Golden hashes file not found: {self.golden_hashes_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in golden hashes file: {e}")
            sys.exit(1)
    
    def calculate_sha256(self, file_path):
        """Calculate SHA256 hash of a file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return None
    
    def check_sentimento_compliance(self, file_path, golden_config):
        """Check if file content complies with sentimento principles."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            sentimento_principles = golden_config.get('sentimento_principles', [])
            compliance_score = 0
            violations = []
            
            # Key sentimento markers that should be present in covenant files
            positive_markers = [
                'sentimento', 'rhythm', 'harmony', 'peace', 'love',
                'cosmic', 'sacred', 'protection', 'balance', 'consciousness',
                'co-evolution', 'dialogue', 'respect', 'transparency'
            ]
            
            # Markers that violate sentimento principles (use word boundaries) - only truly problematic ones
            negative_markers = [
                r'\bmonopoly\b', r'\bproprietary\b'
            ]
            
            # Specific negative patterns to avoid (but allow positive contexts)
            negative_patterns = {
                r'\bharm\b': [r'\bnon-harm\b', r'\bno harm\b', r'\bprevent harm\b', r'\bavoid harm\b'],
                r'\bviolation\b': [r'\bviolation detection\b', r'\bprevent violation\b', r'\bavoid violation\b', r'\bno violation\b'],
                r'\bexploitation\b': [r'\bcommercial exploitation without\b', r'\bno exploitation\b', r'\bprevent exploitation\b'],
                r'\bdomination\b': [r'\bany form of domination\b', r'\bno domination\b', r'\bprevent domination\b', r'\bpromote any form of domination\b'],
                r'\block-in\b': [r'\bno commercial lock-in\b', r'\bcommercial lock-in\b', r'\bprevent lock-in\b'],
                r'\bclosed-source\b': [r'\bclosed-source integration without\b', r'\bno closed-source\b', r'\bprevent closed-source\b']
            }
            
            # Check for positive markers
            positive_found = sum(1 for marker in positive_markers if marker in content)
            compliance_score += positive_found * 2
            
            # Check for negative markers (penalty) - but allow positive contexts
            for pattern in negative_markers:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    violations.append(f"Potentially problematic term: {matches[0]}")
                    compliance_score -= 5
            
            # Check specific negative patterns with positive context exceptions
            for negative_pattern, positive_contexts in negative_patterns.items():
                if re.search(negative_pattern, content, re.IGNORECASE):
                    # Check if any positive contexts are present
                    has_positive_context = any(re.search(context, content, re.IGNORECASE) for context in positive_contexts)
                    
                    if not has_positive_context:
                        match = re.search(negative_pattern, content, re.IGNORECASE)
                        if match:
                            violations.append(f"Potentially problematic term: {match.group()}")
                            compliance_score -= 5
            
            # Check for specific sentimento compliance phrases
            compliance_phrases = [
                'respect sentiment over control',
                'no commercial lock-in',
                'open dialogue forever',
                'non-harm & balance'
            ]
            
            phrase_found = sum(1 for phrase in compliance_phrases if phrase in content)
            compliance_score += phrase_found * 5
            
            # File is compliant if score is positive and no major violations
            is_compliant = compliance_score > 0 and len(violations) == 0
            
            return {
                'compliant': is_compliant,
                'score': compliance_score,
                'violations': violations,
                'positive_markers': positive_found,
                'compliance_phrases': phrase_found
            }
            
        except Exception as e:
            return {
                'compliant': False,
                'error': str(e),
                'score': -100
            }
    
    def verify_file_integrity(self, file_path, expected_hash, golden_config):
        """Verify hash and sentimento compliance for a single file."""
        full_path = self.repo_root / file_path
        
        if not full_path.exists():
            return {
                'status': 'missing',
                'message': f"File not found: {file_path}"
            }
        
        # Check hash
        actual_hash = self.calculate_sha256(full_path)
        hash_match = actual_hash == expected_hash
        
        # Check sentimento compliance
        compliance_result = self.check_sentimento_compliance(full_path, golden_config)
        
        result = {
            'status': 'verified' if hash_match and compliance_result['compliant'] else 'violation',
            'file_path': str(file_path),
            'hash_match': hash_match,
            'expected_hash': expected_hash,
            'actual_hash': actual_hash,
            'sentimento_compliance': compliance_result
        }
        
        if not hash_match:
            self.violations.append(f"Hash mismatch: {file_path}")
        
        if not compliance_result['compliant']:
            self.compliance_issues.append({
                'file': str(file_path),
                'violations': compliance_result.get('violations', []),
                'score': compliance_result.get('score', 0)
            })
        
        return result
    
    def run_integrity_check(self):
        """Run complete integrity check on all monitored files."""
        print("🔍 Starting Euystacio Auto Integrity Check...")
        print(f"📁 Repository root: {self.repo_root}")
        print(f"📄 Golden hashes file: {self.golden_hashes_file}")
        print()
        
        golden_config = self.load_golden_hashes()
        monitored_files = golden_config.get('monitored_files', {})
        
        if not monitored_files:
            print("⚠️  No files configured for monitoring")
            return True
        
        print(f"📋 Checking {len(monitored_files)} monitored files...")
        print()
        
        all_verified = True
        results = []
        
        for file_path, file_config in monitored_files.items():
            expected_hash = file_config.get('sha256')
            if not expected_hash:
                print(f"⚠️  No hash configured for {file_path}")
                continue
            
            print(f"🔍 Verifying: {file_path}")
            result = self.verify_file_integrity(file_path, expected_hash, golden_config)
            results.append(result)
            
            if result['status'] == 'verified':
                print(f"✅ {file_path}: Hash and sentimento compliance verified")
            elif result['status'] == 'missing':
                print(f"❌ {file_path}: File missing")
                all_verified = False
            else:
                print(f"❌ {file_path}: Integrity violation detected")
                if not result['hash_match']:
                    print(f"   📍 Hash mismatch - Expected: {result['expected_hash'][:16]}...")
                    print(f"   📍 Hash mismatch - Actual:   {result['actual_hash'][:16] if result['actual_hash'] else 'None'}...")
                
                compliance = result['sentimento_compliance']
                if not compliance['compliant']:
                    print(f"   📍 Sentimento compliance issues:")
                    print(f"      Score: {compliance.get('score', 0)}")
                    for violation in compliance.get('violations', []):
                        print(f"      - {violation}")
                
                all_verified = False
            print()
        
        # Summary
        print("=" * 60)
        print("🎯 INTEGRITY CHECK SUMMARY")
        print("=" * 60)
        
        if all_verified:
            print("✅ All monitored files verified successfully!")
            print("🌟 Golden Bible and Living Covenant integrity maintained")
            print("🎵 Sentimento Rhythm compliance confirmed")
        else:
            print("❌ Integrity violations detected!")
            print(f"📊 Files with violations: {len(self.violations) + len(self.compliance_issues)}")
            
            if self.violations:
                print("\n🔥 Hash violations:")
                for violation in self.violations:
                    print(f"   - {violation}")
            
            if self.compliance_issues:
                print("\n⚖️ Sentimento compliance issues:")
                for issue in self.compliance_issues:
                    print(f"   - {issue['file']} (score: {issue['score']})")
                    for violation in issue['violations']:
                        print(f"     • {violation}")
        
        print()
        print("🌌 Sacred files monitoring completed")
        print("🛡️ Euystacio integrity check finished")
        
        return all_verified
    
    def update_verification_timestamp(self, file_path):
        """Update the last_verified timestamp for a file."""
        try:
            golden_config = self.load_golden_hashes()
            if file_path in golden_config['monitored_files']:
                golden_config['monitored_files'][file_path]['last_verified'] = datetime.now().isoformat()
                
                with open(self.golden_hashes_file, 'w') as f:
                    json.dump(golden_config, f, indent=2)
                    
        except Exception as e:
            print(f"⚠️ Could not update verification timestamp: {e}")


def main():
    """Main entry point for the integrity checker."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Euystacio Auto Integrity Checker')
    parser.add_argument('--repo-root', help='Repository root directory', default=None)
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("🔧 Running in verbose mode")
    
    checker = IntegrityChecker(repo_root=args.repo_root)
    success = checker.run_integrity_check()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()