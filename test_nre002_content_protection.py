"""
Tests for NRE-002 Content Protection System
Validates anti-censorship, transparency, and didactic stratification
"""

import sys
import json
from content_protection import (
    ContentLevel,
    ContentWarning,
    ContentItem,
    NRE002ContentSystem,
    ADiSynthesis
)


def test_content_item_creation():
    """Test that content items require complete content"""
    print("Test 1: Content item creation with complete content...")
    
    content = ContentItem(
        content_id="test_001",
        title="Test Historical Document",
        content_by_level={
            ContentLevel.BASIC: "Overview of historical event",
            ContentLevel.DETAILED: "Detailed analysis with context",
            ContentLevel.COMPLETE: "Complete archival material with all details"
        },
        warnings=[ContentWarning.SENSITIVE_HISTORICAL]
    )
    
    assert content.content_id == "test_001"
    assert ContentLevel.COMPLETE in content.content_by_level
    assert content.integrity_hash is not None
    print("✓ Content item created successfully with integrity hash")
    
    # Test that content without COMPLETE level fails
    try:
        invalid_content = ContentItem(
            content_id="test_002",
            title="Invalid Content",
            content_by_level={
                ContentLevel.BASIC: "Only basic content"
            },
            warnings=[ContentWarning.NONE]
        )
        print("✗ FAILED: Should not allow content without COMPLETE level")
        return False
    except ValueError as e:
        print(f"✓ Correctly rejected content without COMPLETE level: {e}")
    
    return True


def test_integrity_verification():
    """Test content integrity verification"""
    print("\nTest 2: Content integrity verification...")
    
    content = ContentItem(
        content_id="test_003",
        title="Integrity Test",
        content_by_level={
            ContentLevel.COMPLETE: "Original complete content"
        },
        warnings=[ContentWarning.NONE]
    )
    
    # Verify original integrity
    assert content.verify_integrity() == True
    print("✓ Original content integrity verified")
    
    # Tamper with content
    content.content_by_level[ContentLevel.COMPLETE] = "Tampered content"
    
    # Verify integrity fails after tampering
    assert content.verify_integrity() == False
    print("✓ Tampering detected correctly")
    
    return True


def test_always_override_option():
    """Test Always-Override option for complete access"""
    print("\nTest 3: Always-Override option...")
    
    system = NRE002ContentSystem()
    
    content = ContentItem(
        content_id="test_004",
        title="Override Test",
        content_by_level={
            ContentLevel.BASIC: "Basic info",
            ContentLevel.DETAILED: "Detailed info",
            ContentLevel.COMPLETE: "Complete sensitive material"
        },
        warnings=[ContentWarning.TRAUMA_RELATED]
    )
    
    system.add_content(content, curator_id="curator_001", rationale="Test content")
    
    # Without override, warning should be required
    result = system.get_content(
        content_id="test_004",
        requested_level=ContentLevel.BASIC,
        user_id="user_001",
        user_acknowledged_warnings=False,
        override_to_complete=False
    )
    
    assert result["status"] == "warning_required"
    print("✓ Content warning required when not acknowledged")
    
    # With override, should get complete content immediately
    result = system.get_content(
        content_id="test_004",
        requested_level=ContentLevel.BASIC,
        user_id="user_001",
        user_acknowledged_warnings=False,
        override_to_complete=True  # Always-Override
    )
    
    assert result["status"] == "success"
    assert result["level"] == "COMPLETE"
    assert result["content"] == "Complete sensitive material"
    print("✓ Always-Override option provides immediate access to complete content")
    
    return True


def test_anti_censorship_compliance():
    """Test that system enforces anti-censorship requirements"""
    print("\nTest 4: Anti-censorship compliance...")
    
    system = NRE002ContentSystem()
    
    # Try to add content without complete level (should fail)
    try:
        incomplete_content = ContentItem(
            content_id="test_005",
            title="Incomplete Content",
            content_by_level={
                ContentLevel.BASIC: "Only basic"
            },
            warnings=[ContentWarning.NONE]
        )
        result = system.add_content(
            incomplete_content,
            curator_id="curator_001",
            rationale="Test"
        )
        print("✗ FAILED: Should not allow content without COMPLETE level")
        return False
    except ValueError:
        print("✓ System correctly rejects content without COMPLETE level")
    
    # Try to add content with empty complete level
    empty_complete = ContentItem(
        content_id="test_006",
        title="Empty Complete",
        content_by_level={
            ContentLevel.COMPLETE: ""  # Empty
        },
        warnings=[ContentWarning.NONE]
    )
    
    result = system.add_content(
        empty_complete,
        curator_id="curator_001",
        rationale="Test"
    )
    
    assert result == False
    assert len(system.anti_censorship_violations) > 0
    print("✓ System detects and logs anti-censorship violations")
    
    return True


def test_audit_logging():
    """Test transparent audit logging"""
    print("\nTest 5: Audit logging and transparency...")
    
    system = NRE002ContentSystem()
    
    content = ContentItem(
        content_id="test_007",
        title="Audit Test",
        content_by_level={
            ContentLevel.BASIC: "Basic",
            ContentLevel.DETAILED: "Detailed",
            ContentLevel.COMPLETE: "Complete"
        },
        warnings=[ContentWarning.NONE]
    )
    
    system.add_content(
        content,
        curator_id="historian_001",
        rationale="Educational stratification for age-appropriate access"
    )
    
    # Check that curation was logged
    logs = system.get_audit_logs(content_id="test_007")
    log_data = json.loads(logs)
    
    assert len(log_data) >= 3  # One log per level
    assert any(log["curator_id"] == "historian_001" for log in log_data)
    assert any(log["rationale"] == "Educational stratification for age-appropriate access" for log in log_data)
    print("✓ Curation decisions are logged with rationale")
    
    # Access content and verify access is logged
    system.get_content(
        content_id="test_007",
        requested_level=ContentLevel.COMPLETE,
        user_id="user_002",
        user_acknowledged_warnings=True,
        override_to_complete=True
    )
    
    logs = system.get_audit_logs(content_id="test_007")
    log_data = json.loads(logs)
    
    access_logs = [log for log in log_data if log["action"] == "access"]
    assert len(access_logs) >= 1
    assert access_logs[0]["user_id"] == "user_002"
    assert access_logs[0]["override_used"] == True
    print("✓ User access patterns are logged for transparency")
    
    return True


def test_system_integrity_verification():
    """Test system-wide integrity verification"""
    print("\nTest 6: System integrity verification...")
    
    system = NRE002ContentSystem()
    
    content1 = ContentItem(
        content_id="test_008",
        title="Content 1",
        content_by_level={
            ContentLevel.COMPLETE: "Complete content 1"
        },
        warnings=[ContentWarning.NONE]
    )
    
    content2 = ContentItem(
        content_id="test_009",
        title="Content 2",
        content_by_level={
            ContentLevel.COMPLETE: "Complete content 2"
        },
        warnings=[ContentWarning.NONE]
    )
    
    system.add_content(content1, curator_id="curator_001", rationale="Test")
    system.add_content(content2, curator_id="curator_001", rationale="Test")
    
    integrity_report = system.verify_system_integrity()
    
    assert integrity_report["total_content_items"] == 2
    assert len(integrity_report["integrity_verified"]) == 2
    assert len(integrity_report["integrity_failed"]) == 0
    assert integrity_report["system_compliant"] == True
    print("✓ System integrity verification working correctly")
    
    return True


def test_adi_synthesis():
    """Test ADi (Inspirational Synthesis from Facts) implementation"""
    print("\nTest 7: ADi synthesis from facts...")
    
    adi = ADiSynthesis.create_adi_from_facts(
        facts=[
            "Historical event occurred on specific date",
            "Event had documented impact on community",
            "Multiple primary sources confirm details"
        ],
        context="Educational material for historical understanding",
        synthesis_goal="Provide meaningful context for learning"
    )
    
    assert adi["type"] == "ADi_Synthesis"
    assert len(adi["verified_facts"]) == 3
    assert adi["accuracy_maintained"] == True
    assert adi["manipulation_free"] == True
    print("✓ ADi synthesis maintains factual accuracy")
    
    return True


def test_voluntary_consent():
    """Test voluntary consent and zero-obligation principle"""
    print("\nTest 8: Voluntary consent and zero-obligation...")
    
    system = NRE002ContentSystem()
    
    content = ContentItem(
        content_id="test_010",
        title="Consent Test",
        content_by_level={
            ContentLevel.BASIC: "Basic content",
            ContentLevel.COMPLETE: "Complete sensitive content"
        },
        warnings=[ContentWarning.GRAPHIC_DETAIL]
    )
    
    system.add_content(content, curator_id="curator_001", rationale="Test")
    
    # Without acknowledgment, user should get warning
    result = system.get_content(
        content_id="test_010",
        requested_level=ContentLevel.COMPLETE,
        user_id="user_003",
        user_acknowledged_warnings=False
    )
    
    assert result["status"] == "warning_required"
    assert ContentWarning.GRAPHIC_DETAIL.value in result["warnings"]
    print("✓ System requires voluntary consent before sensitive content")
    
    # With acknowledgment, user should get content
    result = system.get_content(
        content_id="test_010",
        requested_level=ContentLevel.COMPLETE,
        user_id="user_003",
        user_acknowledged_warnings=True
    )
    
    assert result["status"] == "success"
    assert result["content"] == "Complete sensitive content"
    print("✓ Voluntary consent allows access without forced exposure")
    
    return True


def run_all_tests():
    """Run all NRE-002 tests"""
    print("="*60)
    print("NRE-002 Content Protection System - Test Suite")
    print("="*60)
    
    tests = [
        test_content_item_creation,
        test_integrity_verification,
        test_always_override_option,
        test_anti_censorship_compliance,
        test_audit_logging,
        test_system_integrity_verification,
        test_adi_synthesis,
        test_voluntary_consent
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
