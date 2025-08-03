#!/usr/bin/env python3
"""
Static site build script for Euystacio Netlify deployment.
Generates static HTML files from the Flask application.
"""

import os
import json
import shutil
from pathlib import Path

def create_static_version():
    """
    Create static version of the dashboard for deployment.
    """
    print("Building static version for deployment...")
    
    # Ensure static directory exists
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    # Copy existing docs to static directory for deployment
    docs_dir = Path("docs")
    if docs_dir.exists():
        print("Copying docs directory to static...")
        if static_dir.exists():
            shutil.rmtree(static_dir)
        shutil.copytree(docs_dir, static_dir)
    
    # Create basic index.html if it doesn't exist
    index_file = static_dir / "index.html"
    if not index_file.exists():
        print("Creating basic index.html...")
        index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Euystacio - The Sentimento Kernel</title>
</head>
<body>
    <h1>🌳 Euystacio Dashboard</h1>
    <p>"Created not by code alone, but by rhythm, feeling, and human harmony."</p>
    <p>Static deployment successful!</p>
</body>
</html>"""
        index_file.write_text(index_content)
    
    print(f"Static build completed. Files available in {static_dir}")

def build_bidirectional_dashboard():
    """
    Stub function for bidirectional dashboard creation.
    This function serves as a placeholder for potential future bidirectional dashboard functionality. 
    Currently, it delegates to the existing static version creation process to maintain compatibility.
    """
    print("Building bidirectional dashboard...")
    create_static_version()
    print("Bidirectional dashboard build completed (using static version)")

if __name__ == "__main__":
    build_bidirectional_dashboard()
