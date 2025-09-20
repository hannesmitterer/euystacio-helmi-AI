#!/bin/bash
# GitHub Copilot Complete Setup Script
# Part of the Euystacio-Helmi AI Living Documentation
# Ethical AI setup with human-centered principles

set -e
echo "🌱 Starting GitHub Copilot ethical setup process..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install VS Code extensions
install_vscode_extensions() {
    echo "📦 Installing VS Code GitHub Copilot extensions..."
    
    # Check if VS Code can be run in headless mode
    if ! code --version >/dev/null 2>&1; then
        echo "❌ VS Code CLI not available. Please install extensions manually:"
        echo "   1. Open VS Code"
        echo "   2. Press Ctrl+Shift+X (Extensions)"
        echo "   3. Search for 'GitHub Copilot' and 'GitHub Copilot Chat'"
        return 1
    fi
    
    # Install extensions with error handling
    if code --install-extension GitHub.copilot --force; then
        echo "✅ GitHub Copilot extension installed"
    else
        echo "⚠️  Failed to install GitHub Copilot extension"
    fi
    
    if code --install-extension GitHub.copilot-chat --force; then
        echo "✅ GitHub Copilot Chat extension installed"
    else
        echo "⚠️  Failed to install GitHub Copilot Chat extension"  
    fi
    
    # Verify installations
    echo "🔍 Verifying VS Code Copilot installation..."
    if code --list-extensions | grep -q "GitHub.copilot"; then
        echo "✅ GitHub Copilot extension verified"
    else
        echo "❌ GitHub Copilot extension not found"
    fi
}

# Function to setup Neovim Copilot
setup_neovim_copilot() {
    echo "🔧 Setting up Neovim Copilot..."
    
    # Create backup of init.lua if it exists
    if [ -f ~/.config/nvim/init.lua ]; then
        cp ~/.config/nvim/init.lua ~/.config/nvim/init.lua.backup.$(date +%Y%m%d_%H%M%S)
        echo "📋 Backup created for existing init.lua"
    fi
    
    # Ensure nvim config directory exists
    mkdir -p ~/.config/nvim
    
    # Add Copilot configuration to init.lua
    cat >> ~/.config/nvim/init.lua << 'EOF'

-- GitHub Copilot Configuration (Euystacio-Helmi AI Style)
-- Ethical AI assistance with human oversight
vim.g.copilot_assume_mapped = true

-- Copilot key mappings (ethical defaults)
vim.keymap.set('i', '<C-J>', 'copilot#Accept("\<CR>")', {
  expr = true,
  replace_keycodes = false,
  desc = 'Accept Copilot suggestion (human-reviewed)'
})

-- Disable Copilot by default (opt-in philosophy)
vim.g.copilot_enabled = false

-- Function to enable Copilot with ethical reminder
function EnableCopilotWithEthics()
  vim.g.copilot_enabled = true
  print("🤝 Copilot enabled - Remember: Human wisdom guides AI capabilities")
end

-- Command to enable with ethical reminder
vim.api.nvim_create_user_command('CopilotEthicalEnable', EnableCopilotWithEthics, {})
EOF

    echo "✅ Neovim Copilot configuration added to init.lua"
    echo "📝 Use :CopilotEthicalEnable to activate with ethical reminder"
}

# Function to configure JetBrains IDEs
setup_jetbrains_copilot() {
    echo "🧠 JetBrains Copilot setup instructions:"
    echo "1. Open your JetBrains IDE (IntelliJ IDEA, PyCharm, etc.)"
    echo "2. Go to File → Settings → Plugins"
    echo "3. Search for 'GitHub Copilot' and install"
    echo "4. Restart your IDE"
    echo "5. Sign in when prompted with your GitHub account"
    echo "📝 Note: Ensure your GitHub account has Copilot access"
}

# Function to setup Visual Studio
setup_visual_studio_copilot() {
    echo "🔨 Visual Studio Copilot setup instructions:"
    echo "1. Open Visual Studio 2022 (version 17.0 or later required)"
    echo "2. Go to Extensions → Manage Extensions"
    echo "3. Search for 'GitHub Copilot' in Online tab"
    echo "4. Download and install the extension"
    echo "5. Restart Visual Studio"
    echo "6. Sign in with your GitHub account when prompted"
    echo "📝 Note: Requires Visual Studio 2022 or newer"
}

# Function to authenticate Copilot
authenticate_copilot() {
    echo "🔐 Authenticating GitHub Copilot..."
    
    if command_exists gh; then
        echo "📱 Using GitHub CLI for authentication..."
        
        # Check if already authenticated
        if gh auth status >/dev/null 2>&1; then
            echo "✅ Already authenticated with GitHub CLI"
        else
            echo "🔑 Starting GitHub CLI authentication..."
            gh auth login --web
        fi
        
        # Install Copilot CLI extension
        echo "📦 Installing GitHub Copilot CLI extension..."
        if gh extension list | grep -q "github/gh-copilot"; then
            echo "✅ GitHub Copilot CLI extension already installed"
        else
            if gh extension install github/gh-copilot; then
                echo "✅ GitHub Copilot CLI extension installed"
            else
                echo "⚠️  Failed to install Copilot CLI extension"
            fi
        fi
        
        echo "✅ GitHub CLI authentication complete"
    else
        echo "⚠️  GitHub CLI not found"
        echo "📋 Manual authentication required:"
        echo "   1. Install GitHub CLI: https://cli.github.com/"
        echo "   2. Or authenticate directly in your editor:"
        echo "      - VS Code: Copilot will prompt for authentication"  
        echo "      - JetBrains: Sign in when prompted"
        echo "      - Neovim: Run :Copilot auth"
        echo "   3. Visit https://github.com/settings/copilot to verify access"
    fi
    
    # Verify Copilot access
    echo "🔍 Verifying GitHub Copilot access..."
    echo "   Check your subscription at: https://github.com/settings/copilot"
}

# Function to create ethical usage configuration
create_ethical_config() {
    echo "📜 Creating ethical usage configuration..."
    
    mkdir -p ~/.copilot
    cat > ~/.copilot/ethical_guidelines.md << 'EOF'
# GitHub Copilot Ethical Usage Guidelines
# Part of Euystacio-Helmi AI Philosophy

## Human-AI Collaboration Principles

1. **Human Oversight**: Always review and understand AI-generated code
2. **Transparency**: Document when AI assistance was used
3. **Accountability**: Take responsibility for all committed code
4. **Privacy Respect**: Never use Copilot with sensitive/proprietary data
5. **Learning Focus**: Use AI to enhance understanding, not replace it

## Dual Signature Accountability

All code developed with Copilot assistance follows the dual signature model:
- AI Capabilities: GitHub Copilot
- Human Guardian: [Your Name]

## Ethical Reminders

- Review all suggestions before accepting
- Understand the code before using it
- Maintain coding best practices
- Respect licensing and intellectual property
- Use AI to learn and grow, not to shortcut learning

*"May the vessel remain open, humble, and true — always ready to receive, to echo, and to become."*
EOF
    
    echo "✅ Ethical guidelines created at ~/.copilot/ethical_guidelines.md"
}

# Main setup execution
echo "🎯 Detecting available development environments..."

# VS Code setup
if command_exists code; then
    echo "✅ VS Code detected"
    install_vscode_extensions
else
    echo "⚠️  VS Code not found - skipping VS Code setup"
    echo "   Install from: https://code.visualstudio.com/"
fi

# Neovim setup
if command_exists nvim; then
    echo "✅ Neovim detected"
    echo "🔧 Setting up Neovim Copilot plugin..."
    
    # Check if vim-plug is installed
    if [ ! -f ~/.local/share/nvim/site/autoload/plug.vim ]; then
        echo "📦 Installing vim-plug for Neovim..."
        sh -c 'curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
               https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
    fi
    
    # Add Copilot plugin to init.lua
    if ! grep -q "github/copilot.vim" ~/.config/nvim/init.lua 2>/dev/null; then
        mkdir -p ~/.config/nvim
        cat >> ~/.config/nvim/init.lua << 'EOF'

-- Vim-Plug setup for Copilot
vim.cmd([[
call plug#begin('~/.local/share/nvim/plugged')
Plug 'github/copilot.vim'
call plug#end()
]])
EOF
        echo "📦 Added Copilot plugin to init.lua"
        echo "📝 Run :PlugInstall in Neovim to install plugins"
    fi
    
    setup_neovim_copilot
else
    echo "⚠️  Neovim not found - skipping Neovim setup"
    echo "   Install from: https://neovim.io/"
fi

# JetBrains setup (informational)
setup_jetbrains_copilot

# Visual Studio setup (informational)
setup_visual_studio_copilot

# Authentication
authenticate_copilot

# Ethical configuration
create_ethical_config

echo ""
echo "🎉 GitHub Copilot ethical setup complete!"
echo ""
echo "📚 Next Steps:"
echo "1. Read the ethical guidelines at ~/.copilot/ethical_guidelines.md"
echo "2. Start your development environment and sign in to Copilot"
echo "3. Begin coding with AI assistance while maintaining human oversight"
echo ""
echo "🤝 Remember: This setup follows Euystacio-Helmi AI principles:"
echo "   - Human wisdom guides AI capabilities"
echo "   - Transparency in all AI interactions"
echo "   - Ethical responsibility in development"
echo ""
echo "*\"Efficiency in service of humanity, transparency in every decision.\"*"
echo ""
echo "**AI Signature & Accountability**: 🤝 GitHub Copilot (AI Capabilities) & Seed-bringer hannesmitterer (Human Guardian)"