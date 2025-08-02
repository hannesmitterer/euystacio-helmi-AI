import os
import shutil
import re

def create_static_version():
    """
    Create a static version of the dashboard by copying template files
    and converting Flask template syntax to static paths.
    """
    print("Creating static version...")
    
    # Ensure docs directory structure exists
    os.makedirs("docs", exist_ok=True)
    os.makedirs("docs/css", exist_ok=True)
    os.makedirs("docs/js", exist_ok=True)
    os.makedirs("docs/images", exist_ok=True)
    
    # Copy static assets
    if os.path.exists("static/css/style.css"):
        shutil.copy2("static/css/style.css", "docs/css/style.css")
        print("✓ Copied CSS files")
    
    if os.path.exists("static/js/app.js"):
        shutil.copy2("static/js/app.js", "docs/js/app-static.js")
        print("✓ Copied JS files")
    
    # Copy avatar image
    if os.path.exists("static/euystacio-avatar.jpg"):
        shutil.copy2("static/euystacio-avatar.jpg", "docs/images/euystacio-avatar.jpg")
        print("✓ Copied avatar image")
    
    # Convert template to static HTML
    if os.path.exists("templates/index.html"):
        with open("templates/index.html", "r") as f:
            content = f.read()
        
        # Replace Flask template syntax with static paths
        content = re.sub(
            r'\{\{\s*url_for\(\'static\',\s*filename=\'css/style\.css\'\)\s*\}\}',
            'css/style.css',
            content
        )
        content = re.sub(
            r'\{\{\s*url_for\(\'static\',\s*filename=\'js/app\.js\'\)\s*\}\}',
            'js/app-static.js',
            content
        )
        content = re.sub(
            r'\{\{\s*url_for\(\'static\',\s*filename=\'euystacio-avatar\.jpg\'\)\s*\}\}',
            'images/euystacio-avatar.jpg',
            content
        )
        
        with open("docs/index.html", "w") as f:
            f.write(content)
        print("✓ Generated static HTML")
    
    print("Static version created successfully!")

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
