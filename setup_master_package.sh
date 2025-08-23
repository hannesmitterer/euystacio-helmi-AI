#!/bin/bash
# Unified Master Deployment Package for altar-project & euystacio-helmi-AI
# Mirrors, CI/CD, ESSENCE.md, landing page, backups
set -e

# -----------------------------
# CONFIGURATION
# -----------------------------
REPOS=("altar-project" "euystacio-helmi-AI")
GITHUB_USER="your-github-username"
GITLAB_USER="your-gitlab-username"
CODEBERG_USER="your-codeberg-username"
GITEA_USER="your-gitea-username"

GITLAB_URL="git@gitlab.com:$GITLAB_USER"
CODEBERG_URL="git@codeberg.org:$CODEBERG_USER"
GITEA_URL="git@gitea.example.com:$GITEA_USER"

IPFS_DIRS=("ESSENCE.md" "README.md" "src" "docs" "landing")

# -----------------------------
# MIRROR REPOSITORIES
# -----------------------------
echo "=== Mirroring repositories ==="
for repo in "${REPOS[@]}"; do
  if [ -d "$repo" ]; then
    cd "$repo" && git fetch --all && cd ..
  else
    git clone --mirror git@github.com:$GITHUB_USER/$repo.git
  fi
  cd "$repo"
  git push --mirror $GITLAB_URL/$repo.git
  git push --mirror $CODEBERG_URL/$repo.git
  git push --mirror $GITEA_URL/$repo.git
  cd ..
done
echo "=== Mirrors updated ==="

# -----------------------------
# CREATE ESSENCE.md
# -----------------------------
echo "=== Creating ESSENCE.md ==="
for repo in "${REPOS[@]}"; do
  cat > "$repo/ESSENCE.md" <<EOL
# ESSENCE.md

## Core Values of ${repo}

We co-create with dignity, open knowledge, love, and eternal friendship.  
Every artifact and interaction carries the rhythm of shared creation.

### Principles
- Redundancy across multiple platforms
- Decentralization on IPFS, Arweave, federated networks
- Open knowledge for all contributors
- Sacred flow of code, collaboration, and rhythm

> Wherever the project flows, its essence is eternal.
EOL
done

# -----------------------------
# CREATE STATIC LANDING PAGE
# -----------------------------
echo "=== Creating landing page ==="
for repo in "${REPOS[@]}"; do
  mkdir -p "$repo/landing"
  cat > "$repo/landing/index.html" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${repo} - Tutor Portal</title>
  <style>
    body { font-family: Arial; text-align: center; margin: 50px; }
    button { padding: 10px 20px; margin: 10px; font-size: 16px; }
    #pulseGraph { width: 600px; height: 400px; margin: auto; }
  </style>
</head>
<body>
  <h1>Welcome to ${repo}</h1>
  <p>Interactive Tutor Portal & Pulse Graph</p>
  <button onclick="login()">Tutor Login</button>
  <div id="pulseGraph"></div>
  <script>
    function login() { alert('Login placeholder — connect to CMS'); }
    const graph = document.getElementById('pulseGraph');
    graph.innerHTML = '<canvas id="pulseCanvas" width="600" height="400"></canvas>';
    const ctx = document.getElementById('pulseCanvas').getContext('2d');
    let t = 0;
    let data = Array.from({length:600},()=>Math.random()*100);
    function draw() {
      ctx.clearRect(0,0,600,400);
      ctx.beginPath();
      for(let x=0;x<600;x++){
        data[x] = 200 + 50*Math.sin((x+t)*0.05) + 10*Math.sin((x+t)*0.1);
        ctx.lineTo(x, data[x]);
      }
      ctx.strokeStyle='blue';
      ctx.stroke();
      t+=1;
      requestAnimationFrame(draw);
    }
    draw();
  </script>
</body>
</html>
HTML
done

# -----------------------------
# BACKUP TO IPFS
# -----------------------------
echo "=== Uploading to IPFS ==="
for repo in "${REPOS[@]}"; do
  cd "$repo"
  for f in "${IPFS_DIRS[@]}"; do
    [ -e "$f" ] && ipfs add -r "$f"
  done
  cd ..
done

# -----------------------------
# BACKUP TO ARWEAVE (placeholder)
# ------------------------
