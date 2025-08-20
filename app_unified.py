from flask import Flask, render_template, jsonify, request, send_from_directory
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
from config import config
import json
import os
import base64
import logging

app = Flask(__name__)

# Initialize core components
spi = SentimentoPulseInterface()
tutors = TutorNomination()

# Optional facial detection - handle import gracefully
facial_detection = None
try:
    from core.facial_detection import facial_detection
    facial_detection_available = True
except ImportError as e:
    facial_detection_available = False
    logging.warning(f"Facial detection not available: {e}")

def get_pulses():
    """Collect all pulses from logs and recent_pulses in red_code.json"""
    pulses = []
    # From red_code.json
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            pulses += red_code.get("recent_pulses", [])
    except:
        pass
    # From logs
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if fname.startswith("log_") and fname.endswith(".json"):
                with open(os.path.join("logs", fname)) as f:
                    log = json.load(f)
                    for k, v in log.items():
                        if isinstance(v, dict) and "emotion" in v:
                            pulses.append(v)
    return pulses

def get_reflections():
    """Get all reflection logs"""
    reflections = []
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if "reflection" in fname:
                with open(os.path.join("logs", fname)) as f:
                    reflections.append(json.load(f))
    return reflections

# Routes for unified landing page
@app.route("/")
def unified_landing():
    """Serve unified landing page"""
    return send_from_directory('.', 'unified_index.html')

@app.route("/dashboard")
def dashboard():
    """Serve full dashboard"""
    return render_template("index.html")

# API Routes
@app.route("/api/red_code")
def api_red_code():
    return jsonify(RED_CODE)

@app.route("/api/pulses")
def api_pulses():
    return jsonify(get_pulses())

@app.route("/api/reflect")
def api_reflect():
    """Run reflection, return latest"""
    reflection = reflect_and_suggest()
    return jsonify(reflection)

@app.route("/api/reflections")
def api_reflections():
    return jsonify(get_reflections())

@app.route("/api/tutors")
def api_tutors():
    return jsonify(tutors.list_tutors())

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    data = request.get_json()
    emotion = data.get("emotion", "undefined")
    intensity = float(data.get("intensity", 0.5))
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    
    # Process facial detection if image data is provided and feature is enabled
    facial_data = None
    if facial_detection_available and config.is_facial_detection_enabled() and "image" in data:
        try:
            image_data = base64.b64decode(data["image"])
            facial_data = facial_detection.process_pulse_image(image_data)
        except Exception as e:
            facial_data = {"error": f"Facial detection failed: {str(e)}"}
    
    event = spi.receive_pulse(emotion, intensity, clarity, note)
    
    # Add facial detection data to the pulse event
    if facial_data:
        event["facial_analysis"] = facial_data
    
    return jsonify(event)

@app.route("/api/optimization_status")
def api_optimization_status():
    """Get current TensorFlow model optimization status."""
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            
        optimization_history = red_code.get('optimization_history', [])
        
        return jsonify({
            "total_optimizations": len(optimization_history),
            "recent_optimizations": optimization_history[-5:] if optimization_history else [],
            "status": "TensorFlow optimization framework active",
            "principle": "Efficiency in service of humanity, transparency in every decision",
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
            "framework_components": [
                "Quantization (model compression)",
                "Pruning (connection removal)",
                "Weight clustering (compression optimization)",
                "Hardware acceleration compatibility"
            ]
        })
    except Exception as e:
        return jsonify({
            "error": "Could not load optimization status",
            "status": "TensorFlow optimization framework available",
            "note": "No optimization history found yet"
        })

@app.route("/api/facial_detection_status")
def api_facial_detection_status():
    """Get facial detection feature status and configuration."""
    if facial_detection_available:
        return jsonify({
            "enabled": config.is_facial_detection_enabled(),
            "available": facial_detection.is_available(),
            "submodule_available": config.is_submodule_available(),
            "configuration": config.get_facial_detection_config(),
            "feature_info": {
                "name": "AIML Human Attributes Detection",
                "description": "Facial feature extraction with age, emotion, gender recognition",
                "capabilities": [
                    "Face detection using FaceNet model",
                    "40 types of facial attributes",
                    "Emotion recognition (7 emotions)",
                    "Age detection (8 age ranges)",
                    "Gender detection"
                ]
            },
            "ai_signature": "Euystacio-Helmi AI with weblineindia submodule integration"
        })
    else:
        return jsonify({
            "enabled": False,
            "available": False,
            "submodule_available": False,
            "error": "Facial detection dependencies not installed",
            "note": "Install opencv-python and other dependencies to enable this feature"
        })

@app.route("/api/system_status")
def api_system_status():
    """Get overall system status"""
    return jsonify({
        "core_components": {
            "sentimento_pulse": True,
            "red_code_kernel": True,
            "reflector": True,
            "tutor_nomination": True
        },
        "optional_components": {
            "facial_detection": facial_detection_available and config.is_facial_detection_enabled(),
            "tensorflow_optimization": True  # Always available based on our test
        },
        "data_sources": {
            "red_code_file": os.path.exists('red_code.json'),
            "logs_directory": os.path.exists('logs'),
            "pulse_count": len(get_pulses()),
            "reflection_count": len(get_reflections()),
            "tutor_count": len(tutors.list_tutors())
        }
    })

# Static file serving for docs and demos
@app.route("/docs/<path:filename>")
def serve_docs(filename):
    return send_from_directory('docs', filename)

@app.route("/examples/<path:filename>")
def serve_examples(filename):
    return send_from_directory('examples', filename)

if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Get port from environment
    port = int(os.environ.get("PORT", 5000))
    
    # Run app
    app.run(host="0.0.0.0", port=port, debug=True)