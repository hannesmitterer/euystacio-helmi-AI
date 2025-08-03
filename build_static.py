import shutil
import os
import json
from core.red_code import RED_CODE

def create_static_version():
    """
    Create a static version of the site by:
    1. Converting Flask templates to static HTML
    2. Copying static assets to docs directory
    3. Generating static API JSON files
    """
    print("Creating static version...")
    
    # Ensure docs directory exists
    os.makedirs("docs", exist_ok=True)
    
    # Read template and convert to static HTML
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    # Replace Flask url_for calls with static paths
    html_content = html_content.replace('{{ url_for(\'static\', filename=\'css/style.css\') }}', 'css/style.css')
    html_content = html_content.replace('{{ url_for(\'static\', filename=\'js/app.js\') }}', 'js/app-static.js')
    
    # Add the dashboard link that was manually added to the current docs/index.html
    if '<body>' in html_content and 'dashboard-link' not in html_content:
        html_content = html_content.replace(
            '<body>',
            '<body>\n    <a href=\'https://github.com/hannesmitterer/euystacio-ai\' class=\'dashboard-link\'>Euystacio AI Dashboard</a>'
        )
    
    # Write to docs/index.html
    with open('docs/index.html', 'w') as f:
        f.write(html_content)
    
    # Copy static assets
    print("Copying static assets...")
    
    # Copy CSS files
    os.makedirs("docs/css", exist_ok=True)
    if os.path.exists("static/css"):
        for file in os.listdir("static/css"):
            shutil.copy2(f"static/css/{file}", f"docs/css/{file}")
    
    # Copy and adapt JS files
    os.makedirs("docs/js", exist_ok=True)
    if os.path.exists("static/js/app.js"):
        # Create static version of JS with proper base URL handling
        with open("static/js/app.js", 'r') as f:
            js_content = f.read()
        
        # Add static hosting compatibility
        static_js = js_content.replace(
            'class EuystacioDashboard {',
            '''// Euystacio Dashboard JavaScript - Static Version
class EuystacioDashboard {'''
        )
        
        # Add base URL handling for static sites
        static_js = static_js.replace(
            'constructor() {',
            '''constructor() {
        this.baseURL = window.location.hostname === 'localhost' ? '' : 'https://hannesmitterer.github.io/euystacio-helmi-AI';'''
        )
        
        with open("docs/js/app-static.js", 'w') as f:
            f.write(static_js)
    
    # Generate static API files
    print("Generating static API files...")
    os.makedirs("docs/api", exist_ok=True)
    
    # Red code JSON
    with open("docs/api/red_code.json", 'w') as f:
        json.dump(RED_CODE, f, indent=2)
    
    # Empty collections for static version
    with open("docs/api/pulses.json", 'w') as f:
        json.dump([], f, indent=2)
    
    with open("docs/api/reflections.json", 'w') as f:
        json.dump([], f, indent=2)
    
    with open("docs/api/tutors.json", 'w') as f:
        json.dump([], f, indent=2)
    
    print("Static version created successfully in docs/ directory")

def build_bidirectional_dashboard():
    """
    Stub function for bidirectional dashboard creation.
    This function serves as a placeholder for potential future bidirectional dashboard functionality. Currently, it delegates to the existing static version creation process to maintain compatibility.
    """
    print("Building bidirectional dashboard...")
    create_static_version()
    print("Bidirectional dashboard build completed (using static version)")

if __name__ == "__main__":
    create_static_version()
