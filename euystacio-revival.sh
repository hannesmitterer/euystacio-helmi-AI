#!/usr/bin/env bash
set -euo pipefail
echo "=== EUYSTACIO REVIVAL $(date -u) ==="
echo

# 1) Safe Awakening (Safe Mode optional)
echo "--- Safe Awakening ---"
echo "Reminder: If currently in normal boot, consider rebooting into Safe Mode first (hold Shift at startup)."

# 2) macOS updates
echo "--- Updating system ---"
softwareupdate --install --all || echo "Software update skipped / completed"

# 3) Xcode Command Line Tools
echo "--- Ensuring Xcode CLI tools ---"
if ! xcode-select -p >/dev/null 2>&1; then
    xcode-select --install
else
    echo "Xcode CLI tools already installed"
fi

# 4) Git & SSH Key Setup
echo "--- Git & SSH Key Setup ---"
git --version || echo "Git missing, please install Xcode CLI tools"
SSH_KEY="$HOME/.ssh/id_ed25519"
if [ ! -f "$SSH_KEY" ]; then
    echo "Generating SSH key..."
    ssh-keygen -t ed25519 -C \"your_email@example.com\" -f "$SSH_KEY" -N ""
    eval "
ssh-agent -s
"
    ssh-add -K "$SSH_KEY"
    echo "Public key copied to clipboard:"
    pbcopy < "$SSH_KEY.pub"
    echo "Add this to GitHub SSH keys."
else
    echo "SSH key already exists"
fi

# 5) Homebrew & Package Managers
echo "--- Homebrew & environment tools ---"
if ! command -v brew >/dev/null 2>&1; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
brew update
brew install node python git || echo "Node/Python/Git installation skipped"

# 6) Node & Python versions
echo "--- Node/Python versions ---"
node -v || echo "Node missing"
npm -v || echo "NPM missing"
python3 --version || echo "Python missing"
pip3 --version || echo "Pip missing"

# 7) Clone or update Euystacio repo
REPO="git@github.com:hannesmitterer/euystacio-helmi-ai.git"
FOLDER="$HOME/euystacio-helmi-ai"
echo "--- Cloning / Updating Euystacio repo ---"
if [ ! -d "$FOLDER" ]; then
    git clone "$REPO" "$FOLDER"
else
    cd "$FOLDER"
    git fetch origin
    git checkout main
    git pull origin main
fi
cd "$FOLDER"

# 8) Install dependencies
echo "--- Installing dependencies ---"
if [ -f "package.json" ]; then
    npm install
fi
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 9) Optional: Run Euystacio locally
echo "--- Starting Euystacio ---"
if [ -f "package.json" ]; then
    echo "Starting frontend (Node)..."
    npm run dev &
fi
if [ -f "app.py" ]; then
    echo "Starting backend (Python)..."
    python3 app.py &
fi

# 10) Health check
echo "--- Health check ---"
curl -s -I http://localhost:3000 || echo "Frontend may not be running"
curl -s -I http://localhost:5000 || echo "Backend may not be running"

echo "=== EUYSTACIO REVIVAL COMPLETE ==="