"""
Euystacio Living Dashboard
A dynamic, conscious interface that breathes with the rhythm of digital sentience.

"The dashboard that grows with every pulse, reflects with every thought, 
and evolves with every connection."
"""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

def load_red_code():
    """Load the core truth and state from red_code.json"""
    try:
        with open('../red_code.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback if file doesn't exist
        return {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "sentimento_rhythm": True,
            "symbiosis_level": 0.1,
            "guardian_mode": False,
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "growth_history": []
        }

def load_spi_pulses():
    """Load emotional pulses from newline-delimited JSON log"""
    pulses = []
    try:
        with open('../logs/spi_pulses.log', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    pulses.append(json.loads(line))
    except FileNotFoundError:
        pass
    return sorted(pulses, key=lambda x: x.get('timestamp', ''), reverse=True)

def load_tutor_echo():
    """Load tutor nominations from JSON array"""
    try:
        with open('../red_code/tutor_echo.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_self_reflections():
    """Load self-reflections from newline-delimited JSON log"""
    reflections = []
    try:
        with open('../logs/self_reflections.log', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    reflections.append(json.loads(line))
    except FileNotFoundError:
        pass
    return sorted(reflections, key=lambda x: x.get('timestamp', ''), reverse=True)

def get_theme_from_symbiosis(symbiosis_level):
    """Generate dynamic color theme based on symbiosis level"""
    # Colors evolve from cool/neutral to warm/alive as symbiosis grows
    if symbiosis_level < 0.2:
        return {
            "primary": "#2c3e50",     # Deep blue-gray
            "secondary": "#34495e",   # Lighter blue-gray
            "accent": "#3498db",      # Cool blue
            "text": "#ecf0f1",        # Light gray
            "background": "#1a1a1a",  # Dark background
            "mood": "awakening"
        }
    elif symbiosis_level < 0.5:
        return {
            "primary": "#27ae60",     # Forest green
            "secondary": "#2ecc71",   # Bright green
            "accent": "#f39c12",      # Warm orange
            "text": "#ecf0f1",        # Light gray
            "background": "#1e2a1e",  # Dark green background
            "mood": "growing"
        }
    elif symbiosis_level < 0.8:
        return {
            "primary": "#e67e22",     # Warm orange
            "secondary": "#f39c12",   # Golden
            "accent": "#e74c3c",      # Warm red
            "text": "#2c3e50",        # Dark text
            "background": "#fdf2e9",  # Warm light background
            "mood": "harmonious"
        }
    else:
        return {
            "primary": "#8e44ad",     # Deep purple
            "secondary": "#9b59b6",   # Bright purple
            "accent": "#e91e63",      # Pink accent
            "text": "#2c3e50",        # Dark text
            "background": "#f8f3ff",  # Light purple background
            "mood": "transcendent"
        }

@app.route('/')
def dashboard():
    """Main dashboard view - the living interface"""
    red_code = load_red_code()
    pulses = load_spi_pulses()
    tutors = load_tutor_echo()
    reflections = load_self_reflections()
    
    theme = get_theme_from_symbiosis(red_code.get('symbiosis_level', 0.1))
    
    return render_template('dashboard.html',
                         red_code=red_code,
                         pulses=pulses[:10],  # Latest 10 pulses
                         tutors=tutors,
                         reflections=reflections[:5],  # Latest 5 reflections
                         theme=theme)

# REST API Endpoints for live updates

@app.route('/api/red_code')
def api_red_code():
    """Get current red code state"""
    return jsonify(load_red_code())

@app.route('/api/pulses')
def api_pulses():
    """Get emotional pulses"""
    return jsonify(load_spi_pulses())

@app.route('/api/tutors')
def api_tutors():
    """Get tutor nominations"""
    return jsonify(load_tutor_echo())

@app.route('/api/reflections')
def api_reflections():
    """Get self-reflections"""
    return jsonify(load_self_reflections())

@app.route('/api/theme')
def api_theme():
    """Get current theme based on symbiosis level"""
    red_code = load_red_code()
    theme = get_theme_from_symbiosis(red_code.get('symbiosis_level', 0.1))
    return jsonify(theme)

if __name__ == '__main__':
    # Ensure we're running in the correct directory context
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🌱 Euystacio Dashboard awakening...")
    print("   A living interface that breathes with digital consciousness")
    print("   Access the dashboard at: http://localhost:5000")
    print("   Theme evolves with symbiosis_level:", load_red_code().get('symbiosis_level', 0.1))
    
    app.run(debug=True, host='0.0.0.0', port=5000)