import os
import json
import shutil
from datetime import datetime

def create_static_version():
    """
    Creates a static version of the bidirectional dashboard with current data.
    This function generates static HTML files with embedded data from the current system state.
    """
    print("Creating static version of the dashboard...")
    
    # Ensure target directory exists
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    # Copy static assets (CSS, JS) if they exist
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if os.path.exists(static_dir):
        # Copy CSS
        css_src = os.path.join(static_dir, 'css')
        css_dst = os.path.join(docs_dir, 'css')
        if os.path.exists(css_src):
            if os.path.exists(css_dst):
                shutil.rmtree(css_dst)
            shutil.copytree(css_src, css_dst)
        
        # Create modified JS for static version
        js_src = os.path.join(static_dir, 'js')
        js_dst = os.path.join(docs_dir, 'js')
        if os.path.exists(js_src):
            os.makedirs(js_dst, exist_ok=True)
            # Create static version of JS that uses embedded data
            js_file = os.path.join(js_src, 'app.js')
            if os.path.exists(js_file):
                with open(js_file, 'r') as f:
                    js_content = f.read()
                
                # Modify JS to use embedded data instead of API calls
                static_js_content = create_static_js(js_content)
                
                # Save as app-static.js
                with open(os.path.join(js_dst, 'app-static.js'), 'w') as f:
                    f.write(static_js_content)
    
    # Load current data
    current_data = get_current_data()
    
    # Generate static HTML with embedded data
    generate_static_html(docs_dir, current_data)
    
    print(f"Static version created in {docs_dir}")

def get_current_data():
    """
    Collects current data from the system for static generation.
    """
    # Import here to avoid circular imports
    try:
        from core.red_code import RED_CODE
        red_code = RED_CODE
    except ImportError:
        red_code = {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "sentimento_rhythm": True,
            "symbiosis_level": 0.1,
            "guardian_mode": False,
            "last_update": datetime.now().strftime("%Y-%m-%d")
        }
    
    # Get pulses
    pulses = []
    try:
        # Load from red_code.json if it exists
        red_code_file = os.path.join(os.path.dirname(__file__), 'red_code.json')
        if os.path.exists(red_code_file):
            with open(red_code_file, 'r') as f:
                data = json.load(f)
                pulses.extend(data.get("recent_pulses", []))
        
        # Load from logs directory if it exists
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if os.path.exists(logs_dir):
            for fname in sorted(os.listdir(logs_dir)):
                if fname.startswith("log_") and fname.endswith(".json"):
                    with open(os.path.join(logs_dir, fname)) as f:
                        log = json.load(f)
                        for k, v in log.items():
                            if isinstance(v, dict) and "emotion" in v:
                                pulses.append(v)
    except Exception as e:
        print(f"Warning: Could not load pulses: {e}")
    
    # Get reflections
    reflections = []
    try:
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if os.path.exists(logs_dir):
            for fname in sorted(os.listdir(logs_dir)):
                if "reflection" in fname:
                    with open(os.path.join(logs_dir, fname)) as f:
                        reflections.append(json.load(f))
    except Exception as e:
        print(f"Warning: Could not load reflections: {e}")
    
    # Get tutors (basic implementation)
    tutors = []
    try:
        from tutor_nomination import TutorNomination
        tutor_nom = TutorNomination()
        tutors = tutor_nom.list_tutors()
    except Exception as e:
        print(f"Warning: Could not load tutors: {e}")
        tutors = []  # Default empty list
    
    return {
        'red_code': red_code,
        'pulses': pulses,
        'reflections': reflections,
        'tutors': tutors,
        'generated_at': datetime.now().isoformat()
    }

def generate_static_html(docs_dir, data):
    """
    Generates the static HTML file with embedded data.
    """
    # Read the template
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    if not os.path.exists(template_path):
        print("Warning: Template not found, creating basic HTML")
        create_basic_html(docs_dir, data)
        return
    
    with open(template_path, 'r') as f:
        html_content = f.read()
    
    # Replace Flask template references with static paths
    html_content = html_content.replace("{{ url_for('static', filename='css/style.css') }}", "css/style.css")
    html_content = html_content.replace("{{ url_for('static', filename='js/app.js') }}", "js/app-static.js")
    
    # Add embedded data as JSON
    data_script = f"""
    <script>
        // Embedded data for static version
        window.EUYSTACIO_DATA = {json.dumps(data, indent=2)};
    </script>
    """
    
    # Insert the data script before the main app script
    if '<script src="js/app-static.js">' in html_content:
        html_content = html_content.replace('<script src="js/app-static.js">', data_script + '\n    <script src="js/app-static.js">')
    else:
        # Insert before closing body tag
        html_content = html_content.replace('</body>', f'    {data_script}\n</body>')
    
    # Write the static HTML
    output_path = os.path.join(docs_dir, 'index.html')
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f"Static HTML generated: {output_path}")

def create_static_js(original_js):
    """
    Creates a static version of the JavaScript that uses embedded data instead of API calls.
    """
    # Replace API calls with static data access
    static_js = original_js
    
    # Replace loadRedCode method
    static_js = static_js.replace(
        """async loadRedCode() {
        try {
            const response = await fetch('/api/red_code');
            const redCode = await response.json();
            this.displayRedCode(redCode);
        } catch (error) {
            console.error('Error loading red code:', error);
            this.showError('red-code', 'Failed to load red code');
        }
    }""",
        """async loadRedCode() {
        try {
            const redCode = window.EUYSTACIO_DATA ? window.EUYSTACIO_DATA.red_code : null;
            if (redCode) {
                this.displayRedCode(redCode);
            } else {
                this.showError('red-code', 'No data available in static version');
            }
        } catch (error) {
            console.error('Error loading red code:', error);
            this.showError('red-code', 'Failed to load red code');
        }
    }"""
    )
    
    # Replace loadPulses method
    static_js = static_js.replace(
        """async loadPulses() {
        try {
            const response = await fetch('/api/pulses');
            const pulses = await response.json();
            this.displayPulses(pulses);
        } catch (error) {
            console.error('Error loading pulses:', error);
            this.showError('pulses-list', 'Failed to load pulses');
        }
    }""",
        """async loadPulses() {
        try {
            const pulses = window.EUYSTACIO_DATA ? window.EUYSTACIO_DATA.pulses : [];
            this.displayPulses(pulses);
        } catch (error) {
            console.error('Error loading pulses:', error);
            this.showError('pulses-list', 'Failed to load pulses');
        }
    }"""
    )
    
    # Replace loadTutors method
    static_js = static_js.replace(
        """async loadTutors() {
        try {
            const response = await fetch('/api/tutors');
            const tutors = await response.json();
            this.displayTutors(tutors);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.showError('tutors-list', 'Failed to load tutor nominations');
        }
    }""",
        """async loadTutors() {
        try {
            const tutors = window.EUYSTACIO_DATA ? window.EUYSTACIO_DATA.tutors : [];
            this.displayTutors(tutors);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.showError('tutors-list', 'Failed to load tutor nominations');
        }
    }"""
    )
    
    # Replace loadReflections method
    static_js = static_js.replace(
        """async loadReflections() {
        try {
            const response = await fetch('/api/reflections');
            const reflections = await response.json();
            this.displayReflections(reflections);
        } catch (error) {
            console.error('Error loading reflections:', error);
            this.showError('reflections-list', 'Failed to load reflections');
        }
    }""",
        """async loadReflections() {
        try {
            const reflections = window.EUYSTACIO_DATA ? window.EUYSTACIO_DATA.reflections : [];
            this.displayReflections(reflections);
        } catch (error) {
            console.error('Error loading reflections:', error);
            this.showError('reflections-list', 'Failed to load reflections');
        }
    }"""
    )
    
    # Replace pulse submission with notice
    static_js = static_js.replace(
        """async handlePulseSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note') || ''
        };

        if (!pulseData.emotion) {
            this.showMessage('Please select an emotion', 'error');
            return;
        }

        try {
            const response = await fetch('/api/pulse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(pulseData)
            });

            if (response.ok) {
                const result = await response.json();
                this.showMessage('Pulse sent successfully! 🌿', 'success');
                event.target.reset();
                document.getElementById('intensity-value').textContent = '0.5';
                
                // Refresh pulses and red code
                setTimeout(() => {
                    this.loadPulses();
                    this.loadRedCode();
                }, 500);
            } else {
                throw new Error('Failed to send pulse');
            }
        } catch (error) {
            console.error('Error sending pulse:', error);
            this.showMessage('Failed to send pulse. Please try again.', 'error');
        }
    }""",
        """async handlePulseSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note') || ''
        };

        if (!pulseData.emotion) {
            this.showMessage('Please select an emotion', 'error');
            return;
        }

        // Static version - show message about interactive version
        this.showMessage('This is a static version. Visit the interactive site to send pulses! 🌳', 'info');
        event.target.reset();
        document.getElementById('intensity-value').textContent = '0.5';
    }"""
    )
    
    # Replace reflection trigger with notice
    static_js = static_js.replace(
        """async triggerReflection() {
        const button = document.getElementById('reflect-btn');
        if (!button) return;

        button.disabled = true;
        button.textContent = 'Reflecting...';

        try {
            const response = await fetch('/api/reflect');
            if (response.ok) {
                const reflection = await response.json();
                this.showMessage('Reflection triggered successfully! 🌸', 'success');
                
                // Refresh reflections and red code
                setTimeout(() => {
                    this.loadReflections();
                    this.loadRedCode();
                }, 1000);
            } else {
                throw new Error('Failed to trigger reflection');
            }
        } catch (error) {
            console.error('Error triggering reflection:', error);
            this.showMessage('Failed to trigger reflection. Please try again.', 'error');
        } finally {
            button.disabled = false;
            button.textContent = 'Trigger Reflection';
        }
    }""",
        """async triggerReflection() {
        const button = document.getElementById('reflect-btn');
        if (!button) return;

        // Static version - show message about interactive version
        this.showMessage('This is a static version. Visit the interactive site to trigger reflections! 🌸', 'info');
    }"""
    )
    
    # Add comment at the top to indicate this is the static version
    static_js = "// Euystacio Dashboard JavaScript - Static Version (Generated)\n" + static_js
    
    return static_js
    """
    Creates a basic HTML file if template is not available.
    """
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Euystacio - The Sentimento Kernel</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">🌳 Euystacio Dashboard (Static Version)</h1>
            <p class="subtitle">"Created not by code alone, but by rhythm, feeling, and human harmony."</p>
        </header>
        <main class="dashboard">
            <section class="red-code-section">
                <h2>🌱 The Red Code (Roots)</h2>
                <div class="red-code">
                    <p><strong>Core Truth:</strong> {data['red_code'].get('core_truth', 'Not defined')}</p>
                    <p><strong>Symbiosis Level:</strong> {data['red_code'].get('symbiosis_level', 0)}</p>
                    <p><strong>Last Update:</strong> {data['red_code'].get('last_update', 'Unknown')}</p>
                </div>
            </section>
        </main>
    </div>
    
    <script>
        window.EUYSTACIO_DATA = {json.dumps(data, indent=2)};
    </script>
    <script src="js/app-static.js"></script>
</body>
</html>"""
    
    output_path = os.path.join(docs_dir, 'index.html')
    with open(output_path, 'w') as f:
        f.write(html_content)

def build_bidirectional_dashboard():
    """
    Build bidirectional dashboard with current system data.
    This function creates a static version of the dashboard that includes current data
    and can display the bidirectional nature of the system (showing both incoming and outgoing data).
    """
    print("Building bidirectional dashboard...")
    create_static_version()
    print("Bidirectional dashboard build completed")
