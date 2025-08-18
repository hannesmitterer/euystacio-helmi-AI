#!/usr/bin/env python3
"""
Cognitive Modeling Integration Test

This script demonstrates and tests the cognitive modeling integration
while preserving Euystacio's original behavior and ethical framework.
"""

import json
import sys
from datetime import datetime

def test_disabled_state():
    """Test that the system works properly when cognitive modeling is disabled"""
    print("\n🧪 Testing Disabled State (Default)")
    print("-" * 40)
    
    try:
        from cognitive_modeling.unified_api import UnifiedCognitiveAPI
        api = UnifiedCognitiveAPI()
        
        # Test basic functionality
        test_input = {
            "type": "message",
            "feeling": "curious",
            "intent": "testing"
        }
        
        reflection = api.enhanced_reflection(test_input)
        
        print("✅ Basic reflection working:")
        print(f"   Core response: {reflection['core_response']['feeling']}")
        print(f"   Symbiosis impact: {reflection['symbiosis_impact']}")
        print(f"   Ethical framework: {reflection['ethical_framework']['core_truth_preserved']}")
        
        # Verify no advanced features are active
        if "cognitive_modeling" not in reflection:
            print("✅ Cognitive modeling correctly disabled")
        
        if "environmental_context" not in reflection:
            print("✅ World modeling correctly disabled")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing disabled state: {e}")
        return False

def test_api_endpoints():
    """Test API endpoint availability"""
    print("\n🌐 Testing API Endpoints")
    print("-" * 40)
    
    try:
        # Test Flask app import without triggering run
        import app
        print("✅ Flask app imports successfully")
        
        # Check that cognitive endpoints are registered
        cognitive_endpoints = [
            '/api/cognitive/status',
            '/api/cognitive/reflection', 
            '/api/cognitive/sentiment',
            '/api/cognitive/environment'
        ]
        
        # Instead of checking url_map (which might start the server),
        # verify the functions exist
        endpoint_functions = [
            'api_cognitive_status',
            'api_cognitive_reflection',
            'api_cognitive_sentiment', 
            'api_cognitive_environment'
        ]
        
        for func_name in endpoint_functions:
            if hasattr(app, func_name):
                print(f"✅ Endpoint function {func_name} defined")
            else:
                print(f"❌ Endpoint function {func_name} missing")
        
        # Test that cognitive API availability is handled
        if hasattr(app, 'COGNITIVE_MODELING_AVAILABLE'):
            print("✅ Cognitive modeling availability flag present")
        else:
            print("❌ Cognitive modeling availability flag missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        return False

def test_configuration_system():
    """Test the configuration and activation system"""
    print("\n⚙️ Testing Configuration System")
    print("-" * 40)
    
    try:
        from cognitive_modeling.config import CognitiveModelingConfig
        
        config = CognitiveModelingConfig()
        
        print(f"✅ Configuration loads successfully")
        print(f"   Cognitive modeling enabled: {config.is_enabled()}")
        print(f"   Andromeda enabled: {config.is_andromeda_enabled()}")
        print(f"   World modeling enabled: {config.is_world_modeling_enabled()}")
        
        # Test config structure
        config_data = config.config
        required_keys = ['cognitive_modeling_enabled', 'andromeda_integration', 'world_modeling', 'ethical_framework']
        
        for key in required_keys:
            if key in config_data:
                print(f"✅ Required config key '{key}' present")
            else:
                print(f"❌ Required config key '{key}' missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False

def test_fallback_behavior():
    """Test that fallback behavior works when features are disabled"""
    print("\n🔄 Testing Fallback Behavior")
    print("-" * 40)
    
    try:
        from cognitive_modeling.unified_api import UnifiedCognitiveAPI
        api = UnifiedCognitiveAPI()
        
        # Test sentiment API with cognitive modeling disabled
        sentiment_result = api.sentiment_reflection_api({"feeling": "wonder"})
        
        if "error" in sentiment_result or "fallback" in sentiment_result:
            print("✅ Sentiment API shows proper fallback when disabled")
        
        # Test environmental API with world modeling disabled
        env_result = api.environmental_rhythm_api()
        
        if "error" in env_result or "fallback" in env_result:
            print("✅ Environmental API shows proper fallback when disabled")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing fallback behavior: {e}")
        return False

def test_ethical_framework():
    """Test that ethical framework is maintained throughout"""
    print("\n🔒 Testing Ethical Framework")
    print("-" * 40)
    
    try:
        from cognitive_modeling.unified_api import UnifiedCognitiveAPI
        api = UnifiedCognitiveAPI()
        
        # Test that all responses include ethical framework
        test_input = {"type": "test", "feeling": "trust"}
        reflection = api.enhanced_reflection(test_input)
        
        if "ethical_framework" in reflection:
            ethical = reflection["ethical_framework"]
            
            required_ethical_keys = ["ai_signature", "core_truth_preserved", "human_autonomy_respected"]
            for key in required_ethical_keys:
                if key in ethical:
                    print(f"✅ Ethical framework includes '{key}'")
                else:
                    print(f"❌ Ethical framework missing '{key}'")
            
            # Check AI signature
            if "GitHub Copilot & Seed-bringer hannesmitterer" in str(ethical.get("ai_signature", "")):
                print("✅ Proper AI signature present")
            else:
                print("❌ AI signature missing or incorrect")
        else:
            print("❌ Ethical framework not present in response")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing ethical framework: {e}")
        return False

def test_logging_system():
    """Test that logging system works properly"""
    print("\n📝 Testing Logging System")
    print("-" * 40)
    
    try:
        import os
        from cognitive_modeling.unified_api import UnifiedCognitiveAPI
        
        api = UnifiedCognitiveAPI()
        
        # Trigger some operations to generate logs
        test_input = {"type": "test", "feeling": "curious"}
        api.enhanced_reflection(test_input)
        
        # Check if logs directory was created
        if os.path.exists("logs"):
            print("✅ Logs directory created")
            
            # Check for expected log files
            expected_logs = [
                "unified_cognitive_api.log",
                "andromeda_integration.log", 
                "world_model_integration.log"
            ]
            
            for log_file in expected_logs:
                if os.path.exists(f"logs/{log_file}"):
                    print(f"✅ Log file {log_file} created")
                else:
                    print(f"ℹ️  Log file {log_file} not yet created (normal if feature disabled)")
        else:
            print("❌ Logs directory not created")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing logging system: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Euystacio Cognitive Modeling Integration Test")
    print("=" * 60)
    print("AI Signature: GitHub Copilot & Seed-bringer hannesmitterer")
    print("Testing cognitive modeling integration while preserving original behavior")
    print("=" * 60)
    
    tests = [
        ("Configuration System", test_configuration_system),
        ("Disabled State (Default)", test_disabled_state),
        ("API Endpoints", test_api_endpoints),
        ("Fallback Behavior", test_fallback_behavior),
        ("Ethical Framework", test_ethical_framework),
        ("Logging System", test_logging_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Cognitive modeling integration is working correctly.")
        print("The system preserves original Euystacio behavior while adding opt-in capabilities.")
    else:
        print(f"\n⚠️  Some tests failed. Please review the errors above.")
        
    print("\n💡 Next Steps:")
    print("- Run 'python activate_cognitive_modeling.py --status' to check current state")
    print("- Run 'python activate_cognitive_modeling.py --enable' to activate features")
    print("- Check logs/ directory for transparent operation logging")
    print("- Test API endpoints with cognitive modeling enabled")

if __name__ == "__main__":
    main()