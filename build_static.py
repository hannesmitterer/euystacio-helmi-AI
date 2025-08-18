#!/usr/bin/env python3
"""
Static build script for Euystacio Dashboard
Prepares static version for GitHub Pages deployment
"""

import os
import shutil
import json
from pathlib import Path

def create_static_version():
    """
    Create static version by copying and processing files for GitHub Pages.
    This ensures the docs/ directory contains everything needed for deployment.
    """
    print("🌳 Building static version of Euystacio Dashboard...")
    
    # Ensure docs directory exists
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Copy static assets if they don't exist or are outdated
    static_source = Path("static")
    if static_source.exists():
        for asset_type in ["css", "js"]:
            source_dir = static_source / asset_type
            target_dir = docs_dir / asset_type
            if source_dir.exists():
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.copytree(source_dir, target_dir)
                print(f"  ✓ Copied {asset_type} assets")
    
    # Ensure red_code.json exists for the dashboard
    red_code_file = Path("red_code.json")
    docs_red_code = docs_dir / "red_code.json"
    if red_code_file.exists():
        shutil.copy2(red_code_file, docs_red_code)
        print("  ✓ Copied red_code.json")
    else:
        # Create a minimal red_code.json if it doesn't exist
        minimal_red_code = {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "sentimento_rhythm": "Active",
            "symbiosis_level": 0.1,
            "guardian_mode": "Off",
            "last_update": "2025-08-01",
            "recent_pulses": [],
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
        }
        with open(docs_red_code, 'w') as f:
            json.dump(minimal_red_code, f, indent=2)
        print("  ✓ Created minimal red_code.json")
    
    # Create logs directory in docs if it doesn't exist
    logs_dir = docs_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Copy any existing log files
    source_logs = Path("logs")
    if source_logs.exists():
        for log_file in source_logs.glob("*.json"):
            shutil.copy2(log_file, logs_dir / log_file.name)
        print("  ✓ Copied log files")
    
    print("🌲 Static build completed successfully!")
    return True

def build_bidirectional_dashboard():
    """
    Build function that can be called from GitHub Actions.
    Currently delegates to static version creation.
    """
    print("🌿 Building bidirectional dashboard...")
    success = create_static_version()
    if success:
        print("🌸 Bidirectional dashboard build completed!")
    else:
        print("❌ Build failed!")
        exit(1)

if __name__ == "__main__":
    build_bidirectional_dashboard()
