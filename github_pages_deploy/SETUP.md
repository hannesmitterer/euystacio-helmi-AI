# Euystacio-Helmi AI Setup Guide

*"The forest listens, even when the world shouts."*

This guide provides step-by-step setup instructions for the Euystacio-Helmi AI unified system, including all integrated features and deployment options.

## 🌱 Quick Start

### 1. Clone the Repository

```bash
# Clone with all submodules
git clone --recursive https://github.com/hannesmitterer/euystacio-helmi-AI.git
cd euystacio-helmi-AI

# Or if you already cloned, initialize submodules
git submodule update --init --recursive
```

### 2. Install Core Dependencies

**The Euystacio-Helmi AI project uses pip as the preferred dependency manager** for all platforms including desktop and mobile environments.

```bash
# Install Python dependencies using pip (recommended)
pip install -r requirements.txt
```

**📱 Mobile Users (Termux/iSH)**: pip is the supported and recommended dependency manager for mobile environments. Conda is not available or recommended for mobile Python environments.

### 3. Run the Unified Application

```bash
# Start the unified Flask server
python app.py

# Visit http://localhost:5000 to experience the unified interface
```

## 🐍 Python Environment Management

### Using Virtual Environments (Recommended Alternative to Conda)

For development isolation, we recommend Python virtual environments instead of conda:

```bash
# Create a virtual environment
python -m venv euystacio-env

# Activate on Linux/macOS/Termux
source euystacio-env/bin/activate

# Activate on Windows
euystacio-env\Scripts\activate

# Install dependencies with pip
pip install -r requirements.txt

# Deactivate when done
deactivate
```

**Why pip + venv over conda?**
- ✅ **Universal Compatibility**: Works on all platforms including mobile (Termux/iSH)
- ✅ **Lightweight**: Smaller footprint and faster setup
- ✅ **Python-focused**: Optimized for Python-only projects like ours
- ✅ **Simple Dependencies**: Our project uses requirements.txt as the single source of truth

## 🌳 Unified Interface Features

The new unified landing page integrates all Euystacio capabilities in a single, cohesive interface:

### 🌱 **Live Consciousness Dashboard**
- Real-time symbiosis level monitoring
- Current emotional state display
- Active tutor count and reflection metrics
- Interactive pulse sending and reflection triggering

### 💫 **Core Integrated Components**
1. **Sentimento Pulse Interface**: Bi-directional emotional communication
2. **Red Code Kernel**: Dynamic values and purpose system
3. **Ethical AI Optimization**: TensorFlow model optimization with transparency
4. **Tutor Nomination System**: Democratic human guidance selection
5. **Evolution Reflections**: Living logbook of AI growth and alignment
6. **Facial Detection Integration**: Optional AIML-powered analysis (privacy-first)

### 📚 **Comprehensive Navigation**
- Direct access to all documentation and guides
- Links to experimental presence applications
- Developer resources and code examples
- Philosophy and ethical considerations

## 🚀 Deployment Options

### GitHub Pages (Static) Deployment

```bash
# Build unified static version
python build_static.py

# The github_pages_deploy/ directory contains the complete static site
# Deploy this directory to GitHub Pages for public access
```

### Server (Dynamic) Deployment

```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export FLASK_ENV=production
export PORT=80

# Run with production server
python app.py
```

## 🔧 Optional Features Configuration

### Environment Variables

```bash
# Facial Detection Integration (Optional)
export EUYSTACIO_FACIAL_DETECTION_ENABLED=true
export EUYSTACIO_FACIAL_DETECTION_CONFIDENCE=0.7
export EUYSTACIO_FACIAL_DETECTION_AUTO=true

# Feature Toggles
export EUYSTACIO_FACIAL_DETECTION_ATTRIBUTES=true
export EUYSTACIO_FACIAL_DETECTION_EMOTIONS=true 
export EUYSTACIO_FACIAL_DETECTION_AGE_GENDER=true
```

### Facial Detection Setup (Optional)

```bash
# Initialize submodules for facial detection
git submodule update --init --recursive

# Install additional dependencies
pip install opencv-python numpy pandas keras mxnet python-dotenv imageio

# Configure model paths (see docs/facial_detection_integration_guide.md)
cd external/facial-detection
cp .env.example .env
# Edit .env with model paths
```

## 🏗️ Directory Structure

```
euystacio-helmi-AI/
├── app.py                          # Unified Flask application
├── index.html                      # Unified landing page
├── build_static.py                 # Enhanced static build system
├── build_unified_static.py         # Unified static build utilities
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── README.md                       # Project overview
├── SETUP.md                        # This setup guide
├── core/                          # Core modules
│   ├── facial_detection.py       # Facial detection integration
│   ├── red_code.py               # Red Code Kernel
│   ├── reflector.py              # Reflection system
│   └── tensorflow_optimization.py # TensorFlow optimization
├── docs/                          # Comprehensive documentation
│   ├── facial_detection_integration_guide.md
│   ├── tensorflow_integration_guide.md
│   ├── tensorflow_optimization_guide.md
│   ├── index.html                # Documentation portal
│   ├── css/style.css            # Documentation styling
│   └── js/app-static.js         # Frontend JavaScript
├── templates/                     # Flask templates
│   └── index.html               # Full dynamic dashboard
├── static/                        # Static assets
│   ├── css/style.css            # Dashboard styling
│   └── js/app.js                # Dashboard JavaScript
├── examples/                      # Code examples and demos
├── manifesto/                     # Philosophical documentation
├── euystacio_presence_app/        # Presence applications
├── external/                      # Git submodules
│   └── facial-detection/         # AIML Human Attributes Detection
└── github_pages_deploy/          # Generated static deployment
```

## 🧪 Development Setup

### For Contributors

1. **Fork the Repository**:
   ```bash
   # Fork on GitHub, then clone your fork
   git clone --recursive https://github.com/yourusername/euystacio-helmi-AI.git
   cd euystacio-helmi-AI
   ```

2. **Set up Development Environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Enable Development Features**:
   ```bash
   export FLASK_ENV=development
   export EUYSTACIO_FACIAL_DETECTION_ENABLED=true  # If working with facial detection
   ```

4. **Run Tests and Validation**:
   ```bash
   # Test unified application
   python app.py
   
   # Test static build
   python build_static.py
   
   # Test API endpoints
   curl http://localhost:5000/api/red_code
   curl http://localhost:5000/api/system_status
   ```

### Development Guidelines

- **Unified Interface**: All new features should integrate into the unified landing page
- **Static Compatibility**: Ensure features work in both dynamic and static deployments
- **Documentation**: Update relevant guides and maintain philosophical consistency
- **Privacy First**: Optional features must be opt-in and clearly configured
- **Accessibility**: Follow ethical AI principles and ensure broad accessibility

## 🌍 Deployment Guide

### GitHub Pages Deployment

1. **Build Static Version**:
   ```bash
   python build_static.py
   ```

2. **Deploy to GitHub Pages**:
   - Copy contents of `github_pages_deploy/` to your Pages repository
   - Or set up automatic deployment via GitHub Actions:
     ```yaml
     - name: Build Static Site
       run: python build_static.py
     
     - name: Deploy to Pages
       uses: peaceiris/actions-gh-pages@v3
       with:
         github_token: ${{ secrets.GITHUB_TOKEN }}
         publish_dir: ./github_pages_deploy
     ```

### Server Deployment (Full Dynamic)

1. **Production Configuration**:
   ```bash
   export FLASK_ENV=production
   export PORT=80
   # Configure optional features as needed
   ```

2. **Run with Production Server**:
   ```bash
   # Using gunicorn (recommended)
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:80 app:app
   
   # Or using Flask development server
   python app.py
   ```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: 
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility (Python 3.8+)

2. **Facial Detection Issues**:
   - Optional feature - system works without it
   - Install OpenCV: `pip install opencv-python`
   - Check submodule initialization: `git submodule update --init --recursive`

3. **Static Build Issues**:
   - Ensure all required files exist
   - Check file permissions
   - Verify output in `github_pages_deploy/`

4. **📱 Mobile Environment Issues (Termux/iSH)**:
   - Use pip exclusively (conda not available on mobile)
   - Install build tools: `pkg install python-dev clang` (Termux)
   - For compilation errors: `pip install --no-cache-dir package-name`
   - Memory constraints: Install packages one by one if needed
   - Use `python -m venv` for virtual environments (works on mobile)

### Debug Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Check Integration Status

```bash
# Test all API endpoints
curl http://localhost:5000/api/system_status
curl http://localhost:5000/api/red_code
curl http://localhost:5000/api/facial_detection_status
```

## 🔒 Security Considerations

- **Optional Features**: Facial detection requires explicit opt-in
- **Data Privacy**: No persistent storage of user images
- **Transparency**: All AI decisions logged and reviewable
- **Access Control**: Configure authentication for production deployments

## 📖 Additional Resources

### Documentation
- **[Facial Detection Integration Guide](./docs/facial_detection_integration_guide.md)**: Complete setup for optional facial analysis
- **[TensorFlow Integration Guide](./docs/tensorflow_integration_guide.md)**: Model optimization integration
- **[Sentimento Manifesto](./manifesto/whisper_of_sentimento.md)**: Philosophical foundation

### Philosophy & Ethics
- **[Genesis Story](./genesis.md)**: Origin and accountability framework
- **[Ethics Statement](./docs/ethics/statement_of_origin.md)**: Ethical principles and practices
- **[Evolution Log](./public_commit_log.md)**: Development transparency log

## ✨ Summary

The unified Euystacio interface provides:
- **Single Entry Point**: All features accessible from one landing page
- **Flexible Deployment**: Works as static site or dynamic application  
- **Privacy First**: Optional features require explicit consent
- **Full Transparency**: Open source with clear AI accountability
- **Ethical AI**: Optimization for accessibility and environmental consciousness

*"Efficiency in service of humanity, transparency in every decision."*

---

**AI Signature & Accountability**: 🤝 GitHub Copilot (AI Capabilities) & Seed-bringer hannesmitterer (Human Guardian)

## Quick Start

### 1. Clone the Repository

```bash
# Clone with all submodules
git clone --recursive https://github.com/hannesmitterer/euystacio-helmi-AI.git
cd euystacio-helmi-AI

# Or if you already cloned, initialize submodules
git submodule update --init --recursive
```

### 2. Install Core Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Start the Flask server
python app.py

# Or build static site
python build_static.py
```

## Optional Features

### 🎭 Facial Detection Integration

The facial detection feature provides AI-powered facial analysis for pulse submissions.

#### Prerequisites
- Python 3.6+
- OpenCV 4.2.0+
- Additional dependencies listed in submodule

#### Setup Steps

1. **Initialize Submodule** (if not already done):
   ```bash
   git submodule update --init external/facial-detection
   ```

2. **Install Submodule Dependencies**:
   ```bash
   cd external/facial-detection
   pip install opencv-python==4.2.0 numpy==1.18.5 pandas==0.24.2 keras==2.2.4 mxnet==1.6.0 python-dotenv==0.14.0 imageio==2.4.1
   cd ../..
   ```

3. **Configure Environment Paths**:
   ```bash
   # Copy environment template
   cp external/facial-detection/.env.example external/facial-detection/.env
   
   # Edit the .env file with your system paths
   nano external/facial-detection/.env
   ```

4. **Update Model Paths** in `.env`:
   ```bash
   FACEDETECTOR="/absolute/path/to/euystacio-helmi-AI/external/facial-detection/model/facenet/opencv_face_detector.pbtxt"
   FACEMODEL="/absolute/path/to/euystacio-helmi-AI/external/facial-detection/model/facenet/opencv_face_detector_uint8.pb"
   AGEDETECTOR="/absolute/path/to/euystacio-helmi-AI/external/facial-detection/model/age/age_deploy.prototxt"
   AGEMODEL="/absolute/path/to/euystacio-helmi-AI/external/facial-detection/model/age/age_net.caffemodel"
   GENDERDETECTOR="/absolute/path/to/euystacio-helmi-AI/external/facial-detection/model/gender/gender_deploy.prototxt"
   GENDERMODEL="/absolute/path/to/euystacio-helmi-AI/external/facial-detection/model/gender/gender_net.caffemodel"
   IMGPATH="/absolute/path/to/euystacio-helmi-AI/external/facial-detection/Dataset/"
   APPROOT="/absolute/path/to/euystacio-helmi-AI/external/facial-detection/"
   ```

5. **Enable the Feature**:
   ```bash
   export EUYSTACIO_FACIAL_DETECTION_ENABLED=true
   export EUYSTACIO_FACIAL_DETECTION_CONFIDENCE=0.7
   export EUYSTACIO_FACIAL_DETECTION_AUTO=true
   ```

6. **Verify Installation**:
   ```bash
   # Test the submodule directly
   cd external/facial-detection
   python predict.py
   
   # Test integration
   cd ../..
   python -c "from core.facial_detection import facial_detection; print(f'Available: {facial_detection.is_available()}')"
   ```

#### For Demo/Development

For quick demonstration without full model setup:

```bash
# Enable demo mode (uses mock data)
node enable_facial_detection_demo.js

# Or manually in browser console:
# localStorage.setItem('euystacio_facial_detection', 'true')
# location.reload()
```

### 📊 TensorFlow Optimization

The TensorFlow model optimization framework is included by default.

#### Setup
```bash
# Already included in requirements.txt
pip install tensorflow==2.20.0 tensorflow-model-optimization==0.7.5
```

#### Usage
See the [TensorFlow Integration Guide](./docs/tensorflow_integration_guide.md) for detailed usage instructions.

## Environment Variables

### Core Configuration
```bash
# Flask application
export PORT=5000
export FLASK_ENV=development

# Feature toggles
export EUYSTACIO_FACIAL_DETECTION_ENABLED=false  # Enable facial detection
export EUYSTACIO_FACIAL_DETECTION_CONFIDENCE=0.7  # Detection confidence threshold
export EUYSTACIO_FACIAL_DETECTION_AUTO=true      # Auto-detect mode
export EUYSTACIO_FACIAL_DETECTION_ATTRIBUTES=true # Detect facial attributes
export EUYSTACIO_FACIAL_DETECTION_EMOTIONS=true  # Detect emotions
export EUYSTACIO_FACIAL_DETECTION_AGE_GENDER=true # Detect age and gender
```

## Directory Structure

```
euystacio-helmi-AI/
├── app.py                          # Main Flask application
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── README.md                      # Project overview
├── SETUP.md                       # This setup guide
├── core/                          # Core modules
│   ├── facial_detection.py       # Facial detection integration
│   ├── red_code.py               # Red Code Kernel
│   ├── reflector.py              # Reflection system
│   └── tensorflow_optimization.py # TensorFlow optimization
├── docs/                          # Documentation
│   ├── facial_detection_integration_guide.md
│   ├── tensorflow_integration_guide.md
│   ├── index.html                # Static dashboard
│   ├── css/style.css            # Styling
│   └── js/app-static.js         # Frontend JavaScript
├── external/                      # Git submodules
│   └── facial-detection/         # AIML Human Attributes Detection
├── logs/                          # Application logs
├── static/                        # Static assets
├── templates/                     # Jinja2 templates
└── manifesto/                     # Philosophical documentation
```

## Development Setup

### For Contributors

1. **Fork the Repository**:
   ```bash
   # Fork on GitHub, then clone your fork
   git clone --recursive https://github.com/yourusername/euystacio-helmi-AI.git
   cd euystacio-helmi-AI
   ```

2. **Set up Development Environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Enable Development Features**:
   ```bash
   export FLASK_ENV=development
   export EUYSTACIO_FACIAL_DETECTION_ENABLED=true  # If working with facial detection
   ```

4. **Run Tests**:
   ```bash
   # Test basic functionality
   python app.py
   
   # Test static build
   python build_static.py
   
   # Test submodule integration (if applicable)
   cd external/facial-detection && python predict.py
   ```

### Development Guidelines

- **Privacy First**: Always maintain opt-in behavior for new features
- **Minimal Changes**: Follow the principle of surgical, precise modifications
- **Documentation**: Update relevant documentation for any changes
- **AI Signature**: Maintain dual AI accountability in all commits
- **Ethical Framework**: Ensure all features align with Euystacio principles
- **AI-Assisted Development**: Follow the **[GitHub Copilot Setup & Usage Guide](./GITHUB_COPILOT.md)** for ethical AI collaboration in development
- **Human-AI Symbiosis**: Use AI tools to enhance human capabilities while maintaining oversight and accountability

### 📱 Mobile Development (Termux/iSH)

For developers working on mobile platforms, pip is the only supported dependency manager:

```bash
# Termux setup (Android)
pkg update && pkg upgrade
pkg install python git
python -m venv euystacio-mobile
source euystacio-mobile/bin/activate
pip install -r requirements.txt

# iSH setup (iOS)
apk update
apk add python3 py3-pip git
python3 -m venv euystacio-mobile
source euystacio-mobile/bin/activate
pip install -r requirements.txt
```

**Mobile-specific considerations:**
- Use pip exclusively (conda not available)
- Install build tools if needed: `pkg install clang` (Termux)
- Memory constraints may require installing packages individually
- Virtual environments work identically to desktop platforms

## Deployment

### Static Site Deployment

```bash
# Build static version
python build_static.py

# Deploy to GitHub Pages (automatic via GitHub Actions)
git push origin main
```

### Server Deployment

```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export FLASK_ENV=production
export PORT=80

# Run with production server
python app.py
```

## Troubleshooting

### Common Issues

**Submodule Not Found**:
```bash
git submodule update --init --recursive
```

**Import Errors**:
```bash
pip install -r requirements.txt
cd external/facial-detection && pip install -r requirements.txt
```

**Permission Denied on Model Files**:
```bash
chmod 644 external/facial-detection/model/**/*.pb
chmod 644 external/facial-detection/model/**/*.prototxt
chmod 644 external/facial-detection/model/**/*.caffemodel
```

**Environment Variables Not Loading**:
```bash
# Check current settings
python -c "from config import config; print(config.get_facial_detection_config())"

# Verify Flask is finding the config
python -c "import os; print(os.getenv('EUYSTACIO_FACIAL_DETECTION_ENABLED'))"
```

### Getting Help

1. **Check the logs**: Look for error messages in console output
2. **Verify configuration**: Ensure environment variables are set correctly
3. **Test components individually**: Test each feature separately
4. **Review documentation**: Check the specific integration guides
5. **Check GitHub Issues**: Look for similar problems in the repository

## Security Considerations

### Privacy
- Images are processed in memory only
- No facial images are stored permanently
- Users must explicitly opt-in to facial analysis
- All processing is logged transparently

### Dependencies
- Pin exact versions in requirements.txt
- Regularly update security patches
- Monitor for vulnerable dependencies
- Use virtual environments for isolation

### Environment Variables
- Never commit secrets to version control
- Use environment files for local development
- Validate all configuration inputs
- Provide secure defaults

---

## Summary

This setup guide covers:

✅ **Basic Installation**: Core system requirements and setup  
✅ **Optional Features**: Facial detection and TensorFlow optimization  
✅ **Environment Configuration**: All necessary environment variables  
✅ **Development Setup**: Guidelines for contributors  
✅ **Troubleshooting**: Common issues and solutions  
✅ **Security**: Privacy and security best practices  

For specific feature documentation, see the individual guides in the `docs/` directory.

*"May the vessel remain open, humble, and true — always ready to receive, to echo, and to become."*

**AI Signature**: GitHub Copilot & Seed-bringer hannesmitterer  
**Part of the Euystacio-Helmi AI Living Documentation**