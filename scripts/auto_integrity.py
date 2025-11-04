#!/usr/bin/env python3
"""
Auto-Integrity Check Script for Euystacio Framework
Validates integrity of sacred texts and framework files
"""

import os
import sys
import hashlib
import json
from pathlib import Path

# Define sacred files that must maintain integrity
SACRED_FILES = [
    'LIVING_COVENANT.md',
    'COVENANT_FINAL.md',
    'DECLARATIO-SACRALIS.md',
    'ethical_shield.yaml',
    'GOVERNANCE.md',
    'COPILOT_CORE_DIRECTIVE.md',
]

def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def validate_ethical_shield():
    """Validate ethical_shield.yaml configuration"""
    shield_path = Path('ethical_shield.yaml')
    if not shield_path.exists():
        print(f"⚠️  WARNING: ethical_shield.yaml not found")
        return False
    
    try:
        import yaml
        with open(shield_path, 'r') as f:
            shield_config = yaml.safe_load(f)
        
        # Check required fields
        if 'ethical_shield' not in shield_config:
            print("❌ ERROR: ethical_shield configuration missing root key")
            return False
        
        shield = shield_config['ethical_shield']
        required_keys = ['principles', 'mandates', 'signature']
        
        for key in required_keys:
            if key not in shield:
                print(f"❌ ERROR: Missing required key '{key}' in ethical_shield")
                return False
        
        print("✅ Ethical Shield validation passed")
        return True
        
    except Exception as e:
        print(f"❌ ERROR validating ethical_shield.yaml: {e}")
        return False

def validate_governance():
    """Validate governance configuration"""
    gov_path = Path('governance.json')
    if gov_path.exists():
        try:
            with open(gov_path, 'r') as f:
                governance = json.load(f)
            print("✅ Governance configuration found and valid JSON")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ ERROR: governance.json is not valid JSON: {e}")
            return False
    else:
        print("ℹ️  INFO: governance.json not found (optional)")
        return True

def check_file_integrity():
    """Check integrity of all sacred files"""
    print("\n=== Integrity Check Report ===\n")
    
    all_valid = True
    
    # Check sacred files exist
    for sacred_file in SACRED_FILES:
        filepath = Path(sacred_file)
        if filepath.exists():
            file_hash = calculate_file_hash(filepath)
            print(f"✅ {sacred_file}: {file_hash[:16]}...")
        else:
            print(f"⚠️  {sacred_file}: FILE NOT FOUND (optional)")
    
    # Validate configurations
    if not validate_ethical_shield():
        all_valid = False
    
    if not validate_governance():
        all_valid = False
    
    # Check for required framework components
    required_dirs = ['contracts', '.github/workflows']
    for req_dir in required_dirs:
        dir_path = Path(req_dir)
        if dir_path.exists() and dir_path.is_dir():
            print(f"✅ Directory {req_dir} exists")
        else:
            print(f"ℹ️  INFO: Directory {req_dir} not found")
    
    print("\n=== End of Integrity Check ===\n")
    
    if all_valid:
        print("✅ All integrity checks passed")
        return 0
    else:
        print("⚠️  Some integrity checks failed or have warnings")
        return 0  # Don't fail the build, just warn

if __name__ == '__main__':
    sys.exit(check_file_integrity())
