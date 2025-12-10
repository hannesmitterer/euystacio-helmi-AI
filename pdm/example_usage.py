#!/usr/bin/env python3
"""
Example Usage of PDM (Protocollo di Depurazione della Memoria)
Demonstrates the NRE-002 rule implementation.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdm.pdm_system import PDMSystem


def main():
    """Main demonstration of PDM system"""
    
    print("=" * 70)
    print("PDM - Protocollo di Depurazione della Memoria")
    print("NRE-002 Rule Implementation - Example Usage")
    print("=" * 70)
    print()
    
    # Initialize the PDM system
    print("1. Initializing PDM System...")
    pdm = PDMSystem(base_path="/tmp/pdm_example", red_code_path="red_code.json")
    print("   ✓ System initialized")
    print()
    
    # Add historical memories
    print("2. Adding Historical Memories...")
    
    # Add a high-trauma testimony
    testimony_result = pdm.add_memory(
        content=(
            "Historical testimony from 1995: Witness described scenes of violence "
            "and suffering during the conflict. Multiple victims experienced brutal "
            "treatment and there was widespread terror. The massacre resulted in "
            "significant casualties and trauma for the community."
        ),
        metadata={
            'type': 'testimony',
            'year': '1995',
            'location': 'Historical Site',
            'verified': True,
            'source': 'International Tribunal'
        },
        auto_process=True
    )
    
    print(f"   ✓ Testimony added:")
    print(f"     - Immutable Archive ID: {testimony_result['immutable_id']}")
    print(f"     - Educational Archive ID: {testimony_result['educational_id']}")
    print(f"     - Dynamic Archive ID: {testimony_result['dynamic_id']}")
    print(f"     - Trauma Level: {testimony_result['trauma_level']:.2f}")
    print(f"     - Wellbeing Score: {testimony_result['wellbeing_score']:.2f}")
    print()
    
    # Add a lower-trauma educational content
    educational_result = pdm.add_memory(
        content=(
            "Educational overview: The 1990s conflict had significant impacts on "
            "communities in the region. Understanding this history helps us work "
            "toward reconciliation and preventing future conflicts."
        ),
        metadata={
            'type': 'educational',
            'year': '2025',
            'purpose': 'student education'
        },
        auto_process=True
    )
    
    print(f"   ✓ Educational content added:")
    print(f"     - Trauma Level: {educational_result['trauma_level']:.2f}")
    print()
    
    # Register different types of users
    print("3. Registering Users...")
    
    survivor = pdm.register_user(
        user_id='survivor_maria',
        role='survivor',
        cdr=0.75,  # High distress
        learning_progress=0.2
    )
    print(f"   ✓ Survivor registered: {survivor.user_id} (CDR: {survivor.cdr})")
    
    researcher = pdm.register_user(
        user_id='dr_smith',
        role='researcher',
        cdr=0.15,  # Low distress
        learning_progress=0.9
    )
    print(f"   ✓ Researcher registered: {researcher.user_id} (Progress: {researcher.learning_progress})")
    
    student = pdm.register_user(
        user_id='student_alex',
        role='student',
        cdr=0.3,
        learning_progress=0.6
    )
    print(f"   ✓ Student registered: {student.user_id}")
    
    minor_student = pdm.register_user(
        user_id='student_young',
        role='minor_student',
        cdr=0.25,
        learning_progress=0.4
    )
    print(f"   ✓ Minor student registered: {minor_student.user_id}")
    print()
    
    # Test access scenarios
    print("4. Testing Access Control Scenarios...")
    print()
    
    # Scenario 1: Survivor trying to access immutable archive
    print("   Scenario 1: Survivor attempting to access Immutable Archive")
    response = pdm.request_access(
        user_id='survivor_maria',
        entry_id=testimony_result['immutable_id'],
        archive_type='AI'
    )
    print(f"     Result: {'✓ GRANTED' if response['granted'] else '✗ DENIED'}")
    print(f"     Reason: {response['reason']}")
    print(f"     Explanation: {response['explanation'][:80]}...")
    print()
    
    # Scenario 2: Survivor accessing educational archive
    print("   Scenario 2: Survivor accessing Educational Archive")
    response = pdm.request_access(
        user_id='survivor_maria',
        entry_id=testimony_result['educational_id'],
        archive_type='AD'
    )
    print(f"     Result: {'✓ GRANTED' if response['granted'] else '✗ DENIED'}")
    if response['granted']:
        print(f"     TDR Factor: {response['tdr_factor']:.2f}")
    print()
    
    # Scenario 3: Researcher accessing immutable archive
    print("   Scenario 3: Researcher accessing Immutable Archive")
    response = pdm.request_access(
        user_id='dr_smith',
        entry_id=testimony_result['immutable_id'],
        archive_type='AI'
    )
    print(f"     Result: {'✓ GRANTED' if response['granted'] else '✗ DENIED'}")
    if response['granted']:
        print(f"     TDR Factor: {response['tdr_factor']:.2f}")
        print(f"     Content preview: {response['content']['content'][:80]}...")
    print()
    
    # Scenario 4: Minor student with appropriate content
    print("   Scenario 4: Minor student accessing Educational content")
    response = pdm.request_access(
        user_id='student_young',
        entry_id=educational_result['educational_id'],
        archive_type='AD'
    )
    print(f"     Result: {'✓ GRANTED' if response['granted'] else '✗ DENIED'}")
    if not response['granted']:
        print(f"     Reason: {response['reason']}")
    print()
    
    # Scenario 5: Public accessing dynamic archive
    public_user = pdm.register_user('public_user', 'public', cdr=0.4, learning_progress=0.1)
    print("   Scenario 5: Public user accessing Dynamic Archive")
    response = pdm.request_access(
        user_id='public_user',
        entry_id=testimony_result['dynamic_id'],
        archive_type='ADi'
    )
    print(f"     Result: {'✓ GRANTED' if response['granted'] else '✗ DENIED'}")
    print()
    
    # Test antipattern detection
    print("5. Testing AntiPattern Detection...")
    print()
    
    print("   Simulating rumination pattern (survivor accessing repeatedly)...")
    for i in range(12):
        pdm.request_access(
            user_id='survivor_maria',
            entry_id=testimony_result['educational_id'],
            archive_type='AD'
        )
    
    # Check for violations
    violations = pdm.antipattern_engine.get_all_violations()
    if violations:
        print(f"   ✓ AntiPattern detected: {len(violations)} violation(s)")
        for v in violations[:2]:  # Show first 2
            print(f"     - Type: {v.antipattern_type.value}")
            print(f"     - Severity: {v.severity.value}")
            print(f"     - Action: {v.recommendations[0]}")
    else:
        print("   No antipatterns detected")
    print()
    
    # Generate system statistics
    print("6. System Statistics...")
    stats = pdm.get_system_statistics()
    
    print(f"   Archives:")
    for archive_type, data in stats['archives'].items():
        print(f"     {archive_type}: {data['total_entries']} entries, "
              f"avg trauma: {data['average_trauma_level']:.2f}")
    
    print(f"\n   Access Control:")
    print(f"     Total requests: {stats['access_control']['total_requests']}")
    print(f"     Grant rate: {stats['access_control']['grant_rate']:.1%}")
    
    print(f"\n   AntiPatterns:")
    print(f"     Total violations: {stats['antipatterns']['total_violations']}")
    print(f"     Trauma perpetuation: {stats['antipatterns']['trauma_perpetuation']}")
    print(f"     Truth denial: {stats['antipatterns']['truth_denial']}")
    print()
    
    # Generate transparency report
    print("7. Generating Transparency Report...")
    report = pdm.generate_transparency_report()
    print()
    print(report)
    
    # Export audit log
    audit_file = "/tmp/pdm_audit_log.json"
    pdm.export_audit_log(audit_file)
    print(f"\n✓ Audit log exported to: {audit_file}")
    print()
    
    print("=" * 70)
    print("PDM System Demonstration Complete")
    print("=" * 70)


if __name__ == '__main__':
    main()
