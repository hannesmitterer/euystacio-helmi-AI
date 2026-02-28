#!/usr/bin/env python3
"""
Integration Test for Internet Organica Framework

Tests all core modules together:
- Biological Rhythm Synchronization
- SovereignShield Security
- Wall of Entropy Logging
- Vacuum-Bridge IPFS Integration
"""

import sys
import json
from pathlib import Path
import tempfile
import shutil

# Import modules
from biological_rhythm_sync import BiologicalRhythmSync
from sovereign_shield import SovereignShield
from wall_of_entropy import EntropyWall, EventCategory
from vacuum_bridge import VacuumBridge


def test_biological_rhythm():
    """Test biological rhythm synchronization."""
    print("\n" + "=" * 70)
    print("TEST 1: Biological Rhythm Synchronization")
    print("=" * 70)
    
    rhythm = BiologicalRhythmSync()
    
    # Test frequency
    assert rhythm.BIOLOGICAL_FREQUENCY == 0.432, "Frequency should be 0.432 Hz"
    print("✓ Frequency validated: 0.432 Hz")
    
    # Test frequency validation
    assert rhythm.validate_frequency(0.432), "Should validate correct frequency"
    assert not rhythm.validate_frequency(1.0), "Should reject incorrect frequency"
    print("✓ Frequency validation working")
    
    # Test phase calculation
    phase = rhythm.get_current_phase()
    assert 0 <= phase <= 1, "Phase should be between 0 and 1"
    print(f"✓ Current phase: {phase:.3f}")
    
    # Test synchronized decorator
    @rhythm.synchronized
    def test_func():
        return "synchronized"
    
    result = test_func()
    assert result == "synchronized", "Synchronized function should work"
    print("✓ Synchronized decorator working")
    
    # Test statistics
    stats = rhythm.get_sync_statistics()
    assert stats['frequency_hz'] == 0.432, "Stats should report correct frequency"
    print("✓ Statistics generation working")
    
    print("\n✅ Biological Rhythm Synchronization: PASSED")
    return True


def test_sovereign_shield():
    """Test SovereignShield security system."""
    print("\n" + "=" * 70)
    print("TEST 2: SovereignShield Security")
    print("=" * 70)
    
    shield = SovereignShield(enable_logging=True)
    
    # Test legitimate request
    legit_request = {
        'headers': {'user-agent': 'Mozilla/5.0'},
        'params': {'search': 'hello'},
        'url': '/api/search'
    }
    
    allowed, _ = shield.check_and_protect(legit_request)
    assert allowed, "Legitimate request should be allowed"
    print("✓ Legitimate request allowed")
    
    # Test SPID attempt
    spid_request = {
        'headers': {'user-agent': 'Mozilla/5.0'},
        'params': {'fingerprint': 'abc123', 'device-id': 'xyz789'},
        'url': '/api/profile'
    }
    
    allowed, neutralization = shield.check_and_protect(spid_request)
    assert not allowed, "SPID attempt should be blocked"
    assert neutralization is not None, "Neutralization data should be provided"
    print("✓ SPID attempt blocked")
    
    # Test tracking attempt
    tracking_request = {
        'headers': {'user-agent': 'Mozilla/5.0'},
        'params': {'google-analytics': 'true'},
        'url': '/track'
    }
    
    allowed, neutralization = shield.check_and_protect(tracking_request)
    assert not allowed, "Tracking attempt should be blocked"
    print("✓ Tracking attempt blocked")
    
    # Test statistics
    stats = shield.get_statistics()
    assert stats['total_neutralizations'] >= 2, "Should have neutralizations"
    assert stats['nsr_compliance'], "Should be NSR compliant"
    print("✓ Statistics and NSR compliance verified")
    
    print("\n✅ SovereignShield Security: PASSED")
    return True


def test_wall_of_entropy():
    """Test Wall of Entropy logging system."""
    print("\n" + "=" * 70)
    print("TEST 3: Wall of Entropy Logging")
    print("=" * 70)
    
    # Use temporary log file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        temp_log = f.name
    
    try:
        wall = EntropyWall(temp_log)
        
        # Test genesis event
        assert len(wall.events) >= 1, "Should have genesis event"
        print("✓ Genesis event created")
        
        # Test logging events
        wall.log_event(
            EventCategory.SECURITY_EVENT,
            'info',
            'Test Event',
            'Testing entropy wall'
        )
        
        assert len(wall.events) >= 2, "Should have multiple events"
        print("✓ Event logging working")
        
        # Test chain integrity
        assert wall.verify_chain_integrity(), "Chain should be valid"
        print("✓ Chain integrity verified")
        
        # Test filtering
        security_events = wall.get_events(category=EventCategory.SECURITY_EVENT)
        assert len(security_events) > 0, "Should filter by category"
        print("✓ Event filtering working")
        
        # Test statistics
        stats = wall.get_statistics()
        assert stats['total_events'] >= 2, "Should have events"
        assert stats['chain_valid'], "Chain should be valid"
        print("✓ Statistics generation working")
        
        print("\n✅ Wall of Entropy Logging: PASSED")
        return True
        
    finally:
        # Cleanup
        Path(temp_log).unlink(missing_ok=True)


def test_vacuum_bridge():
    """Test Vacuum-Bridge IPFS integration."""
    print("\n" + "=" * 70)
    print("TEST 4: Vacuum-Bridge IPFS Integration")
    print("=" * 70)
    
    # Use temporary directory
    temp_dir = tempfile.mkdtemp(prefix='test_vacuum_')
    
    try:
        bridge = VacuumBridge(temp_dir)
        
        # Create test file
        test_file = Path(temp_dir) / 'test_asset.txt'
        with open(test_file, 'w') as f:
            f.write("Internet Organica Test Asset")
        
        # Test adding asset
        asset = bridge.add_asset(
            str(test_file),
            critical=True,
            metadata={'type': 'test'}
        )
        
        assert asset['critical'], "Asset should be marked critical"
        assert len(asset['backup_locations']) > 0, "Should have backup locations"
        print("✓ Asset distribution working")
        
        # Test integrity verification
        assert bridge.verify_integrity(asset['content_hash']), "Integrity should verify"
        print("✓ Integrity verification working")
        
        # Test retrieval
        content = bridge.get_asset(asset['content_hash'])
        assert content is not None, "Should retrieve asset"
        assert b"Internet Organica" in content, "Content should match"
        print("✓ Asset retrieval working")
        
        # Test statistics
        stats = bridge.get_statistics()
        assert stats['total_assets'] >= 1, "Should have assets"
        assert stats['critical_assets'] >= 1, "Should have critical assets"
        print("✓ Statistics generation working")
        
        print("\n✅ Vacuum-Bridge IPFS Integration: PASSED")
        return True
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_integration():
    """Test integration of all modules."""
    print("\n" + "=" * 70)
    print("TEST 5: Full Integration Test")
    print("=" * 70)
    
    # Initialize all systems
    rhythm = BiologicalRhythmSync()
    shield = SovereignShield(enable_logging=True)
    
    temp_dir = tempfile.mkdtemp(prefix='test_integration_')
    temp_log = str(Path(temp_dir) / 'test_wall.log')
    
    try:
        wall = EntropyWall(temp_log)
        bridge = VacuumBridge(str(Path(temp_dir) / 'vacuum'))
        
        # Simulate a complete workflow
        print("\nSimulating integrated workflow...")
        
        # 1. Biological rhythm sync
        @rhythm.synchronized
        def protected_operation():
            return "synced"
        
        result = protected_operation()
        print("✓ Operation synchronized with biological rhythm")
        
        # 2. Shield protects request
        request = {
            'headers': {'user-agent': 'Scraper/1.0'},
            'params': {'extract-all': 'true'},
            'url': '/api/data'
        }
        
        allowed, neutralization = shield.check_and_protect(request)
        
        # 3. Log to entropy wall
        if not allowed:
            wall.log_event(
                EventCategory.THREAT_NEUTRALIZED,
                'warning',
                'Threat Blocked',
                f"Blocked {neutralization['threat_type']}"
            )
            print("✓ Threat blocked and logged to entropy wall")
        
        # 4. Distribute critical asset
        test_file = Path(temp_dir) / 'critical_doc.txt'
        with open(test_file, 'w') as f:
            f.write("Critical Internet Organica Document")
        
        asset = bridge.add_asset(str(test_file), critical=True)
        print("✓ Critical asset distributed via Vacuum-Bridge")
        
        # 5. Verify everything
        assert rhythm.validate_frequency(0.432)
        assert shield.get_statistics()['nsr_compliance']
        assert wall.verify_chain_integrity()
        assert bridge.verify_integrity(asset['content_hash'])
        
        print("\n✅ Full Integration Test: PASSED")
        print("\nAll systems working together harmoniously! 🌿")
        return True
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Run all tests."""
    print("=" * 70)
    print("Internet Organica Framework - Integration Test Suite")
    print("=" * 70)
    print("\nTesting all core modules for harmonious operation...")
    
    tests = [
        ("Biological Rhythm Synchronization", test_biological_rhythm),
        ("SovereignShield Security", test_sovereign_shield),
        ("Wall of Entropy Logging", test_wall_of_entropy),
        ("Vacuum-Bridge IPFS Integration", test_vacuum_bridge),
        ("Full System Integration", test_integration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name}: FAILED")
            print(f"Error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 70)
    
    if passed == total:
        print("\n🌿 All systems operational and aligned with Internet Organica principles!")
        print("Frequency: 0.432 Hz | Principles: Lex Amoris, NSR, OLF")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
