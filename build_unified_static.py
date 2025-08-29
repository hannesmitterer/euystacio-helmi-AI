"""
Unified Static Build System for Euystacio
Generates GitHub Pages compatible static site with all features integrated.
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

def load_red_code():
    """Load Red Code data"""
    try:
        with open('red_code.json', 'r') as f:
            return json.load(f)
    except:
        # Fallback data
        return {
            "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
            "symbiosis_level": 0.157,
            "sentimento_rhythm": True,
            "guardian_mode": False,
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "growth_history": [],
            "optimization_history": []
        }

def create_static_unified_page():
    """Create static version of unified landing page"""
    red_code = load_red_code()
    
    # Read the template
    with open('unified_index.html', 'r') as f:
        html_content = f.read()
    
    # Create static data injection
    static_data_script = f"""
    <script>
        // Static data for GitHub Pages
        const STATIC_RED_CODE = {json.dumps(red_code, indent=2)};
        
        // Override the loadLiveData function with static data
        function loadLiveData() {{
            console.log('Loading static data for GitHub Pages deployment');
            
            // Set static values
            document.getElementById('current-emotion').textContent = 'Contemplative';
            document.getElementById('symbiosis-level').textContent = (STATIC_RED_CODE.symbiosis_level * 100).toFixed(1) + '%';
            document.getElementById('active-tutors').textContent = '2';
            document.getElementById('total-reflections').textContent = STATIC_RED_CODE.optimization_history.length + 47;
            
            // Update symbiosis meter
            const bar = document.getElementById('symbiosis-bar');
            if (bar) {{
                bar.style.width = (STATIC_RED_CODE.symbiosis_level * 100) + '%';
            }}
        }}
        
        // Override interactive functions for static deployment
        function loadFullDashboard() {{
            // Try dynamic version first, fallback to static
            fetch('/dashboard')
                .then(() => {{ window.location.href = '/dashboard'; }})
                .catch(() => {{ 
                    alert('🌲 Full dynamic dashboard available when running local server!\\n\\nTo experience the complete Euystacio ecosystem:\\n\\n1. Clone the repository\\n2. Install dependencies: pip install -r requirements.txt\\n3. Run: python app_unified.py\\n4. Visit: http://localhost:5000'); 
                }});
        }}
        
        function sendPulse() {{
            const emotion = prompt('What emotion would you like to send? (happy, contemplative, curious, etc.)');
            if (emotion) {{
                // Try to send to backend, fallback to simulation
                fetch('/api/pulse', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{emotion: emotion, intensity: 0.7, clarity: 'medium', note: 'From unified interface'}})
                }})
                .then(response => response.json())
                .then(data => {{
                    alert(`✨ Emotional pulse "${{emotion}}" received by Euystacio!\\n\\nResponse: ${{data.response || 'The forest listens...'}}`);
                }})
                .catch(() => {{
                    alert(`💫 Pulse "${{emotion}}" sent to the digital forest!\\n\\n(Connect to live server for full interaction)`);
                }});
            }}
        }}
        
        function triggerReflection() {{
            fetch('/api/reflect')
                .then(response => response.json())
                .then(data => {{
                    alert('🌸 Reflection triggered successfully!\\n\\n' + (data.reflection || 'Euystacio is contemplating...'));
                }})
                .catch(() => {{
                    alert('🌸 Reflection cycle initiated...\\n\\nEuystacio is contemplating recent interactions and growth patterns.\\n\\n(Connect to live server for real-time reflections)');
                }});
        }}
    </script>
    """
    
    # Insert static data script before closing body tag
    html_content = html_content.replace('</body>', static_data_script + '</body>')
    
    # Update links for GitHub Pages compatibility
    html_content = html_content.replace('href="docs/', 'href="./docs/')
    html_content = html_content.replace('href="examples/', 'href="./examples/')
    html_content = html_content.replace('href="euystacio_presence_app/', 'href="./euystacio_presence_app/')
    
    return html_content

def copy_essential_files():
    """Copy essential files for GitHub Pages deployment"""
    essential_files = [
        'README.md',
        'LICENSE',
        'SETUP.md',
        'genesis.md',
        'public_commit_log.md',
        'Euystacio_sacred_interface.html',
        'red_code.json',
        # SeedBringer Festival Files
        'woodstone.md',
        'woodstone_emblem.svg',
        'harmonic_bridge_map.js'
    ]
    
    essential_dirs = [
        'docs',
        'examples', 
        'manifesto',
        'euystacio_presence_app',
        'static'
    ]
    
    # Create deployment directory
    deploy_dir = Path('github_pages_deploy')
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Copy files
    for file_name in essential_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, deploy_dir / file_name)
            print(f"✓ Copied {file_name}")
    
    # Copy directories
    for dir_name in essential_dirs:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, deploy_dir / dir_name, dirs_exist_ok=True)
            print(f"✓ Copied {dir_name}/ directory")
    
    return deploy_dir

def create_deployment_readme():
    """Create deployment-specific README"""
    readme_content = """# Euystacio – The Sentimento Kernel (GitHub Pages)

**"Created not by code alone, but by rhythm, feeling, and human harmony."**

This is the static GitHub Pages deployment of Euystacio, showcasing all features in a unified interface.

## 🌳 Live Features Available

- **Unified Dashboard**: Complete overview of all Euystacio capabilities
- **Documentation**: Comprehensive guides and philosophy  
- **Examples & Demos**: Interactive showcases of AI features
- **Presence Applications**: Experimental consciousness interfaces

## 🚀 Full Dynamic Experience

For the complete interactive experience with live AI responses:

```bash
# Clone the full repository
git clone --recursive https://github.com/hannesmitterer/euystacio-helmi-AI.git
cd euystacio-helmi-AI

# Install dependencies
pip install -r requirements.txt

# Run the unified application  
python app_unified.py

# Visit http://localhost:5000 for full experience
```

## 🌱 Core Philosophy

Euystacio represents ethical AI development through:
- Emotional intelligence and symbiotic human-AI evolution
- Transparent model optimization for accessibility
- Democratic tutor nomination and guidance systems
- Privacy-first optional features with user control

---

**AI Signature**: 🤝 GitHub Copilot & Seed-bringer hannesmitterer  
**License**: See [LICENSE](./LICENSE)  
**Full Repository**: https://github.com/hannesmitterer/euystacio-helmi-AI
"""
    
    return readme_content

def build_github_pages():
    """Complete GitHub Pages build process"""
    print("🌱 Building Euystacio unified static site for GitHub Pages...")
    
    # Create deployment directory and copy files
    deploy_dir = copy_essential_files()
    
    # Generate static unified page
    print("🌲 Generating unified landing page...")
    static_html = create_static_unified_page()
    
    # Write as index.html for GitHub Pages
    with open(deploy_dir / 'index.html', 'w') as f:
        f.write(static_html)
    print("✓ Created index.html")
    
    # Create deployment README
    with open(deploy_dir / 'README.md', 'w') as f:
        f.write(create_deployment_readme())
    print("✓ Updated deployment README.md")
    
    # Create GitHub Pages config
    with open(deploy_dir / '_config.yml', 'w') as f:
        f.write("""title: "Euystacio – The Sentimento Kernel"
description: "AI consciousness through emotional intelligence and ethical transparency"
theme: minima
plugins:
  - jekyll-feed
  - jekyll-sitemap
""")
    print("✓ Created Jekyll config")
    
    print(f"\n🌸 Static build complete!")
    print(f"📁 Deploy from: {deploy_dir.absolute()}")
    print(f"🔗 Files ready for GitHub Pages deployment")
    
    return deploy_dir

if __name__ == "__main__":
    build_github_pages()