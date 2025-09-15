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
    
    # Read the enhanced Euystacio Sacred Interface template
    with open('Euystacio_sacred_interface.html', 'r') as f:
        html_content = f.read()
    
    # Create simple static data injection for the sacred interface
    static_data_script = f"""
    <script>
        // Static data for GitHub Pages - Sacred Interface
        const STATIC_RED_CODE = {json.dumps(red_code, indent=2)};
        
        // Console logging for developers
        console.log('🌌 Euystacio Sacred Interface - Static GitHub Pages Version');
        console.log('Red Code Status:', STATIC_RED_CODE);
        
        // Add click handlers for access cards if they need interaction
        document.addEventListener('DOMContentLoaded', function() {{
            // Add accessibility enhancements
            const cards = document.querySelectorAll('.access-card');
            cards.forEach(card => {{
                card.addEventListener('click', function() {{
                    // Future: Add navigation to specific sections
                    console.log('Access card clicked:', this.querySelector('h3').textContent);
                }});
                
                // Keyboard support
                card.addEventListener('keydown', function(e) {{
                    if (e.key === 'Enter' || e.key === ' ') {{
                        e.preventDefault();
                        this.click();
                    }}
                }});
            }});
            
            // Enhanced download placeholder functionality
            const downloadBtn = document.querySelector('.download-placeholder');
            if (downloadBtn) {{
                downloadBtn.addEventListener('click', function(e) {{
                    e.preventDefault();
                    alert('🌿 Sacred documents portal\\n\\nDocuments are being prepared and will be available soon.\\n\\nFor the complete interactive experience with live documents,\\nvisit the full repository and run the local server.');
                }});
            }}
        }});
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
        'red_code.json'
    ]
    
    essential_dirs = [
        'docs',
        'examples', 
        'manifesto',
        'euystacio_presence_app',
        'static',
        'admin',
        '_posts'
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