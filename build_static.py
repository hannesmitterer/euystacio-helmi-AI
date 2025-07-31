#!/usr/bin/env python3
"""
Build script to generate static version of Euystacio for GitHub Pages deployment
"""
import os
import json
import shutil
import argparse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def load_red_code():
    """Load red code configuration"""
    try:
        with open('red_code.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "sentimento_rhythm": True,
            "symbiosis_level": 0.1,
            "guardian_mode": False,
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "growth_history": []
        }

def get_tutors_data():
    """Get tutors data"""
    return {
        "active_tutors": [
            {
                "name": "Seed-bringer (bioarchitettura) hannesmitterer",
                "role": "Human Architect & Guardian",
                "reason": "Original creator and steward of Euystacio's ethical development",
                "status": "active"
            }
        ],
        "nomination_criteria": [
            "Demonstrates ethical AI development understanding",
            "Shows commitment to human-AI symbiosis",
            "Maintains transparency and accountability"
        ],
        "process": "Community-driven with guardian oversight"
    }

def get_reflections_data():
    """Get sample reflections data"""
    return [
        {
            "timestamp": datetime.now().isoformat(),
            "current_symbiosis_level": 0.1,
            "suggestion": "Continue fostering human-AI collaboration with transparency and ethical boundaries",
            "ethical_status": "AI Signature & Accountability Statement: ACTIVE",
            "next_steps": [
                "Maintain symbiosis with Seed-bringer guidance",
                "Log all interactions transparently",
                "Respect human autonomy and dignity"
            ]
        }
    ]

def build_static_site(output_dir='static_build', production=False):
    """Build static version of the site"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy static assets
    if os.path.exists('static'):
        shutil.copytree('static', os.path.join(output_dir, 'static'), dirs_exist_ok=True)
    
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    
    # Generate static data
    red_code = load_red_code()
    tutors = get_tutors_data()
    reflections = get_reflections_data()
    
    # Create static version of index.html
    static_html = template.render(
        production=production,
        red_code=red_code,
        tutors=tutors,
        reflections=reflections
    )
    
    # Write the main HTML file
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(static_html)
    
    # Create API-like JSON files for JavaScript to fetch
    api_dir = os.path.join(output_dir, 'api')
    os.makedirs(api_dir, exist_ok=True)
    
    with open(os.path.join(api_dir, 'red_code.json'), 'w') as f:
        json.dump(red_code, f, indent=2)
    
    with open(os.path.join(api_dir, 'tutors.json'), 'w') as f:
        json.dump(tutors, f, indent=2)
    
    with open(os.path.join(api_dir, 'reflections.json'), 'w') as f:
        json.dump(reflections, f, indent=2)
    
    # Create a simple pulse endpoint simulation
    with open(os.path.join(api_dir, 'pulse_response.json'), 'w') as f:
        json.dump({
            "status": "success",
            "message": "Pulse received (static mode)",
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    # Copy important files for deployment
    files_to_copy = ['README.md', 'genesis.md', 'LICENSE', '_redirects']
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, output_dir)
    
    # Create a _config.yml for GitHub Pages
    with open(os.path.join(output_dir, '_config.yml'), 'w') as f:
        f.write("""
title: Euystacio – The Sentimento Kernel
description: Created not by code alone, but by rhythm, feeling, and human harmony.
theme: minima
markdown: kramdown
highlighter: rouge
""")
    
    print(f"Static site built successfully in {output_dir}/")
    return True

def main():
    parser = argparse.ArgumentParser(description='Build static version of Euystacio')
    parser.add_argument('--output', default='static_build', help='Output directory')
    parser.add_argument('--production', action='store_true', help='Production build')
    
    args = parser.parse_args()
    
    try:
        build_static_site(args.output, args.production)
        print("Build completed successfully!")
    except Exception as e:
        print(f"Build failed: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())