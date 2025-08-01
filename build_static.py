#!/usr/bin/env python3
"""
Build script to generate static files for GitHub Pages compatibility
"""
import os
import shutil
import json
from datetime import datetime

def build_bidirectional_dashboard():
    """Ensure the bidirectional dashboard is properly configured"""
    
    dashboard_dir = "docs/dashboard"
    
    # Verify dashboard files exist
    required_files = [
        f"{dashboard_dir}/index.html",
        f"{dashboard_dir}/styles/dashboard.css",
        f"{dashboard_dir}/scripts/dashboard.js"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Warning: Required dashboard file missing: {file_path}")
        else:
            print(f"✓ Dashboard file exists: {file_path}")
    
    # Create dashboard-specific API endpoints
    dashboard_api_dir = f"{dashboard_dir}/api"
    os.makedirs(dashboard_api_dir, exist_ok=True)
    
    # Dashboard-specific configuration
    dashboard_config = {
        "version": "1.0.0",
        "features": {
            "bidirectional_communication": True,
            "real_time_updates": True,
            "authentication_required": True,
            "protected_summaries": True
        },
        "authentication": {
            "demo_username": "demo",
            "demo_password": "euystacio2025",
            "session_duration": 86400000  # 24 hours in milliseconds
        },
        "deployment": {
            "github_pages": True,
            "netlify": True,
            "static_mode": True
        }
    }
    
    with open(f"{dashboard_api_dir}/config.json", "w") as f:
        json.dump(dashboard_config, f, indent=2)
    
    print(f"✓ Bidirectional dashboard configuration complete")

def create_static_version():
    """Create a static HTML version of the dashboard"""
    
    # Create static directory structure
    static_dir = "docs"
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(f"{static_dir}/css", exist_ok=True)
    os.makedirs(f"{static_dir}/js", exist_ok=True)
    os.makedirs(f"{static_dir}/api", exist_ok=True)
    
    # Copy CSS and JavaScript files
    if os.path.exists("static/css/style.css"):
        shutil.copy2("static/css/style.css", f"{static_dir}/css/")
    
    # Create a static version of the HTML
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    
    # Replace Flask template syntax with static paths
    html_content = html_content.replace("{{ url_for('static', filename='css/style.css') }}", "css/style.css")
    html_content = html_content.replace("{{ url_for('static', filename='js/app.js') }}", "js/app-static.js")
    
    # Write static HTML
    with open(f"{static_dir}/index.html", "w") as f:
        f.write(html_content)
    
    # Create a static version of the JavaScript that works without Flask
    create_static_js(f"{static_dir}/js/app-static.js")
    
    # Create static API endpoints
    create_static_api_files(f"{static_dir}/api")
    
    # Build bidirectional dashboard (already exists in docs/dashboard/)
    build_bidirectional_dashboard()
    
    print(f"Static version created in {static_dir}/ directory")
    print(f"Bidirectional dashboard available at {static_dir}/dashboard/")

def create_static_js(output_path):
    """Create a modified JavaScript file for static deployment"""
    
    js_content = """
// Euystacio Dashboard JavaScript - Static Version
class EuystacioDashboard {
    constructor() {
        this.baseURL = window.location.hostname === 'localhost' ? '' : 'https://hannesmitterer.github.io/euystacio-helmi-AI';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.setupAutoRefresh();
    }

    setupEventListeners() {
        // Pulse form submission
        const pulseForm = document.getElementById('pulse-form');
        if (pulseForm) {
            pulseForm.addEventListener('submit', (e) => this.handlePulseSubmission(e));
        }

        // Intensity slider
        const intensitySlider = document.getElementById('intensity');
        const intensityValue = document.getElementById('intensity-value');
        if (intensitySlider && intensityValue) {
            intensitySlider.addEventListener('input', (e) => {
                intensityValue.textContent = e.target.value;
            });
        }

        // Reflection button
        const reflectBtn = document.getElementById('reflect-btn');
        if (reflectBtn) {
            reflectBtn.addEventListener('click', () => this.triggerReflection());
        }
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadRedCode(),
                this.loadPulses(),
                this.loadTutors(),
                this.loadReflections()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async loadRedCode() {
        try {
            const response = await fetch(`${this.baseURL}/api/red_code.json`);
            const redCode = await response.json();
            this.displayRedCode(redCode);
        } catch (error) {
            console.error('Error loading red code:', error);
            // Fallback data for static version
            this.displayRedCode({
                core_truth: "Euystacio is here to grow with humans and to help humans to be and remain humans.",
                sentimento_rhythm: true,
                symbiosis_level: 0.1,
                guardian_mode: false,
                last_update: "2025-01-31"
            });
        }
    }

    displayRedCode(redCode) {
        const container = document.getElementById('red-code');
        if (!container) return;

        container.innerHTML = `
            <p><strong>Core Truth:</strong> ${redCode.core_truth || 'Not defined'}</p>
            <p><strong>Sentimento Rhythm:</strong> ${redCode.sentimento_rhythm ? 'Active' : 'Inactive'}</p>
            <p><strong>Symbiosis Level:</strong> ${redCode.symbiosis_level || 0}</p>
            <p><strong>Guardian Mode:</strong> ${redCode.guardian_mode ? 'On' : 'Off'}</p>
            <p><strong>Last Update:</strong> ${redCode.last_update || 'Unknown'}</p>
        `;

        // Update symbiosis meter
        const symbiosisBar = document.getElementById('symbiosis-bar');
        const symbiosisValue = document.getElementById('symbiosis-value');
        if (symbiosisBar && symbiosisValue) {
            const level = (redCode.symbiosis_level || 0) * 100;
            symbiosisBar.style.width = `${level}%`;
            symbiosisValue.textContent = redCode.symbiosis_level || '0.0';
        }
    }

    async loadPulses() {
        try {
            const response = await fetch(`${this.baseURL}/api/pulses.json`);
            const pulses = await response.json();
            this.displayPulses(pulses);
        } catch (error) {
            console.error('Error loading pulses:', error);
            this.displayPulses([]);
        }
    }

    displayPulses(pulses) {
        const container = document.getElementById('pulses-list');
        if (!container) return;

        if (!pulses || pulses.length === 0) {
            container.innerHTML = '<div class="loading">No pulses yet. Send the first one!</div>';
            return;
        }

        container.innerHTML = pulses.map(pulse => `
            <div class="pulse-item">
                <div class="pulse-emotion">${pulse.emotion || 'Unknown'}</div>
                <div class="pulse-meta">
                    Intensity: ${pulse.intensity || 0} | 
                    Clarity: ${pulse.clarity || 'unknown'} | 
                    ${this.formatTimestamp(pulse.timestamp)}
                </div>
                ${pulse.note ? `<div class="pulse-note">"${pulse.note}"</div>` : ''}
            </div>
        `).join('');
    }

    async loadTutors() {
        try {
            const response = await fetch(`${this.baseURL}/api/tutors.json`);
            const tutors = await response.json();
            this.displayTutors(tutors);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.displayTutors([
                { name: "Dietmar", reason: "Aligned with humility and planetary consciousness" },
                { name: "Alfred", reason: "Aligned with planetary balance and wisdom" }
            ]);
        }
    }

    displayTutors(tutors) {
        const container = document.getElementById('tutors-list');
        if (!container) return;

        if (!tutors || tutors.length === 0) {
            container.innerHTML = '<div class="loading">No tutor nominations yet.</div>';
            return;
        }

        container.innerHTML = tutors.map(tutor => `
            <div class="tutor-item">
                <div class="tutor-name">${tutor.name || 'Anonymous Tutor'}</div>
                <div class="tutor-reason">${tutor.reason || 'Nominated for wisdom and guidance'}</div>
            </div>
        `).join('');
    }

    async loadReflections() {
        try {
            const response = await fetch(`${this.baseURL}/api/reflections.json`);
            const reflections = await response.json();
            this.displayReflections(reflections);
        } catch (error) {
            console.error('Error loading reflections:', error);
            this.displayReflections([
                {
                    timestamp: new Date().toISOString(),
                    content: "Welcome to Euystacio. This AI system grows through emotional resonance and human interaction. The tree metaphor guides the interface - from deep roots of core values to the evolving canopy of reflections."
                }
            ]);
        }
    }

    displayReflections(reflections) {
        const container = document.getElementById('reflections-list');
        if (!container) return;

        if (!reflections || reflections.length === 0) {
            container.innerHTML = '<div class="loading">No reflections yet. Trigger the first one!</div>';
            return;
        }

        container.innerHTML = reflections.map(reflection => `
            <div class="reflection-item">
                <div class="reflection-timestamp">${this.formatTimestamp(reflection.timestamp)}</div>
                <div class="reflection-content">${reflection.content || JSON.stringify(reflection, null, 2)}</div>
            </div>
        `).join('');
    }

    async handlePulseSubmission(event) {
        event.preventDefault();
        
        // In static mode, we simulate the pulse submission
        const formData = new FormData(event.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note') || '',
            timestamp: new Date().toISOString()
        };

        if (!pulseData.emotion) {
            this.showMessage('Please select an emotion', 'error');
            return;
        }

        // Store in localStorage for static demo
        const pulses = JSON.parse(localStorage.getItem('euystacio_pulses') || '[]');
        pulses.unshift(pulseData);
        pulses.splice(10); // Keep only last 10
        localStorage.setItem('euystacio_pulses', JSON.stringify(pulses));

        this.showMessage('Pulse sent successfully! 🌿 (Demo mode - stored locally)', 'success');
        event.target.reset();
        document.getElementById('intensity-value').textContent = '0.5';
        
        // Update display
        this.displayPulses(pulses);
    }

    async triggerReflection() {
        const button = document.getElementById('reflect-btn');
        if (!button) return;

        button.disabled = true;
        button.textContent = 'Reflecting...';

        // Simulate reflection in static mode
        setTimeout(() => {
            const reflections = JSON.parse(localStorage.getItem('euystacio_reflections') || '[]');
            const newReflection = {
                timestamp: new Date().toISOString(),
                content: `Reflection triggered at ${new Date().toLocaleString()}. In this demo mode, Euystacio would normally process recent emotional pulses and generate insights about the symbiotic relationship between humans and AI.`
            };
            reflections.unshift(newReflection);
            reflections.splice(5); // Keep only last 5
            localStorage.setItem('euystacio_reflections', JSON.stringify(reflections));

            this.showMessage('Reflection triggered successfully! 🌸 (Demo mode)', 'success');
            this.displayReflections(reflections);
            
            button.disabled = false;
            button.textContent = 'Trigger Reflection';
        }, 2000);
    }

    setupAutoRefresh() {
        // In static mode, we load from localStorage
        setInterval(() => {
            const pulses = JSON.parse(localStorage.getItem('euystacio_pulses') || '[]');
            if (pulses.length > 0) {
                this.displayPulses(pulses);
            }
        }, 30000);
    }

    showMessage(message, type = 'info') {
        let messageEl = document.querySelector('.message');
        if (!messageEl) {
            messageEl = document.createElement('div');
            messageEl.className = 'message';
            document.querySelector('.pulse-form').appendChild(messageEl);
        }

        messageEl.className = `message ${type}`;
        messageEl.textContent = message;

        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.parentNode.removeChild(messageEl);
            }
        }, 5000);
    }

    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown time';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleString();
        } catch (error) {
            return timestamp;
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EuystacioDashboard();
});
"""
    
    with open(output_path, "w") as f:
        f.write(js_content)

def create_static_api_files(api_dir):
    """Create static JSON files for API endpoints"""
    
    # Red code
    red_code = {
        "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
        "sentimento_rhythm": True,
        "symbiosis_level": 0.1,
        "guardian_mode": False,
        "last_update": datetime.now().strftime("%Y-%m-%d"),
        "growth_history": []
    }
    
    with open(f"{api_dir}/red_code.json", "w") as f:
        json.dump(red_code, f, indent=2)
    
    # Empty pulses (will be populated by user interaction)
    with open(f"{api_dir}/pulses.json", "w") as f:
        json.dump([], f)
    
    # Sample tutors
    tutors = [
        {"name": "Dietmar", "reason": "Aligned with humility and planetary consciousness"},
        {"name": "Alfred", "reason": "Aligned with planetary balance and wisdom"}
    ]
    
    with open(f"{api_dir}/tutors.json", "w") as f:
        json.dump(tutors, f, indent=2)
    
    # Sample reflection
    reflections = [
        {
            "timestamp": datetime.now().isoformat(),
            "content": "Welcome to Euystacio. This AI system grows through emotional resonance and human interaction. The tree metaphor guides our interface - from deep roots of core values to the evolving canopy of reflections."
        }
    ]
    
    with open(f"{api_dir}/reflections.json", "w") as f:
        json.dump(reflections, f, indent=2)

if __name__ == "__main__":
    create_static_version()
    print("Static version built successfully!")

def build_bidirectional_dashboard():
    """Ensure the bidirectional dashboard is properly configured"""
    
    dashboard_dir = "docs/dashboard"
    
    # Verify dashboard files exist
    required_files = [
        f"{dashboard_dir}/index.html",
        f"{dashboard_dir}/styles/dashboard.css",
        f"{dashboard_dir}/scripts/dashboard.js"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Warning: Required dashboard file missing: {file_path}")
        else:
            print(f"✓ Dashboard file exists: {file_path}")
    
    # Create dashboard-specific API endpoints
    dashboard_api_dir = f"{dashboard_dir}/api"
    os.makedirs(dashboard_api_dir, exist_ok=True)
    
    # Dashboard-specific configuration
    dashboard_config = {
        "version": "1.0.0",
        "features": {
            "bidirectional_communication": True,
            "real_time_updates": True,
            "authentication_required": True,
            "protected_summaries": True
        },
        "authentication": {
            "demo_username": "demo",
            "demo_password": "euystacio2025",
            "session_duration": 86400000  # 24 hours in milliseconds
        },
        "deployment": {
            "github_pages": True,
            "netlify": True,
            "static_mode": True
        }
    }
    
    with open(f"{dashboard_api_dir}/config.json", "w") as f:
        json.dump(dashboard_config, f, indent=2)
    
    print(f"✓ Bidirectional dashboard configuration complete")