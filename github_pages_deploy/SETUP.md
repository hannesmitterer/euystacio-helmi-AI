# Euystacio-Helmi AI Setup Guide

*"The forest listens, even when the world shouts."*

This guide provides step-by-step setup instructions for the Euystacio-Helmi AI system, including optional features and integrations.

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