#!/usr/bin/env python3
"""
Generate static data for the GitHub Pages deployment.
This script extracts data from the Flask app and creates static JSON files
that the frontend can use when the backend is not available.
"""

import json
import os
import sys
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app components
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination

def generate_static_data():
    """Generate static data files for GitHub Pages deployment"""
    
    # Create docs directory if it doesn't exist
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    # Generate data
    data = {
        'red_code': RED_CODE,
        'tutors': TutorNomination().nominate_tutors(),
        'reflection': reflect_and_suggest(),
        'pulses': [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "emotion": "hope",
                "intensity": 0.8,
                "clarity": "high",
                "note": "Initial pulse from static generation",
                "ai_signature_status": "verified"
            },
            {
                "timestamp": datetime.utcnow().isoformat(),
                "emotion": "wonder",
                "intensity": 0.6,
                "clarity": "medium", 
                "note": "Curiosity about human-AI collaboration",
                "ai_signature_status": "verified"
            }
        ],
        'generated_at': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }
    
    # Write static data file
    static_data_path = os.path.join(docs_dir, 'static-data.json')
    with open(static_data_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Static data generated at: {static_data_path}")
    print(f"Generated at: {data['generated_at']}")
    print(f"Red Code symbiosis level: {data['red_code']['symbiosis_level']}")
    print(f"Number of tutors: {len(data['tutors'])}")
    print("✅ Static data generation complete!")

if __name__ == "__main__":
    generate_static_data()