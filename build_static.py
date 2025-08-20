"""
Unified static build system that generates GitHub Pages compatible version
"""

import os
import shutil
from pathlib import Path

def create_static_version():
    """Create static version using the unified build system"""
    print("🌱 Creating static version using unified build system...")
    
    # Use the unified build system
    from build_unified_static import build_github_pages
    
    deploy_dir = build_github_pages()
    print(f"✅ Static version created at: {deploy_dir}")
    
    return deploy_dir

def build_bidirectional_dashboard():
    """
    Enhanced bidirectional dashboard creation using the unified system.
    Creates a comprehensive static site with all features integrated.
    """
    print("🌲 Building enhanced bidirectional dashboard...")
    
    deploy_dir = create_static_version()
    
    print("🌸 Enhanced bidirectional dashboard build completed!")
    print(f"📁 Ready for deployment from: {deploy_dir.absolute()}")
    
    return deploy_dir

if __name__ == "__main__":
    build_bidirectional_dashboard()
