## Euystacio Full Package Automated Deployment

To deploy the full Euystacio package into this repository, use the provided shell script:

### Steps

1. **Ensure you have cloned this repository and have the Euystacio_Full_Package directory available.**
2. **Run the deployment script:**

    ```bash
    ./deploy-euystacio.sh /path/to/Euystacio_Full_Package
    ```

3. **The script will:**
   - Copy all files from the package into the repo
   - Stage all changes
   - Commit with a unified pulse message
   - Push to the main branch

> **Note:** You must have Git installed and configured, and push permissions for the repository.

## 🚀 GitHub Pages Deployment

This repository automatically deploys to GitHub Pages whenever changes are pushed to the main branch.

### Automatic Deployment Process

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will:

1. **Build the static site** using the unified build system
2. **Copy all content** from the Euystacio_Full_Package folder and other essential directories
3. **Generate a unified dashboard** as the homepage (index.html)
4. **Deploy to GitHub Pages** with the static content

### Manual Local Build

To build the static site locally for testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Build the static site
python build_static.py

# The generated content will be in ./github_pages_deploy/
# Open ./github_pages_deploy/index.html in your browser to preview
```

### Deployment Features

- ✅ **Automatic deployment** on every push to main branch
- ✅ **Complete content inclusion** - all folders and files from Euystacio_Full_Package
- ✅ **Unified homepage** - professionally styled index.html served as the landing page
- ✅ **Jekyll compatibility** with proper _config.yml configuration
- ✅ **Seamless updates** - both initial setup and future changes work automatically

The deployed site will be available at: `https://[username].github.io/euystacio-helmi-AI/`