"""
integration_example.py - Example integration of Lex Amoris Security with Euystacio Framework

This example demonstrates how to integrate the Lex Amoris security system with
existing Euystacio components like red_code, sentimento_pulse_interface, and
ethical_shield.
"""

import json
from datetime import datetime, timezone
from lex_amoris_security import LexAmorisSecuritySystem
from red_code import load_red_code, save_red_code, ensure_red_code


def integrate_with_red_code():
    """
    Example: Integrate Lex Amoris security status with red_code.json
    """
    print("=" * 60)
    print("Lex Amoris Security + Red Code Integration")
    print("=" * 60)
    
    # Ensure red_code.json exists
    ensure_red_code()
    
    # Initialize security system
    security = LexAmorisSecuritySystem()
    
    # Load existing red_code
    red_code_data = load_red_code()
    print(f"\n✓ Loaded red_code.json")
    print(f"  Current symbiosis level: {red_code_data.get('symbiosis_level', 0)}")
    
    # Get security system status
    security_status = security.get_system_status()
    
    # Add Lex Amoris security information to red_code
    red_code_data['lex_amoris_security'] = {
        "enabled": True,
        "last_update": datetime.now(timezone.utc).isoformat(),
        "lazy_security_active": security_status['lazy_security']['is_active'],
        "blacklisted_sources": security_status['blacklist']['total_blocked'],
        "total_validations": security_status['rhythm_validation']['total_validations'],
        "total_rescues": security_status['rescue_channel']['total_rescues']
    }
    
    # Save updated red_code
    save_red_code(red_code_data)
    print(f"\n✓ Updated red_code.json with Lex Amoris security status")
    print(f"  Lazy security active: {security_status['lazy_security']['is_active']}")
    print(f"  Blacklisted sources: {security_status['blacklist']['total_blocked']}")
    
    return security, red_code_data


def process_sentimento_pulse_with_security(emotion="love", intensity=0.9):
    """
    Example: Process emotional pulse through security validation
    """
    print("\n" + "=" * 60)
    print("Lex Amoris Security + Sentimento Pulse Integration")
    print("=" * 60)
    
    # Initialize security system
    security = LexAmorisSecuritySystem()
    
    # Create sentimento pulse data
    pulse_data = {
        "emotion": emotion,
        "intensity": intensity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "sentimento_pulse_interface",
        "lex_amoris_signature": "love_first_protocol"
    }
    
    # Process through security
    result = security.process_packet(pulse_data, "internal")
    
    print(f"\n📡 Sentimento Pulse:")
    print(f"  Emotion: {emotion}")
    print(f"  Intensity: {intensity}")
    
    if result["accepted"]:
        print(f"\n✓ Pulse ACCEPTED by security system")
        print(f"  Reason: {result['reason']}")
        
        # Calculate rhythm frequency
        frequency = security.rhythm_validator.calculate_packet_frequency(pulse_data)
        print(f"  Harmonic frequency: {frequency:.2f} Hz")
        print(f"  Base frequency: {security.rhythm_validator.base_frequency} Hz")
        
        return True, pulse_data
    else:
        print(f"\n✗ Pulse REJECTED by security system")
        print(f"  Reason: {result['reason']}")
        return False, None


def create_complete_backup():
    """
    Example: Create complete IPFS backup of all configurations
    """
    print("\n" + "=" * 60)
    print("Lex Amoris Security - Configuration Backup")
    print("=" * 60)
    
    # Initialize security system
    security = LexAmorisSecuritySystem()
    
    # Create backup
    manifest = security.create_configuration_backup()
    
    print(f"\n💾 Backup created:")
    print(f"  Timestamp: {manifest['timestamp']}")
    print(f"  Files backed up: {len(manifest['files'])}")
    
    for file_path, file_info in manifest['files'].items():
        if 'hash' in file_info:
            print(f"\n  ✓ {file_path}")
            print(f"    Hash: {file_info['hash'][:16]}...")
            print(f"    Size: {file_info['size']} bytes")
    
    return manifest


def demonstrate_rescue_channel():
    """
    Example: Demonstrate rescue channel functionality
    """
    print("\n" + "=" * 60)
    print("Lex Amoris Security - Rescue Channel")
    print("=" * 60)
    
    # Initialize security system
    security = LexAmorisSecuritySystem()
    
    # Simulate multiple failed validations from same source
    source_ip = "192.168.1.100"
    
    print(f"\n🔒 Simulating validation failures for {source_ip}...")
    
    # Create some invalid packets
    for i in range(6):
        invalid_data = {"test": f"invalid_{i}"}
        result = security.process_packet(invalid_data, source_ip)
        
        if not result["accepted"]:
            print(f"  ✗ Validation {i+1} failed")
    
    # Check if source is blacklisted
    is_blacklisted = security.blacklist.is_blacklisted(source_ip)
    print(f"\n  Source blacklisted: {is_blacklisted}")
    
    # Create validation log with high false positive rate
    validation_log = []
    for i in range(10):
        validation_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": source_ip,
            "valid": i % 2 == 0  # 50% false positive rate
        })
    
    # Check if rescue should be triggered
    should_rescue = security.rescue_channel.should_trigger_rescue(validation_log)
    
    if should_rescue:
        print(f"\n💖 Rescue triggered - high false positive rate detected")
        
        # Send rescue message
        rescue_msg = security.rescue_channel.send_rescue_message(
            source_ip,
            "Compassionate unblocking due to false positive pattern"
        )
        
        print(f"  Rescue message sent:")
        print(f"    Action: {rescue_msg['action']}")
        print(f"    Compassion level: {rescue_msg['compassion_level']}")
        print(f"    Lex Amoris signature: {rescue_msg['lex_amoris_signature']}")
    else:
        print(f"\n  Rescue not needed - false positive rate acceptable")


def main():
    """
    Run all integration examples
    """
    print("\n" + "=" * 60)
    print("LEX AMORIS SECURITY - INTEGRATION EXAMPLES")
    print("Demonstrating integration with Euystacio Framework")
    print("=" * 60)
    
    try:
        # Example 1: Red Code Integration
        security, red_code = integrate_with_red_code()
        
        # Example 2: Sentimento Pulse Integration
        accepted, pulse = process_sentimento_pulse_with_security("harmony", 0.95)
        
        # Example 3: IPFS Backup
        backup_manifest = create_complete_backup()
        
        # Example 4: Rescue Channel
        demonstrate_rescue_channel()
        
        # Final status
        print("\n" + "=" * 60)
        print("INTEGRATION EXAMPLES COMPLETED")
        print("=" * 60)
        
        final_status = security.get_system_status()
        
        print(f"\n📊 Final Security Status:")
        print(f"  Lazy security active: {final_status['lazy_security']['is_active']}")
        print(f"  Total validations: {final_status['rhythm_validation']['total_validations']}")
        print(f"  Blocked sources: {final_status['blacklist']['total_blocked']}")
        print(f"  Rescue operations: {final_status['rescue_channel']['total_rescues']}")
        
        print(f"\n✅ All integrations successful!")
        print(f"   Lex Amoris principles maintained:")
        print(f"     - Love First ✓")
        print(f"     - Compassionate Enforcement ✓")
        print(f"     - Harmonic Validation (432 Hz) ✓")
        print(f"     - Energy Efficiency ✓")
        
    except Exception as e:
        print(f"\n❌ Error during integration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
