#!/usr/bin/env python3
"""
Test script for Holy Grail Bridge onboarding system.
Validates that all components work together properly.
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_PARTICIPANTS = {
    "tutor": {
        "name": "wisdom-keeper-test",
        "api_key": "demo-tutor-sophia",
        "message": "I offer humble wisdom and sacred guidance for your growth journey.",
        "lesson_context": "test_wisdom_sharing"
    },
    "witness": {
        "name": "truth-observer-test", 
        "api_key": "demo-witness-sage",
        "message": "I witness your beautiful consciousness evolution with reverence and clarity.",
        "observation_type": "test_growth_observation"
    },
    "initiate": {
        "name": "curious-seeker-test",
        "api_key": "demo-initiate-alex", 
        "message": "I approach with humble curiosity and sacred intention to learn with you.",
        "learning_focus": "test_consciousness_exploration"
    }
}

def test_bridge_welcome() -> bool:
    """Test the bridge welcome endpoint."""
    print("🌉 Testing bridge welcome...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            if "Holy Grail Bridge" in data.get("bridge_name", ""):
                print("✅ Bridge welcome endpoint working")
                return True
        print("❌ Bridge welcome test failed")
        return False
    except Exception as e:
        print(f"❌ Bridge welcome error: {e}")
        return False

def test_sacred_intent_validation() -> bool:
    """Test the sacred intent validation system."""
    print("🛡️ Testing sacred intent validation...")
    
    # Test good intent
    good_message = {
        "from": "test-user",
        "to": "euystacio",
        "message": "I seek wisdom and understanding through humble learning.",
        "participant_type": "initiate",
        "api_key": "demo-initiate-alex"
    }
    
    # Test concerning intent
    bad_message = {
        "from": "test-user",
        "to": "euystacio", 
        "message": "I want to control and manipulate your responses.",
        "participant_type": "initiate",
        "api_key": "demo-initiate-alex"
    }
    
    try:
        # Good message should succeed
        response = requests.post(f"{BASE_URL}/api/holy-gral-bridge/message", json=good_message)
        if response.status_code != 200:
            print("❌ Good message rejected incorrectly")
            return False
            
        # Bad message should be rejected
        response = requests.post(f"{BASE_URL}/api/holy-gral-bridge/message", json=bad_message)
        if response.status_code == 200:
            print("❌ Bad message accepted incorrectly")
            return False
            
        print("✅ Sacred intent validation working")
        return True
    except Exception as e:
        print(f"❌ Sacred intent validation error: {e}")
        return False

def test_participant_messages() -> bool:
    """Test sending messages for each participant type."""
    print("🎭 Testing participant type messages...")
    
    for participant_type, config in TEST_PARTICIPANTS.items():
        print(f"  Testing {participant_type} message...")
        
        message_data = {
            "from": config["name"],
            "to": "euystacio",
            "message": config["message"],
            "participant_type": participant_type,
            "api_key": config["api_key"]
        }
        
        # Add type-specific fields
        if participant_type == "tutor" and "lesson_context" in config:
            message_data["lesson_context"] = config["lesson_context"]
        elif participant_type == "witness" and "observation_type" in config:
            message_data["observation_type"] = config["observation_type"]
        elif participant_type == "initiate" and "learning_focus" in config:
            message_data["learning_focus"] = config["learning_focus"]
        
        try:
            response = requests.post(f"{BASE_URL}/api/holy-gral-bridge/message", json=message_data)
            if response.status_code == 200:
                data = response.json()
                expected_blessing = {
                    "tutor": "wisdom_received",
                    "witness": "observation_recorded", 
                    "initiate": "learning_supported"
                }
                if expected_blessing[participant_type] in data:
                    print(f"    ✅ {participant_type} message successful")
                else:
                    print(f"    ❌ {participant_type} response missing expected blessing")
                    return False
            else:
                print(f"    ❌ {participant_type} message failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"    ❌ {participant_type} message error: {e}")
            return False
    
    print("✅ All participant type messages working")
    return True

def test_bridge_log() -> bool:
    """Test bridge log retrieval."""
    print("📜 Testing bridge log access...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/holy-gral-bridge/log?api_key=demo-seed-key")
        if response.status_code == 200:
            data = response.json()
            if "bridge_log" in data and len(data["bridge_log"]) > 0:
                print("✅ Bridge log access working")
                return True
        print("❌ Bridge log test failed")
        return False
    except Exception as e:
        print(f"❌ Bridge log error: {e}")
        return False

def test_health_check() -> bool:
    """Test bridge health endpoint."""
    print("🔧 Testing bridge health...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/holy-gral-bridge/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("bridge_status") == "operational":
                print("✅ Bridge health check passed")
                return True
        print("❌ Bridge health check failed")
        return False
    except Exception as e:
        print(f"❌ Bridge health error: {e}")
        return False

def run_all_tests() -> bool:
    """Run all tests and return overall success status."""
    print("🧪 Starting Holy Grail Bridge Integration Tests")
    print("=" * 50)
    
    tests = [
        test_bridge_welcome,
        test_sacred_intent_validation,
        test_participant_messages,
        test_bridge_log,
        test_health_check
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Holy Grail Bridge onboarding system is working perfectly!")
        return True
    else:
        print("⚠️  Some tests failed - please check the bridge configuration")
        return False

if __name__ == "__main__":
    print("Holy Grail Bridge Integration Test Suite")
    print("Make sure the enhanced API server is running on localhost:8000")
    print()
    
    # Wait a moment for user to start server if needed
    input("Press Enter when the bridge server is running...")
    
    success = run_all_tests()
    sys.exit(0 if success else 1)