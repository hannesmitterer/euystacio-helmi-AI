#!/usr/bin/env python3
"""
Lex Amoris Validation Script
Sempre in Costante - Always in Constant Resonance

This script validates the Lex Amoris PWA files:
- lexamoris.html
- manifest.json
- service-worker.js

Version: 1.0.0
"""

import json
import os
import sys
import re
from pathlib import Path

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """Print an error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """Print an info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def validate_html_file(filepath):
    """Validate lexamoris.html"""
    print_header("Validating lexamoris.html")
    
    if not os.path.exists(filepath):
        print_error(f"File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: File size
    tests_total += 1
    file_size = len(content)
    if file_size > 0:
        print_success(f"File exists and has content ({file_size} bytes)")
        tests_passed += 1
    else:
        print_error("File is empty")
    
    # Test 2: HTML structure
    tests_total += 1
    if '<!DOCTYPE html>' in content and '<html' in content and '</html>' in content:
        print_success("Valid HTML document structure")
        tests_passed += 1
    else:
        print_error("Invalid HTML structure")
    
    # Test 3: Manifest link
    tests_total += 1
    if '<link rel="manifest" href="/manifest.json">' in content or \
       '<link rel="manifest" href="manifest.json">' in content:
        print_success("Manifest link present")
        tests_passed += 1
    else:
        print_error("Manifest link missing")
    
    # Test 4: Branding - "Sempre in Costante"
    tests_total += 1
    if 'Sempre in Costante' in content:
        count = content.count('Sempre in Costante')
        print_success(f"Branding 'Sempre in Costante' present ({count} occurrences)")
        tests_passed += 1
    else:
        print_error("Branding 'Sempre in Costante' missing")
    
    # Test 5: Lex Amoris title
    tests_total += 1
    if 'Lex Amoris' in content:
        count = content.count('Lex Amoris')
        print_success(f"'Lex Amoris' present ({count} occurrences)")
        tests_passed += 1
    else:
        print_error("'Lex Amoris' missing")
    
    # Test 6: Resonance pulse animation
    tests_total += 1
    if '@keyframes resonance-pulse' in content:
        print_success("Resonance pulse animation defined")
        tests_passed += 1
    else:
        print_error("Resonance pulse animation missing")
    
    # Test 7: Exponential growth function
    tests_total += 1
    if 'calculateExponentialGrowth' in content:
        print_success("Exponential growth function present")
        tests_passed += 1
    else:
        print_error("Exponential growth function missing")
    
    # Test 8: Red Shield security
    tests_total += 1
    if 'initializeRedShield' in content or 'Red Shield' in content:
        print_success("Red Shield security system present")
        tests_passed += 1
    else:
        print_error("Red Shield security system missing")
    
    # Test 9: Service Worker registration
    tests_total += 1
    if 'service-worker' in content.lower() and 'serviceWorker.register' in content:
        print_success("Service Worker registration code present")
        tests_passed += 1
    else:
        print_warning("Service Worker registration code not found")
    
    # Test 10: Responsive design
    tests_total += 1
    if 'viewport' in content and 'width=device-width' in content:
        print_success("Responsive viewport meta tag present")
        tests_passed += 1
    else:
        print_error("Responsive viewport meta tag missing")
    
    # Test 11: Accessibility
    tests_total += 1
    if 'prefers-reduced-motion' in content:
        print_success("Reduced motion accessibility support present")
        tests_passed += 1
    else:
        print_warning("Reduced motion support not found")
    
    # Summary
    print(f"\n{Colors.BOLD}HTML Validation: {tests_passed}/{tests_total} tests passed{Colors.END}")
    return tests_passed == tests_total

def validate_manifest_file(filepath):
    """Validate manifest.json"""
    print_header("Validating manifest.json")
    
    if not os.path.exists(filepath):
        print_error(f"File not found: {filepath}")
        return False
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Valid JSON
    tests_total += 1
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        print_success("Valid JSON syntax")
        tests_passed += 1
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON: {e}")
        return False
    
    # Test 2: Required PWA fields
    required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
    for field in required_fields:
        tests_total += 1
        if field in manifest:
            print_success(f"Required field '{field}' present")
            tests_passed += 1
        else:
            print_error(f"Required field '{field}' missing")
    
    # Test 3: Name contains branding
    tests_total += 1
    if 'name' in manifest and 'Sempre in Costante' in manifest['name']:
        print_success(f"Name contains branding: {manifest['name']}")
        tests_passed += 1
    else:
        print_error("Name doesn't contain 'Sempre in Costante'")
    
    # Test 4: Theme color
    tests_total += 1
    if 'theme_color' in manifest:
        print_success(f"Theme color: {manifest['theme_color']}")
        tests_passed += 1
    else:
        print_warning("Theme color not specified")
    
    # Test 5: Background color
    tests_total += 1
    if 'background_color' in manifest:
        print_success(f"Background color: {manifest['background_color']}")
        tests_passed += 1
    else:
        print_warning("Background color not specified")
    
    # Test 6: Icons array
    tests_total += 1
    if 'icons' in manifest and len(manifest['icons']) > 0:
        icon_count = len(manifest['icons'])
        print_success(f"Icons array has {icon_count} icons")
        tests_passed += 1
        
        # Check for required sizes
        sizes = [icon.get('sizes', '') for icon in manifest['icons']]
        has_192 = any('192' in s for s in sizes)
        has_512 = any('512' in s for s in sizes)
        
        if has_192 and has_512:
            print_success("Has recommended icon sizes (192x192 and 512x512)")
        else:
            print_warning("Missing recommended icon sizes (192x192 or 512x512)")
    else:
        print_error("Icons array is empty or missing")
    
    # Test 7: Shortcuts
    tests_total += 1
    if 'shortcuts' in manifest and len(manifest['shortcuts']) > 0:
        shortcut_count = len(manifest['shortcuts'])
        print_success(f"Shortcuts defined ({shortcut_count} shortcuts)")
        tests_passed += 1
        
        for i, shortcut in enumerate(manifest['shortcuts'], 1):
            if 'name' in shortcut and 'url' in shortcut:
                print_info(f"  Shortcut {i}: {shortcut['name']}")
            else:
                print_warning(f"  Shortcut {i} missing name or url")
    else:
        print_warning("No shortcuts defined")
    
    # Test 8: Start URL
    tests_total += 1
    if 'start_url' in manifest:
        if 'lexamoris' in manifest['start_url'].lower():
            print_success(f"Start URL points to Lex Amoris: {manifest['start_url']}")
            tests_passed += 1
        else:
            print_error(f"Start URL doesn't point to Lex Amoris: {manifest['start_url']}")
    else:
        print_error("Start URL missing")
    
    # Test 9: Display mode
    tests_total += 1
    if 'display' in manifest:
        if manifest['display'] == 'standalone':
            print_success("Display mode is standalone (recommended)")
            tests_passed += 1
        else:
            print_info(f"Display mode is '{manifest['display']}'")
            tests_passed += 1
    else:
        print_warning("Display mode not specified")
    
    # Test 10: Scope
    tests_total += 1
    if 'scope' in manifest:
        print_success(f"Scope defined: {manifest['scope']}")
        tests_passed += 1
    else:
        print_warning("Scope not defined (will default to start_url directory)")
    
    # Summary
    print(f"\n{Colors.BOLD}Manifest Validation: {tests_passed}/{tests_total} tests passed{Colors.END}")
    return tests_passed >= tests_total - 2  # Allow for warnings

def validate_service_worker(filepath):
    """Validate service-worker.js"""
    print_header("Validating service-worker.js")
    
    if not os.path.exists(filepath):
        print_warning(f"File not found: {filepath} (optional)")
        return True  # Service worker is optional
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: File size
    tests_total += 1
    file_size = len(content)
    if file_size > 0:
        print_success(f"File exists and has content ({file_size} bytes)")
        tests_passed += 1
    else:
        print_error("File is empty")
    
    # Test 2: Install event
    tests_total += 1
    if "addEventListener('install'" in content or 'addEventListener("install"' in content:
        print_success("Install event listener present")
        tests_passed += 1
    else:
        print_error("Install event listener missing")
    
    # Test 3: Activate event
    tests_total += 1
    if "addEventListener('activate'" in content or 'addEventListener("activate"' in content:
        print_success("Activate event listener present")
        tests_passed += 1
    else:
        print_error("Activate event listener missing")
    
    # Test 4: Fetch event
    tests_total += 1
    if "addEventListener('fetch'" in content or 'addEventListener("fetch"' in content:
        print_success("Fetch event listener present")
        tests_passed += 1
    else:
        print_error("Fetch event listener missing")
    
    # Test 5: Cache name
    tests_total += 1
    if 'CACHE_NAME' in content or 'cacheName' in content:
        print_success("Cache name defined")
        tests_passed += 1
    else:
        print_warning("Cache name not found")
    
    # Test 6: Lex Amoris references
    tests_total += 1
    if 'lex-amoris' in content.lower() or 'lexamoris' in content.lower():
        print_success("Lex Amoris references present")
        tests_passed += 1
    else:
        print_warning("Lex Amoris references not found")
    
    # Summary
    print(f"\n{Colors.BOLD}Service Worker Validation: {tests_passed}/{tests_total} tests passed{Colors.END}")
    return tests_passed >= tests_total - 1  # Allow for one warning

def run_all_validations():
    """Run all validation tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║            Lex Amoris - PWA Validation Suite v1.0.0              ║")
    print("║                  Sempre in Costante                               ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # File paths
    html_file = current_dir / 'lexamoris.html'
    manifest_file = current_dir / 'manifest.json'
    sw_file = current_dir / 'service-worker.js'
    
    print_info(f"Validation directory: {current_dir}")
    print_info(f"Files to validate:")
    print(f"  - {html_file}")
    print(f"  - {manifest_file}")
    print(f"  - {sw_file}")
    
    # Run validations
    results = []
    
    html_valid = validate_html_file(html_file)
    results.append(('lexamoris.html', html_valid))
    
    manifest_valid = validate_manifest_file(manifest_file)
    results.append(('manifest.json', manifest_valid))
    
    sw_valid = validate_service_worker(sw_file)
    results.append(('service-worker.js', sw_valid))
    
    # Final summary
    print_header("Validation Summary")
    
    all_passed = all(result[1] for result in results)
    
    for filename, passed in results:
        if passed:
            print_success(f"{filename}: PASSED")
        else:
            print_error(f"{filename}: FAILED")
    
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    if all_passed:
        print(f"{Colors.BOLD}{Colors.GREEN}")
        print("✅ ALL VALIDATIONS PASSED!")
        print("Lex Amoris PWA is ready for deployment.")
        print(f"Sempre in Costante - Always in Constant Resonance{Colors.END}")
        return 0
    else:
        print(f"{Colors.BOLD}{Colors.RED}")
        print("❌ SOME VALIDATIONS FAILED")
        print("Please review the errors above and fix the issues.")
        print(f"{Colors.END}")
        return 1

if __name__ == '__main__':
    exit_code = run_all_validations()
    sys.exit(exit_code)
