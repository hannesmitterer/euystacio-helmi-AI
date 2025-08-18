#!/usr/bin/env python3
"""
Cognitive Modeling Activation Script

This script allows users to easily enable cognitive modeling features
while maintaining Euystacio's ethical framework and accountability.

Usage:
    python activate_cognitive_modeling.py --enable
    python activate_cognitive_modeling.py --disable
    python activate_cognitive_modeling.py --status
"""

import argparse
import json
import sys
from datetime import datetime
from cognitive_modeling.config import CognitiveModelingConfig

def print_header():
    print("\n" + "="*60)
    print("🧠 Euystacio Cognitive Modeling Activation")
    print("="*60)
    print("AI Signature: GitHub Copilot & Seed-bringer hannesmitterer")
    print("Part of Euystacio-Helmi AI ethical framework")
    print("="*60)

def print_ethical_notice():
    print("\n🔒 ETHICAL FRAMEWORK NOTICE:")
    print("- All cognitive modeling features are opt-in only")
    print("- Original Euystacio behavior is preserved")
    print("- Human oversight is maintained at all times")
    print("- Full transparency and logging is enabled")
    print("- You can disable features at any time")

def show_status():
    print_header()
    
    config = CognitiveModelingConfig()
    
    print("\n📊 Current Status:")
    print(f"Cognitive Modeling Enabled: {'✅ Yes' if config.is_enabled() else '❌ No'}")
    print(f"Andromeda Integration:      {'✅ Yes' if config.is_andromeda_enabled() else '❌ No'}")
    print(f"World Modeling:             {'✅ Yes' if config.is_world_modeling_enabled() else '❌ No'}")
    
    if config.is_enabled():
        andromeda_config = config.get_andromeda_config()
        world_config = config.get_world_model_config()
        
        print(f"\n🔧 Configuration Details:")
        print(f"Andromeda Model Size:       {andromeda_config.get('model_size', 'small')}")
        print(f"Environmental Sensing:      {'✅' if world_config.get('environmental_sensing') else '❌'}")
        print(f"Rhythm Analysis:            {'✅' if world_config.get('rhythm_analysis') else '❌'}")
        print(f"Ethical Constraints:        {'✅' if andromeda_config.get('ethical_constraints') else '❌'}")
    
    print(f"\n📝 Available API Endpoints (when enabled):")
    print("- GET  /api/cognitive/status")
    print("- POST /api/cognitive/reflection")
    print("- POST /api/cognitive/sentiment")
    print("- GET  /api/cognitive/environment")

def enable_cognitive_modeling():
    print_header()
    print_ethical_notice()
    
    print("\n⚠️  IMPORTANT: You are about to enable cognitive modeling features.")
    print("This will extend Euystacio's capabilities while preserving its core philosophy.")
    
    response = input("\nDo you understand and agree to enable these features? (yes/no): ").lower().strip()
    
    if response not in ['yes', 'y']:
        print("\n❌ Activation cancelled. Cognitive modeling remains disabled.")
        return
    
    print("\n🔧 Configuring cognitive modeling features...")
    
    # Get user preferences
    enable_andromeda = True
    enable_world_modeling = True
    
    andromeda_choice = input("Enable Andromeda cognitive modeling? (Y/n): ").lower().strip()
    if andromeda_choice in ['n', 'no']:
        enable_andromeda = False
    
    world_choice = input("Enable world/environmental modeling? (Y/n): ").lower().strip()
    if world_choice in ['n', 'no']:
        enable_world_modeling = False
    
    # Activate with ethical logging
    config = CognitiveModelingConfig()
    config.enable_cognitive_modeling(
        enable_andromeda=enable_andromeda,
        enable_world_modeling=enable_world_modeling
    )
    
    print("\n✅ Cognitive modeling activated successfully!")
    print("\n📋 What was enabled:")
    print(f"- Cognitive Modeling Core:  ✅ Enabled")
    print(f"- Andromeda Integration:    {'✅ Enabled' if enable_andromeda else '❌ Disabled'}")
    print(f"- World Modeling:           {'✅ Enabled' if enable_world_modeling else '❌ Disabled'}")
    
    print("\n🔄 Next Steps:")
    print("1. Restart your Euystacio application")
    print("2. Check /api/cognitive/status to verify activation")
    print("3. Monitor logs/cognitive_modeling_activation.log for full transparency")
    print("4. Use new API endpoints for enhanced capabilities")
    
    print("\n💡 Remember: You can disable these features anytime with:")
    print("   python activate_cognitive_modeling.py --disable")

def disable_cognitive_modeling():
    print_header()
    
    config = CognitiveModelingConfig()
    
    if not config.is_enabled():
        print("\n✅ Cognitive modeling is already disabled.")
        return
    
    print("\n⚠️  You are about to disable cognitive modeling features.")
    print("This will return Euystacio to its original behavior.")
    
    response = input("Are you sure you want to disable cognitive modeling? (yes/no): ").lower().strip()
    
    if response not in ['yes', 'y']:
        print("\n❌ Deactivation cancelled. Cognitive modeling remains enabled.")
        return
    
    # Disable features
    config.config["cognitive_modeling_enabled"] = False
    config.config["andromeda_integration"]["enabled"] = False
    config.config["world_modeling"]["enabled"] = False
    config._save_config(config.config)
    
    # Log deactivation
    deactivation_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "cognitive_modeling_deactivation",
        "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
        "user_initiated": True
    }
    
    with open("logs/cognitive_modeling_activation.log", "a") as f:
        f.write(json.dumps(deactivation_log) + "\n")
    
    print("\n✅ Cognitive modeling disabled successfully!")
    print("\n📋 What was disabled:")
    print("- All cognitive modeling features")
    print("- Enhanced API endpoints")
    print("- Extended processing capabilities")
    
    print("\n🔄 Next Steps:")
    print("1. Restart your Euystacio application")
    print("2. Euystacio will return to its original behavior")
    print("3. Check logs/cognitive_modeling_activation.log for transparency")
    
    print("\n💡 You can re-enable anytime with:")
    print("   python activate_cognitive_modeling.py --enable")

def main():
    parser = argparse.ArgumentParser(
        description="Activate or deactivate cognitive modeling features for Euystacio",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--enable', 
        action='store_true',
        help='Enable cognitive modeling features (interactive)'
    )
    
    parser.add_argument(
        '--disable',
        action='store_true', 
        help='Disable cognitive modeling features (interactive)'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show current status of cognitive modeling'
    )
    
    args = parser.parse_args()
    
    if args.enable:
        enable_cognitive_modeling()
    elif args.disable:
        disable_cognitive_modeling()
    elif args.status:
        show_status()
    else:
        print_header()
        print("\n🤖 Cognitive Modeling Management")
        print("\nUsage:")
        print("  python activate_cognitive_modeling.py --enable   # Enable features")
        print("  python activate_cognitive_modeling.py --disable  # Disable features") 
        print("  python activate_cognitive_modeling.py --status   # Show status")
        print("\nFor help: python activate_cognitive_modeling.py --help")

if __name__ == "__main__":
    main()