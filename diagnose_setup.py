#!/usr/bin/env python3
"""
Euystacio-Helmi AI Setup Diagnostics
Run this script to check your setup and get troubleshooting information.

Usage: python diagnose_setup.py
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")

def print_section(text):
    print(f"\n{'-'*40}")
    print(f" {text}")
    print(f"{'-'*40}")

def check_python_version():
    print_section("Python Environment")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
    
    # Check Python version compatibility
    major, minor = sys.version_info[:2]
    if major == 3 and minor >= 8:
        print("✅ Python version is compatible")
    else:
        print("❌ Python version may not be compatible (requires 3.8+)")
        print("   Consider upgrading Python")

def check_files():
    print_section("Repository Files")
    required_files = [
        "app.py",
        "requirements.txt", 
        "README.md",
        "SETUP.md",
        "config.py",
        "core/red_code.py",
        "core/reflector.py"
    ]
    
    optional_files = [
        "deploy-euystacio.sh",
        "requirements-minimal.txt",
        "external/facial-detection"
    ]
    
    print("Required files:")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING!")
    
    print("\nOptional files:")
    for file_path in optional_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ⚠️  {file_path} - Not found (optional)")

def check_dependencies():
    print_section("Python Dependencies")
    
    core_packages = [
        ("flask", ">=3.0.0"),
        ("tensorflow", "==2.20.0"),
        ("numpy", ">=1.23.0"),
    ]
    
    optional_packages = [
        ("cv2", "opencv-python"),
        ("pandas", ">=0.24.2"),
    ]
    
    print("Core packages:")
    for package_name, version_req in core_packages:
        try:
            if package_name == "cv2":
                module = importlib.import_module("cv2")
            else:
                module = importlib.import_module(package_name)
            
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✅ {package_name} {version}")
        except ImportError:
            print(f"  ❌ {package_name} - NOT INSTALLED")
            if package_name == "tensorflow":
                print(f"     Install with: pip install tensorflow==2.20.0")
            else:
                print(f"     Install with: pip install {package_name}{version_req}")
    
    print("\nOptional packages:")
    for package_name, install_name in optional_packages:
        try:
            if package_name == "cv2":
                module = importlib.import_module("cv2")
                install_name = "opencv-python"
            else:
                module = importlib.import_module(package_name)
                install_name = package_name
            
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✅ {package_name} {version}")
        except ImportError:
            print(f"  ⚠️  {package_name} - Not installed (optional)")
            print(f"     Install with: pip install {install_name}")

def check_port():
    print_section("Network Configuration")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            print("⚠️  Port 5000 is currently in use")
            print("   The app may not start, or another instance is running")
            print("   Try: export PORT=8080 before running python app.py")
        else:
            print("✅ Port 5000 is available")
    except Exception as e:
        print(f"❓ Could not check port 5000: {e}")

def test_core_imports():
    print_section("Core Module Tests")
    
    test_imports = [
        "from config import config",
        "from core.red_code import RED_CODE", 
        "from sentimento_pulse_interface import SentimentoPulseInterface",
        "from tutor_nomination import TutorNomination"
    ]
    
    for test_import in test_imports:
        try:
            exec(test_import)
            module_name = test_import.split()[-1]
            print(f"  ✅ {module_name}")
        except ImportError as e:
            module_name = test_import.split()[-1]
            print(f"  ❌ {module_name} - {e}")
        except Exception as e:
            module_name = test_import.split()[-1]
            print(f"  ⚠️  {module_name} - {e}")

def provide_recommendations():
    print_section("Recommendations")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in a virtual environment (recommended)")
    else:
        print("⚠️  Not running in a virtual environment")
        print("   Consider creating one: python -m venv venv && source venv/bin/activate")
    
    # Check pip version
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pip_version = result.stdout.strip()
            print(f"✅ pip available: {pip_version}")
        else:
            print("❌ pip not available")
    except:
        print("❓ Could not check pip")

def main():
    print_header("Euystacio-Helmi AI Setup Diagnostics")
    print("This script will check your setup and provide troubleshooting information.")
    
    check_python_version()
    check_files() 
    check_dependencies()
    check_port()
    test_core_imports()
    provide_recommendations()
    
    print_section("Summary")
    print("If you see any ❌ errors above, please:")
    print("1. Check the troubleshooting section in README.md")
    print("2. Try the solutions suggested for each specific error")
    print("3. Consider using requirements-minimal.txt for a basic setup")
    print("4. Create a GitHub issue if problems persist")
    
    print(f"\nDiagnostics complete. Current directory: {os.getcwd()}")

if __name__ == "__main__":
    main()