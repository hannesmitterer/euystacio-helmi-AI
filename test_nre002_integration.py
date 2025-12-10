"""
Integration tests for NRE-002 with existing Euystacio framework
"""

import json
import sys


def test_ethics_block_integration():
    """Test that NRE-002 is properly integrated into ethics_block.json"""
    print("Test: Ethics block integration...")
    
    with open('red_code/ethics_block.json', 'r') as f:
        ethics_data = json.load(f)
    
    # Check for NRE-002 integration
    assert 'nre_002_content_protection' in ethics_data, "NRE-002 not found in ethics_block.json"
    
    nre002 = ethics_data['nre_002_content_protection']
    
    # Verify key components
    assert nre002['status'] == 'ACTIVE', "NRE-002 should be ACTIVE"
    assert 'anti_censorship_clause' in nre002, "Anti-censorship clause missing"
    assert 'user_control_principles' in nre002, "User control principles missing"
    assert 'transparency_requirements' in nre002, "Transparency requirements missing"
    assert 'adi_definition' in nre002, "ADi definition missing"
    assert 'immutable_ai_commitment' in nre002, "Immutable AI commitment missing"
    
    # Verify anti-censorship requirements
    anti_censorship = nre002['anti_censorship_clause']['requirements']
    assert any('Complete content' in req for req in anti_censorship), "Complete content requirement missing"
    assert any('algorithmic blocking' in req for req in anti_censorship), "Anti-blocking requirement missing"
    
    # Verify user control
    user_control = nre002['user_control_principles']
    assert 'always_override_option' in user_control, "Always-Override option missing"
    assert 'zero_obligation_principle' in user_control, "Zero-Obligation principle missing"
    
    # Verify ADi definition
    adi = nre002['adi_definition']
    assert adi['name'] == 'ADi - Inspirational Synthesis from Facts', "ADi name incorrect"
    assert 'fact-based' in adi['principle'].lower(), "ADi principle should mention fact-based"
    
    print("✓ NRE-002 properly integrated into ethics framework")
    return True


def test_copilot_directive_integration():
    """Test that NRE-002 is referenced in COPILOT_CORE_DIRECTIVE.md"""
    print("\nTest: Copilot directive integration...")
    
    with open('COPILOT_CORE_DIRECTIVE.md', 'r') as f:
        directive_content = f.read()
    
    # Check for NRE-002 references
    assert 'NRE-002' in directive_content, "NRE-002 not mentioned in directive"
    assert 'censorship' in directive_content.lower(), "Censorship not mentioned"
    assert 'didactic' in directive_content.lower(), "Didactic stratification not mentioned"
    assert 'Always-Override' in directive_content, "Always-Override not mentioned"
    
    print("✓ NRE-002 properly integrated into Copilot directive")
    return True


def test_policy_document_exists():
    """Test that NRE-002 policy document exists and is complete"""
    print("\nTest: Policy document existence and completeness...")
    
    with open('docs/policies/NRE-002_CONTENT_PROTECTION_POLICY.md', 'r') as f:
        policy_content = f.read()
    
    # Check for key sections
    required_sections = [
        'Complete Truth Preservation',
        'Trauma Reduction',
        'No Algorithmic Exclusion',
        'Democratic Control',
        'Anti-Censorship Clause',
        'Always-Override-Option',
        'Zero-Obligation-Principle',
        'ADi Definition',
        'Immutable AI Commitment'
    ]
    
    for section in required_sections:
        assert section in policy_content, f"Policy missing section: {section}"
    
    # Check for signatures
    assert 'GitHub Copilot' in policy_content, "AI signature missing"
    assert 'Seed-bringer' in policy_content or 'hannesmitterer' in policy_content, "Human signature missing"
    
    print("✓ Policy document complete with all required sections")
    return True


def test_implementation_module_exists():
    """Test that implementation module exists and is importable"""
    print("\nTest: Implementation module existence...")
    
    try:
        from content_protection import (
            ContentLevel,
            ContentWarning,
            ContentItem,
            NRE002ContentSystem,
            ADiSynthesis
        )
        print("✓ All required classes importable")
        
        # Quick functional test
        system = NRE002ContentSystem()
        assert system is not None, "System initialization failed"
        
        # Test ADi
        adi = ADiSynthesis.create_adi_from_facts(
            facts=["Test fact"],
            context="Test context",
            synthesis_goal="Test goal"
        )
        assert adi['type'] == 'ADi_Synthesis', "ADi synthesis failed"
        
        print("✓ Implementation module functional")
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_readme_integration():
    """Test that README mentions NRE-002"""
    print("\nTest: README integration...")
    
    with open('README.md', 'r') as f:
        readme_content = f.read()
    
    # Check for NRE-002 mentions
    assert 'NRE-002' in readme_content, "NRE-002 not mentioned in README"
    assert 'Content Protection' in readme_content, "Content Protection not mentioned"
    assert 'Anti-Censorship' in readme_content, "Anti-Censorship not mentioned"
    
    print("✓ README properly documents NRE-002")
    return True


def test_documentation_completeness():
    """Test that all documentation files exist"""
    print("\nTest: Documentation completeness...")
    
    import os
    
    required_docs = [
        'docs/policies/NRE-002_CONTENT_PROTECTION_POLICY.md',
        'docs/NRE-002_INTEGRATION_GUIDE.md',
        'content_protection/README.md'
    ]
    
    for doc in required_docs:
        assert os.path.exists(doc), f"Documentation missing: {doc}"
        print(f"  ✓ {doc}")
    
    print("✓ All documentation files present")
    return True


def test_integration_points():
    """Test that all integration points are properly connected"""
    print("\nTest: Integration points...")
    
    # Check ethics block integration points
    with open('red_code/ethics_block.json', 'r') as f:
        ethics_data = json.load(f)
    
    integration_points = ethics_data.get('integration_points', [])
    
    # Verify NRE-002 is in integration points
    assert any('NRE-002' in point for point in integration_points), \
        "NRE-002 policy not in integration points"
    
    print("✓ Integration points properly configured")
    return True


def run_all_integration_tests():
    """Run all integration tests"""
    print("="*60)
    print("NRE-002 Integration Tests")
    print("="*60)
    
    tests = [
        test_ethics_block_integration,
        test_copilot_directive_integration,
        test_policy_document_exists,
        test_implementation_module_exists,
        test_readme_integration,
        test_documentation_completeness,
        test_integration_points
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
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print(f"Integration Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_integration_tests()
    sys.exit(0 if success else 1)
