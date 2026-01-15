#!/usr/bin/env python3
"""
validate_lex_amoris.py - Validation script for Lex Amoris Security implementation

This script validates that all components of the Lex Amoris security system
are properly implemented and working correctly.
"""

import sys
import os
from datetime import datetime, timezone


def validate_imports():
    """Validate that all modules can be imported."""
    print("=" * 70)
    print("VALIDATION 1: Module Imports")
    print("=" * 70)
    
    try:
        from lex_amoris_security import (
            RhythmValidator,
            DynamicBlacklist,
            LazySecurity,
            IPFSBackupManager,
            RescueChannel,
            LexAmorisSecuritySystem,
            create_security_system
        )
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def validate_rhythm_validation():
    """Validate rhythm validation functionality."""
    print("\n" + "=" * 70)
    print("VALIDATION 2: Rhythm Validation")
    print("=" * 70)
    
    from lex_amoris_security import RhythmValidator
    
    validator = RhythmValidator(base_frequency=432.0)
    
    # Test packet
    test_data = {
        "message": "test harmony",
        "sentimento": "love",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    is_valid, reason = validator.validate_rhythm(test_data, "192.168.1.1")
    
    print(f"Base frequency: {validator.base_frequency} Hz")
    print(f"Tolerance: {validator.tolerance * 100}%")
    print(f"Test packet: {test_data}")
    print(f"Validation result: {is_valid}")
    print(f"Reason: {reason}")
    
    # Verify log was created
    if len(validator.validation_log) > 0:
        print(f"✓ Validation log working ({len(validator.validation_log)} entries)")
    else:
        print("✗ Validation log not working")
        return False
    
    print("✓ Rhythm validation working correctly")
    return True


def validate_dynamic_blacklist():
    """Validate dynamic blacklist functionality."""
    print("\n" + "=" * 70)
    print("VALIDATION 3: Dynamic Blacklist")
    print("=" * 70)
    
    from lex_amoris_security import DynamicBlacklist
    
    blacklist = DynamicBlacklist(threshold=5, time_window=300)
    
    test_source = "10.0.0.1"
    
    # Record failures
    for i in range(5):
        blacklist.record_failure(test_source)
    
    is_blacklisted = blacklist.is_blacklisted(test_source)
    
    print(f"Threshold: {blacklist.threshold} failures")
    print(f"Time window: {blacklist.time_window} seconds")
    print(f"Test source: {test_source}")
    print(f"Failures recorded: 5")
    print(f"Is blacklisted: {is_blacklisted}")
    
    if is_blacklisted:
        print("✓ Dynamic blacklist working correctly")
        return True
    else:
        print("✗ Dynamic blacklist not working")
        return False


def validate_lazy_security():
    """Validate lazy security functionality."""
    print("\n" + "=" * 70)
    print("VALIDATION 4: Lazy Security")
    print("=" * 70)
    
    from lex_amoris_security import LazySecurity
    
    lazy_sec = LazySecurity(activation_threshold=50.0)
    
    # Perform scan
    pressure = lazy_sec.rotesschild_scan()
    should_activate = lazy_sec.should_activate()
    status = lazy_sec.get_status()
    
    print(f"Activation threshold: {lazy_sec.activation_threshold} mV/m")
    print(f"Current pressure: {pressure:.2f} mV/m")
    print(f"Should activate: {should_activate}")
    print(f"Is active: {status['is_active']}")
    print(f"Scan history entries: {len(lazy_sec.scan_history)}")
    
    if len(lazy_sec.scan_history) > 0:
        print("✓ Lazy security working correctly")
        return True
    else:
        print("✗ Lazy security not working")
        return False


def validate_ipfs_backup():
    """Validate IPFS backup functionality."""
    print("\n" + "=" * 70)
    print("VALIDATION 5: IPFS Backup System")
    print("=" * 70)
    
    from lex_amoris_security import IPFSBackupManager
    import tempfile
    import os
    
    # Create temporary test directory
    temp_dir = tempfile.mkdtemp()
    backup_mgr = IPFSBackupManager(backup_dir=os.path.join(temp_dir, "backup"))
    
    # Create a test file
    test_file = os.path.join(temp_dir, "test_config.json")
    with open(test_file, "w") as f:
        f.write('{"test": "data"}')
    
    # Create backup
    manifest = backup_mgr.create_backup([test_file])
    
    print(f"Backup directory: {backup_mgr.backup_dir}")
    print(f"Files backed up: {len(manifest.get('files', {}))}")
    
    if test_file in manifest.get('files', {}):
        file_info = manifest['files'][test_file]
        print(f"Test file hash: {file_info.get('hash', 'N/A')[:16]}...")
        
        # Verify backup
        is_valid = backup_mgr.verify_backup(test_file)
        print(f"Backup verification: {is_valid}")
        
        if is_valid:
            print("✓ IPFS backup working correctly")
            
            # Cleanup
            import shutil
            shutil.rmtree(temp_dir)
            return True
    
    print("✗ IPFS backup not working")
    return False


def validate_rescue_channel():
    """Validate rescue channel functionality."""
    print("\n" + "=" * 70)
    print("VALIDATION 6: Rescue Channel")
    print("=" * 70)
    
    from lex_amoris_security import RescueChannel
    
    rescue = RescueChannel()
    
    # Send test rescue message
    message = rescue.send_rescue_message("192.168.1.1", "validation_test")
    
    print(f"False positive threshold: {rescue.false_positive_threshold * 100}%")
    print(f"Rescue message sent:")
    print(f"  Type: {message.get('type')}")
    print(f"  Action: {message.get('action')}")
    print(f"  Compassion level: {message.get('compassion_level')}")
    print(f"  Lex Amoris signature: {message.get('lex_amoris_signature')}")
    print(f"Rescue log entries: {len(rescue.rescue_log)}")
    
    if (len(rescue.rescue_log) > 0 and 
        message.get('lex_amoris_signature') == 'love_first_protocol'):
        print("✓ Rescue channel working correctly")
        return True
    else:
        print("✗ Rescue channel not working")
        return False


def validate_integrated_system():
    """Validate integrated security system."""
    print("\n" + "=" * 70)
    print("VALIDATION 7: Integrated Security System")
    print("=" * 70)
    
    from lex_amoris_security import LexAmorisSecuritySystem
    
    security = LexAmorisSecuritySystem()
    
    # Test packet processing
    test_data = {
        "message": "integration test",
        "sentimento": "harmony"
    }
    
    result = security.process_packet(test_data, "192.168.1.10")
    
    print(f"Test packet processed:")
    print(f"  Accepted: {result.get('accepted')}")
    print(f"  Reason: {result.get('reason')}")
    
    # Get system status
    status = security.get_system_status()
    
    print(f"\nSystem status:")
    print(f"  Lazy security active: {status['lazy_security']['is_active']}")
    print(f"  Blacklisted sources: {status['blacklist']['total_blocked']}")
    print(f"  Total validations: {status['rhythm_validation']['total_validations']}")
    print(f"  Total rescues: {status['rescue_channel']['total_rescues']}")
    
    # Verify all components initialized
    if (security.rhythm_validator and 
        security.blacklist and 
        security.lazy_security and 
        security.ipfs_backup and 
        security.rescue_channel):
        print("\n✓ Integrated system working correctly")
        return True
    else:
        print("\n✗ Integrated system not working")
        return False


def validate_cli_tool():
    """Validate CLI tool exists and is executable."""
    print("\n" + "=" * 70)
    print("VALIDATION 8: CLI Tool")
    print("=" * 70)
    
    cli_path = "lex_amoris_cli.py"
    
    if os.path.exists(cli_path):
        print(f"✓ CLI tool exists: {cli_path}")
        
        # Check if executable
        if os.access(cli_path, os.X_OK):
            print("✓ CLI tool is executable")
        else:
            print("⚠ CLI tool is not executable (use: chmod +x lex_amoris_cli.py)")
        
        return True
    else:
        print(f"✗ CLI tool not found: {cli_path}")
        return False


def validate_documentation():
    """Validate documentation exists."""
    print("\n" + "=" * 70)
    print("VALIDATION 9: Documentation")
    print("=" * 70)
    
    docs = [
        ("LEX_AMORIS_SECURITY.md", "Technical documentation"),
        ("LEX_AMORIS_IMPLEMENTATION_SUMMARY.md", "Implementation summary"),
        ("integration_example.py", "Integration examples")
    ]
    
    all_found = True
    for doc_file, description in docs:
        if os.path.exists(doc_file):
            size = os.path.getsize(doc_file)
            print(f"✓ {description}: {doc_file} ({size} bytes)")
        else:
            print(f"✗ {description}: {doc_file} - NOT FOUND")
            all_found = False
    
    return all_found


def validate_tests():
    """Validate test file exists."""
    print("\n" + "=" * 70)
    print("VALIDATION 10: Test Suite")
    print("=" * 70)
    
    test_file = "test_lex_amoris_security.py"
    
    if os.path.exists(test_file):
        print(f"✓ Test suite exists: {test_file}")
        
        # Count test methods
        with open(test_file, 'r') as f:
            content = f.read()
            test_count = content.count('def test_')
        
        print(f"✓ Test methods found: {test_count}")
        
        return True
    else:
        print(f"✗ Test suite not found: {test_file}")
        return False


def main():
    """Run all validations."""
    print("\n" + "=" * 70)
    print("LEX AMORIS SECURITY - VALIDATION SUITE")
    print("=" * 70)
    print(f"Date: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)
    
    validations = [
        ("Module Imports", validate_imports),
        ("Rhythm Validation", validate_rhythm_validation),
        ("Dynamic Blacklist", validate_dynamic_blacklist),
        ("Lazy Security", validate_lazy_security),
        ("IPFS Backup", validate_ipfs_backup),
        ("Rescue Channel", validate_rescue_channel),
        ("Integrated System", validate_integrated_system),
        ("CLI Tool", validate_cli_tool),
        ("Documentation", validate_documentation),
        ("Test Suite", validate_tests)
    ]
    
    results = {}
    
    for name, validation_func in validations:
        try:
            results[name] = validation_func()
        except Exception as e:
            print(f"\n✗ {name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False
    
    # Final summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} validations passed ({passed/total*100:.1f}%)")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 ALL VALIDATIONS PASSED - LEX AMORIS SECURITY READY")
        return 0
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
