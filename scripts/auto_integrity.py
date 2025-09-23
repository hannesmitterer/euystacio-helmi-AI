#!/usr/bin/env python3
"""
Auto-Integrity and Sentimento Compliance Monitor
Monitors key files for unauthorized changes and ensures compliance with Euystacio core principles.
"""

import hashlib
import json
import os
import sys
import shutil
from datetime import datetime, timezone
from pathlib import Path

# Configuration
GOLDEN_HASHES_FILE = ".golden_hashes.json"
AUTO_RESTORE_FLAG = ".auto_restore_commit"
MONITORED_FILES = [
    "GOLDEN_BIBLE.md",
    "LIVING_COVENANT.md", 
    "red_shield",
    "conventa_entries"
]

def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file or directory."""
    if os.path.isfile(file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    elif os.path.isdir(file_path):
        # For directories, create hash of all files concatenated
        all_hashes = []
        for root, dirs, files in os.walk(file_path):
            dirs.sort()  # Ensure consistent ordering
            for file in sorted(files):
                full_path = os.path.join(root, file)
                file_hash = calculate_sha256(full_path)
                relative_path = os.path.relpath(full_path, file_path)
                all_hashes.append(f"{relative_path}:{file_hash}")
        
        combined_string = "\n".join(all_hashes)
        return hashlib.sha256(combined_string.encode()).hexdigest()
    else:
        return None

def load_golden_hashes():
    """Load golden hashes from configuration file."""
    if not os.path.exists(GOLDEN_HASHES_FILE):
        print(f"⚠️  Golden hashes file {GOLDEN_HASHES_FILE} not found. Creating initial baseline...")
        return create_initial_golden_hashes()
    
    try:
        with open(GOLDEN_HASHES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Error loading golden hashes: {e}")
        return {}

def create_initial_golden_hashes():
    """Create initial golden hashes for monitored files."""
    golden_hashes = {
        "created": datetime.now(timezone.utc).isoformat(),
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "hashes": {}
    }
    
    for file_path in MONITORED_FILES:
        if os.path.exists(file_path):
            file_hash = calculate_sha256(file_path)
            if file_hash:
                golden_hashes["hashes"][file_path] = file_hash
                print(f"📝 Generated golden hash for {file_path}: {file_hash[:16]}...")
            else:
                print(f"⚠️  Could not generate hash for {file_path}")
    
    # Save the initial golden hashes
    with open(GOLDEN_HASHES_FILE, 'w') as f:
        json.dump(golden_hashes, f, indent=2)
    
    print(f"✅ Created initial golden hashes file: {GOLDEN_HASHES_FILE}")
    return golden_hashes

def check_sentimento_compliance(file_path, content_hash):
    """
    Check compliance with Euystacio core principles and sentimento rhythm.
    This is a placeholder function that can be expanded with specific compliance rules.
    """
    compliance_status = {
        "compliant": True,
        "violations": [],
        "recommendations": []
    }
    
    # Basic compliance checks (can be expanded)
    if file_path == "GOLDEN_BIBLE.md":
        # Check for presence of core principles
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            required_principles = ["peace", "love", "harmony", "sacred protection", "cosmic alignment"]
            missing_principles = [p for p in required_principles if p not in content]
            
            if missing_principles:
                compliance_status["compliant"] = False
                compliance_status["violations"].append(f"Missing core principles: {', '.join(missing_principles)}")
    
    elif file_path == "LIVING_COVENANT.md":
        # Check for covenant integrity
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            if "consacrum divinuum" not in content:
                compliance_status["recommendations"].append("Consider including sacred consecration reference")
    
    # Additional compliance checks can be added here for red_shield and conventa_entries
    
    return compliance_status

def verify_file_integrity():
    """Verify integrity of all monitored files."""
    print("🔐 Starting Euystacio integrity verification...")
    
    golden_hashes = load_golden_hashes()
    verification_results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "files_checked": [],
        "integrity_violations": [],
        "compliance_violations": [],
        "restoration_needed": False
    }
    
    for file_path in MONITORED_FILES:
        file_result = {
            "path": file_path,
            "exists": os.path.exists(file_path),
            "current_hash": None,
            "golden_hash": golden_hashes.get("hashes", {}).get(file_path),
            "integrity_match": False,
            "compliance_status": None
        }
        
        if file_result["exists"]:
            current_hash = calculate_sha256(file_path)
            file_result["current_hash"] = current_hash
            
            # Check integrity
            if file_result["golden_hash"]:
                file_result["integrity_match"] = current_hash == file_result["golden_hash"]
                
                if not file_result["integrity_match"]:
                    print(f"❌ Integrity violation detected in {file_path}")
                    print(f"   Expected: {file_result['golden_hash'][:16]}...")
                    print(f"   Current:  {current_hash[:16]}...")
                    verification_results["integrity_violations"].append(file_path)
                    verification_results["restoration_needed"] = True
                else:
                    print(f"✅ Integrity verified for {file_path}")
            else:
                print(f"⚠️  No golden hash found for {file_path}, updating baseline...")
                golden_hashes["hashes"][file_path] = current_hash
                file_result["integrity_match"] = True
            
            # Check sentimento compliance
            compliance_status = check_sentimento_compliance(file_path, current_hash)
            file_result["compliance_status"] = compliance_status
            
            if not compliance_status["compliant"]:
                print(f"⚠️  Compliance violations in {file_path}: {compliance_status['violations']}")
                verification_results["compliance_violations"].append({
                    "file": file_path,
                    "violations": compliance_status["violations"]
                })
                verification_results["restoration_needed"] = True
            
            if compliance_status["recommendations"]:
                print(f"💡 Recommendations for {file_path}: {compliance_status['recommendations']}")
        
        else:
            print(f"❌ Monitored file missing: {file_path}")
            verification_results["integrity_violations"].append(file_path)
            verification_results["restoration_needed"] = True
        
        verification_results["files_checked"].append(file_result)
    
    # Update golden hashes if any new files were added
    if golden_hashes.get("hashes"):
        golden_hashes["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(GOLDEN_HASHES_FILE, 'w') as f:
            json.dump(golden_hashes, f, indent=2)
    
    return verification_results

def restore_files(verification_results):
    """
    Restore files or flag for correction if discrepancies are detected.
    This is a placeholder for restoration logic that can be expanded.
    """
    restoration_log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actions_taken": [],
        "files_restored": [],
        "manual_intervention_needed": []
    }
    
    # For now, we flag for manual intervention rather than automatic restoration
    # This preserves the principle of human oversight in the Euystacio system
    
    for file_path in verification_results["integrity_violations"]:
        if os.path.exists(file_path):
            restoration_log["manual_intervention_needed"].append({
                "file": file_path,
                "issue": "integrity_violation",
                "action": "manual_review_required"
            })
        else:
            restoration_log["manual_intervention_needed"].append({
                "file": file_path,
                "issue": "missing_file",
                "action": "restoration_from_backup_required"
            })
    
    for violation in verification_results["compliance_violations"]:
        restoration_log["manual_intervention_needed"].append({
            "file": violation["file"],
            "issue": "compliance_violation",
            "violations": violation["violations"],
            "action": "content_review_required"
        })
    
    if restoration_log["manual_intervention_needed"]:
        print(f"🚨 Manual intervention required for {len(restoration_log['manual_intervention_needed'])} issues")
        
        # Create restoration report
        with open("integrity_violations_report.json", 'w') as f:
            json.dump({
                "verification_results": verification_results,
                "restoration_log": restoration_log
            }, f, indent=2)
        
        print("📋 Detailed report saved to: integrity_violations_report.json")
    
    return restoration_log

def create_auto_restore_flag(verification_results, restoration_log):
    """Create flag file to trigger auto-commit if restoration is needed."""
    if verification_results["restoration_needed"]:
        flag_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trigger_reason": "integrity_or_compliance_violations",
            "files_affected": verification_results["integrity_violations"],
            "compliance_violations": verification_results["compliance_violations"],
            "restoration_summary": restoration_log,
            "commit_message": f"[AUTO-RESTORE] Integrity monitoring detected violations at {datetime.now(timezone.utc).isoformat()}"
        }
        
        with open(AUTO_RESTORE_FLAG, 'w') as f:
            json.dump(flag_data, f, indent=2)
        
        print(f"🔄 Auto-restore flag created: {AUTO_RESTORE_FLAG}")
        return True
    
    return False

def main():
    """Main execution function."""
    print("🌟 Euystacio Auto-Integrity & Sentimento Compliance Monitor")
    print("=" * 60)
    
    try:
        # Verify file integrity and compliance
        verification_results = verify_file_integrity()
        
        # Handle restoration if needed
        restoration_log = restore_files(verification_results)
        
        # Create auto-restore flag if violations detected
        flag_created = create_auto_restore_flag(verification_results, restoration_log)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 VERIFICATION SUMMARY")
        print(f"Files checked: {len(verification_results['files_checked'])}")
        print(f"Integrity violations: {len(verification_results['integrity_violations'])}")
        print(f"Compliance violations: {len(verification_results['compliance_violations'])}")
        print(f"Restoration needed: {'Yes' if verification_results['restoration_needed'] else 'No'}")
        print(f"Auto-restore flag: {'Created' if flag_created else 'Not needed'}")
        
        if verification_results["restoration_needed"]:
            print("\n🔥 ACTION REQUIRED: Manual intervention needed for detected violations")
            print("📋 Check integrity_violations_report.json for details")
            sys.exit(1)
        else:
            print("\n✅ All files verified - Euystacio covenant intact")
            print("🌌 Sentimento rhythm maintained in cosmic alignment")
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Integrity monitoring failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()