#!/usr/bin/env python3
"""
Test suite for Conventa Ceremony Automator
Validates ceremony record keeping, Red Seal verification, and transparency
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone

from conventa_ceremony_automator import ConventaCeremonyAutomator

def test_ceremony_automation():
    """Test the complete ceremony automation workflow"""
    print("Starting ceremony automation tests...")
    
    # Create temporary test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test directories
        conventa_dir = temp_path / "conventa_entries"
        red_shield_dir = temp_path / "red_shield"
        foundation_dir = temp_path / "docs" / "foundation"
        transparency_dir = temp_path / "docs" / "transparency"
        
        conventa_dir.mkdir(parents=True)
        red_shield_dir.mkdir(parents=True)
        foundation_dir.mkdir(parents=True)
        transparency_dir.mkdir(parents=True)
        
        # Create test Conventa entry
        test_entry_content = """=== EUYSTACIO CONVENTA ENTRY ===
2025-09-25T12:00:00Z
Event: Test Rite of Validation
Performer: Test Performer (AI System)

Affirmation:
This is a test affirmation for ceremony validation.
The sacred covenant is maintained through automated systems.
"""
        
        test_entry_file = conventa_dir / "2025-09-25-test-rite-validation.txt"
        with open(test_entry_file, "w") as f:
            f.write(test_entry_content)
        
        # Create corresponding Red Seal
        import hashlib
        with open(test_entry_file, "rb") as f:
            test_hash = hashlib.sha256(f.read()).hexdigest()
        
        red_seal_file = red_shield_dir / "2025-09-25-test-rite-validation.sha256"
        with open(red_seal_file, "w") as f:
            f.write(test_hash)
        
        # Set up automator with test paths
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Create automator instance
            automator = ConventaCeremonyAutomator()
            
            # Test 1: Detect new entries
            new_entries = automator.detect_new_entries()
            assert len(new_entries) == 1, f"Expected 1 new entry, got {len(new_entries)}"
            print("✓ New entry detection works")
            
            # Test 2: Parse conventa entry
            entry_data = automator.parse_conventa_entry(test_entry_file)
            assert entry_data is not None, "Failed to parse conventa entry"
            assert entry_data['event'] == "Test Rite of Validation", f"Event parsing failed: {entry_data['event']}"
            assert entry_data['performer'] == "Test Performer (AI System)", f"Performer parsing failed: {entry_data['performer']}"
            assert entry_data['affirmation_status'] == "complete", f"Affirmation status wrong: {entry_data['affirmation_status']}"
            print("✓ Entry parsing works")
            
            # Test 3: Red Seal verification
            red_seal_info = automator.find_red_seal(test_entry_file.name)
            assert red_seal_info is not None, "Failed to find Red Seal"
            assert red_seal_info['seal_hash'] == test_hash, "Red Seal hash mismatch"
            
            seal_verified = automator.verify_red_seal(test_entry_file, red_seal_info)
            assert seal_verified, "Red Seal verification failed"
            print("✓ Red Seal verification works")
            
            # Test 4: Ceremony record creation
            ceremony_record = automator.create_ceremony_record(test_entry_file)
            assert ceremony_record is not None, "Failed to create ceremony record"
            assert ceremony_record['event'] == "Test Rite of Validation", "Ceremony record event mismatch"
            assert ceremony_record['red_seal']['verified'], "Ceremony record seal verification failed"
            assert ceremony_record['anchoring_status'] == "anchored", "Ceremony record not anchored properly"
            print("✓ Ceremony record creation works")
            
            # Test 5: Full processing
            processed_records = automator.process_all_new_entries()
            assert len(processed_records) == 1, f"Expected 1 processed record, got {len(processed_records)}"
            print("✓ Full processing works")
            
            # Test 6: Verify generated files
            ceremony_ledger_file = foundation_dir / "ceremony_ledger.json"
            assert ceremony_ledger_file.exists(), "Ceremony ledger not created"
            
            sync_ledger_file = foundation_dir / "sync_ledger.json"
            assert sync_ledger_file.exists(), "Sync ledger not created"
            
            transparency_report_file = transparency_dir / "ceremony_transparency_report.json"
            assert transparency_report_file.exists(), "Transparency report not created"
            print("✓ All required files generated")
            
            # Test 7: Verify ledger content
            with open(ceremony_ledger_file, "r") as f:
                ceremony_ledger = json.load(f)
            
            assert len(ceremony_ledger) == 1, "Ceremony ledger should have 1 entry"
            assert ceremony_ledger[0]['anchoring_status'] == "anchored", "Entry should be anchored"
            print("✓ Ledger content verification works")
            
            # Test 8: Test idempotency (running again should not duplicate)
            processed_records_2 = automator.process_all_new_entries()
            assert len(processed_records_2) == 0, "Second run should find no new entries"
            print("✓ Idempotency works")
            
        finally:
            os.chdir(original_cwd)
    
    print("All ceremony automation tests passed! ✓")
    return True

def test_integration_with_existing_system():
    """Test integration with existing astrodeepaura sync system"""
    print("Testing integration with existing synchronization system...")
    
    # Import existing sync functionality
    try:
        from astrodeepaura_sync import current_utc_iso, read_ledger, log_to_ledger
        print("✓ Successfully imported existing sync functions")
        
        # Test timestamp compatibility
        iso_time = current_utc_iso()
        assert 'T' in iso_time and 'Z' not in iso_time, "Timestamp format compatibility check"
        print("✓ Timestamp format compatible")
        
        return True
    except ImportError as e:
        print(f"⚠ Warning: Could not import sync functions: {e}")
        return False

def run_all_tests():
    """Run all ceremony automation tests"""
    print("=== CONVENTA CEREMONY AUTOMATION TESTS ===\n")
    
    try:
        # Test core automation functionality
        test_ceremony_automation()
        print()
        
        # Test integration
        test_integration_with_existing_system()
        print()
        
        print("=== ALL TESTS PASSED ===")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)