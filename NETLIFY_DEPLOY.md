# Netlify Deploy Key Configuration

This document describes the SSH deploy key configuration for Netlify deployment of the Euystacio repository.

## Overview

The repository has been configured to use an SSH deploy key for secure access during Netlify builds. This setup allows Netlify to access the repository and any private dependencies during the build process.

## Deploy Key Details

- **Public Key Location**: `.ssh/netlify_deploy_key.pub`
- **SSH Config**: `.ssh/config`
- **Deploy Script**: `deploy_setup.sh`

## Files Added/Modified

### 1. SSH Configuration (`.ssh/config`)
Contains SSH host configuration for GitHub access with the deploy key:
```
Host github.com-netlify
    HostName github.com
    User git
    IdentityFile ~/.ssh/netlify_deploy_key
    IdentitiesOnly yes
    StrictHostKeyChecking no
```

### 2. Public Deploy Key (`.ssh/netlify_deploy_key.pub`)
The SSH public key provided for Netlify deployment access.

### 3. Deployment Setup Script (`deploy_setup.sh`)
Bash script that:
- Sets up the SSH environment during Netlify builds
- Copies SSH configuration and keys to the correct locations
- Sets appropriate file permissions
- Runs the build process

### 4. Updated Netlify Configuration (`netlify.toml`)
Modified to use the deployment setup script and include environment variables for SSH:
```toml
[build]
  publish = "static"
  command = "./deploy_setup.sh"

[build.environment]
  PYTHON_VERSION = "3.8"
  SSH_AUTH_SOCK = ""
  GIT_SSH_COMMAND = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
```

### 5. Enhanced Build Script (`build_static.py`)
Improved to properly create static files from the docs directory.

## Netlify Setup Requirements

To complete the deployment setup, the following steps are needed in the Netlify dashboard:

1. **Add the corresponding private key** to Netlify:
   - Go to Site Settings > Build & Deploy > Environment Variables
   - Add the private key that corresponds to the public key in this repository

2. **Configure the repository** in Netlify:
   - Connect the repository to Netlify
   - Ensure the build command is set to use `./deploy_setup.sh`
   - Set the publish directory to `static`

## GitHub Repository Setup

The public key should also be added to the GitHub repository as a deploy key:

1. Go to Repository Settings > Deploy keys
2. Add the public key from `.ssh/netlify_deploy_key.pub`
3. Enable "Allow write access" if needed for the deployment process

## Security Notes

- Only the public key is stored in the repository
- The private key should be securely stored in Netlify's environment variables
- SSH connections are configured with appropriate security settings
- File permissions are set correctly during the build process

## Testing

The deployment can be tested locally by running:
```bash
./deploy_setup.sh
```

This will set up the SSH environment and build the static files for deployment.