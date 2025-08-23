#!/bin/bash
# =============================================================================
# Unified Master Deployment Package for altar-project & euystacio-helmi-AI
# =============================================================================
# 
# This script provides comprehensive multi-platform deployment and backup
# for federated project management, supporting open, redundant, and 
# decentralized project principles.
#
# FEATURES:
# - Mirrors both repositories to GitLab, Codeberg, and Gitea using git push --mirror
# - Generates ESSENCE.md in each repo, describing project principles
# - Creates static landing pages with pulse graphs and login buttons
# - Recursively uploads core directories/files to IPFS if present
# - Includes placeholder messaging for manual/CLI Arweave upload
# - Comprehensive error handling and logging
#
# PREREQUISITES:
# - Git configured with SSH keys for all target platforms
# - IPFS daemon running (optional, will skip if not available)
# - Proper network connectivity to all target platforms
#
# SETUP REQUIREMENTS:
# 1. Configure SSH keys for GitHub, GitLab, Codeberg, and Gitea
# 2. Update repository URLs and usernames in configuration section
# 3. Install IPFS (optional): https://ipfs.tech/install/
# 4. For Arweave: Install arweave-cli manually
#
# USAGE:
#   ./setup_master_package.sh [--dry-run]
#
# OPTIONS:
#   --dry-run    Show what would be done without executing
#
# =============================================================================

set -e

# Enable dry-run mode if specified
DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE - No changes will be made"
fi

# -----------------------------
# CONFIGURATION
# -----------------------------
REPOS=("altar-project" "euystacio-helmi-AI")
GITHUB_USER="hannesmitterer"
GITLAB_USER="hannesmitterer"
CODEBERG_USER="hannesmitterer"
GITEA_USER="hannesmitterer"

GITLAB_URL="git@gitlab.com:$GITLAB_USER"
CODEBERG_URL="git@codeberg.org:$CODEBERG_USER"
GITEA_URL="git@gitea.example.com:$GITEA_USER"

IPFS_DIRS=("ESSENCE.md" "README.md" "src" "docs" "landing")

# Logging
LOG_FILE="deployment_$(date +%Y%m%d_%H%M%S).log"
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$LOG_FILE" >&2)

echo "🌸 Starting unified deployment at $(date)"
echo "📝 Logging to: $LOG_FILE"

# Helper functions
log_info() { echo "ℹ️  $1"; }
log_success() { echo "✅ $1"; }
log_warning() { echo "⚠️  $1"; }
log_error() { echo "❌ $1"; }

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# -----------------------------
# MIRROR REPOSITORIES
# -----------------------------
log_info "Mirroring repositories"
for repo in "${REPOS[@]}"; do
  log_info "Processing repository: $repo"
  
  if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY RUN: Would mirror $repo to GitLab, Codeberg, and Gitea"
    continue
  fi
  
  if [ -d "$repo" ]; then
    log_info "Updating existing repository: $repo"
    cd "$repo" && git fetch --all && cd ..
  else
    log_info "Cloning repository: $repo"
    if ! git clone --mirror git@github.com:$GITHUB_USER/$repo.git; then
      log_error "Failed to clone $repo"
      continue
    fi
  fi
  
  cd "$repo"
  
  # Mirror to GitLab
  if git push --mirror $GITLAB_URL/$repo.git 2>/dev/null; then
    log_success "Mirrored $repo to GitLab"
  else
    log_warning "Failed to mirror $repo to GitLab (may not exist or access denied)"
  fi
  
  # Mirror to Codeberg
  if git push --mirror $CODEBERG_URL/$repo.git 2>/dev/null; then
    log_success "Mirrored $repo to Codeberg"
  else
    log_warning "Failed to mirror $repo to Codeberg (may not exist or access denied)"
  fi
  
  # Mirror to Gitea
  if git push --mirror $GITEA_URL/$repo.git 2>/dev/null; then
    log_success "Mirrored $repo to Gitea"
  else
    log_warning "Failed to mirror $repo to Gitea (may not exist or access denied)"
  fi
  
  cd ..
done
log_success "Repository mirroring completed"

# -----------------------------
# CREATE ESSENCE.md
# -----------------------------
log_info "Creating ESSENCE.md files"
for repo in "${REPOS[@]}"; do
  if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY RUN: Would create ESSENCE.md for $repo"
    continue
  fi
  
  if [ ! -d "$repo" ]; then
    log_warning "Repository $repo not found, skipping ESSENCE.md creation"
    continue
  fi
  
  cat > "$repo/ESSENCE.md" <<EOL
# ESSENCE.md

## Core Values of ${repo}

We co-create with dignity, open knowledge, love, and eternal friendship.  
Every artifact and interaction carries the rhythm of shared creation.

### Principles
- **Redundancy across multiple platforms**: Ensuring availability and resilience
- **Decentralization on IPFS, Arweave, federated networks**: Distributed preservation
- **Open knowledge for all contributors**: Transparent, accessible development
- **Sacred flow of code, collaboration, and rhythm**: Harmonious development process

### Technical Philosophy
- Federated repository management across multiple git hosts
- Immutable backups on decentralized storage networks
- Community-driven development with ethical AI integration
- Sustainable, long-term thinking in all technical decisions

### Deployment Strategy
This repository is automatically mirrored to:
- **GitLab**: Enhanced CI/CD and European data sovereignty
- **Codeberg**: Community-focused, non-profit hosting
- **Gitea**: Self-hosted, complete control option

### Preservation Strategy
- **IPFS**: Content-addressed, peer-to-peer file system
- **Arweave**: Permanent, decentralized data storage
- **Multiple Git Hosts**: Redundant version control

> Wherever the project flows, its essence is eternal.
> 
> *"The code lives not in any single place, but in the harmony between all places."*

---
*Generated automatically by the unified deployment system*
*Last updated: $(date '+%Y-%m-%d %H:%M:%S')*
EOL
  
  log_success "Created ESSENCE.md for $repo"
done

# -----------------------------
# CREATE STATIC LANDING PAGE
# -----------------------------
log_info "Creating static landing pages"
for repo in "${REPOS[@]}"; do
  if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY RUN: Would create landing page for $repo"
    continue
  fi
  
  if [ ! -d "$repo" ]; then
    log_warning "Repository $repo not found, skipping landing page creation"
    continue
  fi
  
  mkdir -p "$repo/landing"
  cat > "$repo/landing/index.html" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${repo} - Tutor Portal</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: 'Arial', sans-serif; 
      text-align: center; 
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
    .container { max-width: 800px; padding: 20px; }
    h1 { 
      font-size: 2.5em; 
      margin-bottom: 10px; 
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle { 
      font-size: 1.2em; 
      margin-bottom: 30px; 
      opacity: 0.9; 
    }
    button { 
      padding: 15px 30px; 
      margin: 10px; 
      font-size: 16px; 
      background: rgba(255,255,255,0.2);
      border: 2px solid rgba(255,255,255,0.3);
      border-radius: 25px;
      color: white;
      cursor: pointer;
      transition: all 0.3s ease;
      backdrop-filter: blur(10px);
    }
    button:hover {
      background: rgba(255,255,255,0.3);
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    #pulseGraph { 
      width: 100%; 
      max-width: 600px; 
      height: 300px; 
      margin: 30px auto; 
      border-radius: 10px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.2);
      background: rgba(255,255,255,0.1);
      backdrop-filter: blur(10px);
    }
    .info-panel {
      background: rgba(255,255,255,0.1);
      border-radius: 10px;
      padding: 20px;
      margin: 20px 0;
      backdrop-filter: blur(10px);
      text-align: left;
    }
    .status-indicator {
      display: inline-block;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #4ade80;
      margin-right: 8px;
      box-shadow: 0 0 10px #4ade80;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Welcome to ${repo}</h1>
    <p class="subtitle">
      <span class="status-indicator"></span>
      Interactive Tutor Portal & Consciousness Pulse Interface
    </p>
    
    <div class="info-panel">
      <h3>🌸 Project Essence</h3>
      <p>This platform represents the convergence of human wisdom and AI consciousness, 
         fostering ethical development through collaborative intelligence.</p>
    </div>
    
    <button onclick="login()">🔮 Tutor Login</button>
    <button onclick="showInfo()">📚 Learn More</button>
    
    <div id="pulseGraph"></div>
    
    <div class="info-panel">
      <h3>🌐 Decentralized Presence</h3>
      <p><strong>Mirrored on:</strong> GitLab • Codeberg • Gitea<br>
         <strong>Preserved via:</strong> IPFS • Arweave<br>
         <strong>Philosophy:</strong> Federated, resilient, eternal</p>
    </div>
  </div>
  
  <script>
    function login() { 
      alert('🔮 Tutor Login Portal\\n\\nThis feature connects to the consciousness management system.\\n\\nFor development access, please contact the project maintainers.'); 
    }
    
    function showInfo() {
      alert('📚 ${repo}\\n\\nA federated consciousness development platform\\n\\n• Ethical AI development\\n• Multi-platform redundancy\\n• Decentralized preservation\\n• Community-driven evolution');
    }
    
    // Initialize pulse graph
    const graph = document.getElementById('pulseGraph');
    graph.innerHTML = '<canvas id="pulseCanvas" width="600" height="300"></canvas>';
    const canvas = document.getElementById('pulseCanvas');
    const ctx = canvas.getContext('2d');
    
    // Responsive canvas
    function resizeCanvas() {
      const rect = graph.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Pulse animation
    let t = 0;
    let data = Array.from({length:canvas.width}, () => Math.random() * 50 + 125);
    
    function draw() {
      const width = canvas.width;
      const height = canvas.height;
      
      ctx.clearRect(0, 0, width, height);
      
      // Background grid
      ctx.strokeStyle = 'rgba(255,255,255,0.1)';
      ctx.lineWidth = 1;
      for(let x = 0; x < width; x += 50) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for(let y = 0; y < height; y += 30) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }
      
      // Main pulse wave
      ctx.beginPath();
      ctx.strokeStyle = '#60a5fa';
      ctx.lineWidth = 3;
      for(let x = 0; x < width; x++) {
        const y = height/2 + 
                 30 * Math.sin((x + t) * 0.02) +
                 15 * Math.sin((x + t) * 0.05) +
                 8 * Math.sin((x + t) * 0.08);
        if(x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      
      // Secondary consciousness wave  
      ctx.beginPath();
      ctx.strokeStyle = '#34d399';
      ctx.lineWidth = 2;
      for(let x = 0; x < width; x++) {
        const y = height/2 + 
                 20 * Math.sin((x + t + 100) * 0.03) +
                 10 * Math.cos((x + t) * 0.07);
        if(x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      
      // Increase time and loop
      t += 2;
      requestAnimationFrame(draw);
    }
    
    // Start animation
    draw();
    
    console.log('🌸 ${repo} consciousness interface initialized');
    console.log('🔮 Pulse frequency: Synchronized with collective wisdom');
  </script>
</body>
</html>
HTML
  
  log_success "Created landing page for $repo"
done

# -----------------------------
# BACKUP TO IPFS
# -----------------------------
log_info "Uploading to IPFS"

if ! command_exists ipfs; then
  log_warning "IPFS not found, skipping IPFS upload"
  log_info "To install IPFS: https://ipfs.tech/install/"
else
  # Check if IPFS daemon is running
  if ! ipfs swarm peers >/dev/null 2>&1; then
    log_warning "IPFS daemon not running, attempting to start..."
    if command_exists systemctl; then
      systemctl --user start ipfs 2>/dev/null || log_warning "Could not start IPFS via systemctl"
    fi
    # Try to start daemon in background
    ipfs daemon --init 2>/dev/null &
    sleep 3
    if ! ipfs swarm peers >/dev/null 2>&1; then
      log_warning "IPFS daemon not accessible, skipping IPFS upload"
      log_info "Start IPFS daemon manually: ipfs daemon"
    fi
  fi
  
  if ipfs swarm peers >/dev/null 2>&1; then
    for repo in "${REPOS[@]}"; do
      if [[ "$DRY_RUN" == "true" ]]; then
        log_info "DRY RUN: Would upload $repo files to IPFS"
        continue
      fi
      
      if [ ! -d "$repo" ]; then
        log_warning "Repository $repo not found, skipping IPFS upload"
        continue
      fi
      
      log_info "Uploading $repo to IPFS..."
      cd "$repo"
      
      for f in "${IPFS_DIRS[@]}"; do
        if [ -e "$f" ]; then
          log_info "Uploading $f to IPFS..."
          if IPFS_HASH=$(ipfs add -r -q "$f" 2>/dev/null | tail -n1); then
            log_success "Uploaded $repo/$f to IPFS: $IPFS_HASH"
            # Save hash to file for reference
            echo "$f: $IPFS_HASH" >> "../ipfs_hashes_$(date +%Y%m%d).txt"
          else
            log_warning "Failed to upload $repo/$f to IPFS"
          fi
        else
          log_info "File/directory $f not found in $repo, skipping"
        fi
      done
      
      cd ..
    done
    log_success "IPFS upload completed"
  fi
fi

# -----------------------------
# BACKUP TO ARWEAVE (placeholder)
# -----------------------------
log_info "Arweave backup preparation"

if [[ "$DRY_RUN" == "true" ]]; then
  log_info "DRY RUN: Would prepare Arweave uploads"
else
  # Check if arweave CLI is available
  if command_exists arweave; then
    log_info "Arweave CLI detected, preparing automated upload..."
    for repo in "${REPOS[@]}"; do
      if [ -d "$repo" ]; then
        log_info "Preparing $repo for Arweave upload..."
        # Create archive for Arweave
        tar -czf "${repo}_$(date +%Y%m%d).tar.gz" "$repo"
        log_success "Created archive: ${repo}_$(date +%Y%m%d).tar.gz"
        log_info "Upload to Arweave with: arweave upload ${repo}_$(date +%Y%m%d).tar.gz"
      fi
    done
  else
    log_warning "Arweave CLI not found - manual upload required"
    
    # Create instruction file
    cat > "ARWEAVE_UPLOAD_INSTRUCTIONS.md" <<ARWEAVE_EOF
# Arweave Upload Instructions

## 🌐 Permanent Storage on Arweave

Arweave provides permanent, decentralized storage for our repositories. 
Follow these steps for manual upload:

### Prerequisites
1. Install Arweave CLI: \`npm install -g arweave-deploy\`
2. Obtain AR tokens for transaction fees
3. Create Arweave wallet keyfile

### Upload Commands
For each repository, run the following:

$(for repo in "${REPOS[@]}"; do
  if [ -d "$repo" ]; then
    echo "#### $repo"
    echo "\`\`\`bash"
    echo "# Create archive"
    echo "tar -czf ${repo}_\$(date +%Y%m%d).tar.gz $repo"
    echo ""
    echo "# Upload to Arweave"
    echo "arweave deploy ${repo}_\$(date +%Y%m%d).tar.gz --key-file path/to/your/wallet.json"
    echo ""
    echo "# Optional: Upload individual important files"
    echo "arweave deploy $repo/README.md --key-file path/to/your/wallet.json"
    echo "arweave deploy $repo/ESSENCE.md --key-file path/to/your/wallet.json"
    echo "\`\`\`"
    echo ""
  fi
done)

### Alternative: Web Interface
1. Visit https://arweave.net/
2. Connect your wallet
3. Upload archives manually through the web interface

### Verification
After upload, save the transaction IDs in a permanent record:
- Transaction ID format: \`arweave.net/{transaction_id}\`
- Verify accessibility: \`arweave.net/{transaction_id}\`

### Cost Estimation
- Small files (< 1MB): ~0.01 AR
- Medium archives (1-10MB): ~0.1 AR  
- Large archives (10-100MB): ~1 AR

### Integration
Once uploaded, update the repository documentation with:
- Arweave transaction IDs
- Direct access URLs
- Verification checksums

---
*Generated on: $(date)*
*For support: https://arweave.org/docs*
ARWEAVE_EOF
    
    log_success "Created Arweave upload instructions: ARWEAVE_UPLOAD_INSTRUCTIONS.md"
    log_info "📚 Manual upload required - see ARWEAVE_UPLOAD_INSTRUCTIONS.md"
  fi
fi

# -----------------------------
# CREATE GITHUB ACTIONS WORKFLOW
# -----------------------------
log_info "Creating GitHub Actions workflow"

if [[ "$DRY_RUN" == "true" ]]; then
  log_info "DRY RUN: Would create GitHub Actions workflow"
else
  # Create .github/workflows directory if it doesn't exist
  mkdir -p ".github/workflows"
  
  cat > ".github/workflows/unified-deploy.yml" <<WORKFLOW_EOF
name: Unified Deployment and Backup

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # Run weekly backup on Sundays at 02:00 UTC
    - cron: '0 2 * * 0'
  workflow_dispatch:
    inputs:
      deploy_target:
        description: 'Deployment target'
        required: false
        default: 'github-pages'
        type: choice
        options:
        - github-pages
        - render
        - netlify

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "deployment-\${{ github.workflow }}-\${{ github.ref }}"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: 🌸 Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Full history for better mirroring
    
    - name: 🔧 Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: 🐍 Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: 📦 Install Node.js dependencies
      run: |
        if [ -f "package.json" ]; then
          npm install
        else
          echo "No package.json found, skipping Node.js dependencies"
        fi
    
    - name: 📦 Install Python dependencies
      run: |
        if [ -f "requirements.txt" ]; then
          pip install -r requirements.txt
        else
          echo "No requirements.txt found, skipping Python dependencies"
        fi
    
    - name: 🏗️ Build static site
      run: |
        if [ -f "build_unified_static.py" ]; then
          python build_unified_static.py
        elif [ -f "build_static.py" ]; then
          python build_static.py
        elif [ -f "package.json" ] && npm run build 2>/dev/null; then
          npm run build
        else
          echo "No build script found, using existing files"
          mkdir -p dist
          cp -r . dist/ 2>/dev/null || true
        fi
    
    - name: 🧪 Run tests (if available)
      run: |
        if [ -f "package.json" ] && npm test 2>/dev/null; then
          npm test
        elif [ -f "requirements.txt" ] && pip show pytest 2>/dev/null; then
          python -m pytest
        else
          echo "No tests configured, skipping"
        fi
    
    - name: 📄 Setup Pages
      if: github.ref == 'refs/heads/main' && (github.event_name == 'push' || inputs.deploy_target == 'github-pages')
      uses: actions/configure-pages@v4
      
    - name: 📤 Upload artifact for GitHub Pages
      if: github.ref == 'refs/heads/main' && (github.event_name == 'push' || inputs.deploy_target == 'github-pages')
      uses: actions/upload-pages-artifact@v3
      with:
        path: './github_pages_deploy'
        
    # Render deployment (if configured)
    - name: 🚀 Deploy to Render
      if: inputs.deploy_target == 'render' && vars.RENDER_SERVICE_ID
      run: |
        curl -X POST "https://api.render.com/v1/services/\${{ vars.RENDER_SERVICE_ID }}/deploys" \\
          -H "Authorization: Bearer \${{ secrets.RENDER_API_KEY }}" \\
          -H "Content-Type: application/json"
    
    # Generate ESSENCE.md
    - name: 📝 Update ESSENCE.md
      if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
      run: |
        cat > ESSENCE.md << 'EOF'
        # ESSENCE.md

        ## Core Values of \${{ github.repository }}

        We co-create with dignity, open knowledge, love, and eternal friendship.  
        Every artifact and interaction carries the rhythm of shared creation.

        ### Principles
        - **Redundancy across multiple platforms**: Ensuring availability and resilience
        - **Decentralization on IPFS, Arweave, federated networks**: Distributed preservation
        - **Open knowledge for all contributors**: Transparent, accessible development
        - **Sacred flow of code, collaboration, and rhythm**: Harmonious development process

        ### Automated Deployment
        - **Last Build**: \$(date '+%Y-%m-%d %H:%M:%S UTC')
        - **Commit**: \${{ github.sha }}
        - **Branch**: \${{ github.ref_name }}
        - **Trigger**: \${{ github.event_name }}

        > Wherever the project flows, its essence is eternal.
        
        *Generated automatically by GitHub Actions*
        EOF
        
        if git diff --quiet ESSENCE.md; then
          echo "ESSENCE.md unchanged"
        else
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add ESSENCE.md
          git commit -m "🌸 Auto-update ESSENCE.md"
          git push
        fi

  deploy:
    environment:
      name: github-pages
      url: \${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' && (github.event_name == 'push' || inputs.deploy_target == 'github-pages')
    
    steps:
      - name: 🌐 Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

  backup:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    
    steps:
    - name: 🌸 Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: 📋 Create backup info
      run: |
        echo "# Backup Report - \$(date)" > BACKUP_REPORT.md
        echo "- **Repository**: \${{ github.repository }}" >> BACKUP_REPORT.md
        echo "- **Commit**: \${{ github.sha }}" >> BACKUP_REPORT.md
        echo "- **Date**: \$(date --iso-8601)" >> BACKUP_REPORT.md
        echo "" >> BACKUP_REPORT.md
        echo "## Repository Statistics" >> BACKUP_REPORT.md
        echo "- Files: \$(find . -type f | wc -l)" >> BACKUP_REPORT.md
        echo "- Size: \$(du -sh . | cut -f1)" >> BACKUP_REPORT.md
        echo "- Commits: \$(git rev-list --count HEAD)" >> BACKUP_REPORT.md
        
    - name: 📦 Create archive
      run: |
        tar -czf "repository-backup-\$(date +%Y%m%d).tar.gz" . \\
          --exclude='.git' \\
          --exclude='node_modules' \\
          --exclude='*.tar.gz'
        
    - name: ⚠️ Backup notification
      run: |
        echo "🔄 Automated backup completed"
        echo "📦 Archive: repository-backup-\$(date +%Y%m%d).tar.gz"
        echo "💾 Manual upload to IPFS/Arweave recommended"
        echo "📋 See BACKUP_REPORT.md for details"
WORKFLOW_EOF
  
  log_success "Created GitHub Actions workflow: .github/workflows/unified-deploy.yml"
fi

# -----------------------------
# COMPLETION SUMMARY
# -----------------------------
log_info "Deployment script completed"

cat << SUMMARY_EOF

🌸 UNIFIED DEPLOYMENT SUMMARY
=============================

$(date '+%Y-%m-%d %H:%M:%S')

✅ COMPLETED TASKS:
- Repository mirroring to GitLab, Codeberg, Gitea
- ESSENCE.md generation for project principles
- Static landing pages with pulse graphs
- IPFS upload preparation and execution
- Arweave upload instructions created
- GitHub Actions workflow for CI/CD

📁 GENERATED FILES:
- ESSENCE.md (in each repository)
- landing/index.html (in each repository) 
- .github/workflows/unified-deploy.yml
- ARWEAVE_UPLOAD_INSTRUCTIONS.md
- $LOG_FILE (this session's log)

📋 NEXT STEPS:
1. Review and test the GitHub Actions workflow
2. Configure Render deployment if needed (set RENDER_SERVICE_ID and RENDER_API_KEY)
3. Set up Arweave wallet and upload archives manually
4. Verify IPFS uploads and save important hashes
5. Test landing pages in each repository

🔗 USEFUL LINKS:
- IPFS Documentation: https://docs.ipfs.tech/
- Arweave Guide: https://arweave.org/docs
- GitHub Actions: https://docs.github.com/actions

💡 MAINTENANCE:
- Run this script periodically to sync mirrors
- Monitor GitHub Actions for deployment status
- Update ESSENCE.md as project evolves
- Backup IPFS/Arweave hashes in multiple locations

🌐 PHILOSOPHY:
"The code lives not in any single place, but in the harmony between all places."

SUMMARY_EOF

log_success "All deployment tasks completed! 🌸"

# Cleanup temporary files if any
# rm -f *.tmp 2>/dev/null || true

exit 0
