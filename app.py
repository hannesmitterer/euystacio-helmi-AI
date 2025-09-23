from flask import Flask, render_template, jsonify, request, send_from_directory
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from core.euystacio_core import euystacio_kernel
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
    """Collect all pulses from logs, red_code.json, and enhanced kernel"""
    pulses = []
    
    # Get pulses from enhanced kernel
    try:
        kernel_state = euystacio_kernel.get_current_state()
        kernel_pulses = kernel_state.get("recent_pulses", [])
        pulses.extend(kernel_pulses)
    except Exception as e:
        print(f"Error getting kernel pulses: {e}")
    
    # From red_code.json (legacy compatibility)
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            legacy_pulses = red_code.get("recent_pulses", [])
            pulses.extend(legacy_pulses)
    except:
        pass
        
    # From logs (legacy compatibility)
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if fname.startswith("log_") and fname.endswith(".json"):
                try:
                    with open(os.path.join("logs", fname)) as f:
                        log = json.load(f)
                        for k, v in log.items():
                            if isinstance(v, dict) and "emotion" in v:
                                pulses.append(v)
                except:
                    continue
    
    # Remove duplicates and sort by timestamp
    unique_pulses = []
    seen_timestamps = set()
    for pulse in pulses:
        timestamp = pulse.get("timestamp")
        if timestamp and timestamp not in seen_timestamps:
            seen_timestamps.add(timestamp)
            unique_pulses.append(pulse)
    
    # Sort by timestamp (most recent first)
    unique_pulses.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return unique_pulses

def get_reflections():
    """Get all reflection logs"""
    reflections = []
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if "reflection" in fname:
                with open(os.path.join("logs", fname)) as f:
                    reflections.append(json.load(f))
    return reflections

@app.route("/")
def index():
    """Serve unified landing page"""
    return send_from_directory('.', 'index.html')

@app.route("/dashboard")
def dashboard():
    """Serve enhanced dashboard"""  
    return send_from_directory('EuystacioDRAFT', 'index.html')

@app.route("/EuystacioDRAFT/")
def euystacio_dashboard():
    """Serve enhanced dashboard from EuystacioDRAFT"""  
    return send_from_directory('EuystacioDRAFT', 'index.html')

@app.route("/api/red_code")
def api_red_code():
    return jsonify(RED_CODE)

@app.route("/api/pulses")
def api_pulses():
    return jsonify(get_pulses())

@app.route("/api/reflect")
def api_reflect():
    # Get enhanced kernel reflection
    kernel_reflection = euystacio_kernel.reflect()
    
    # Get traditional reflection for compatibility
    try:
        traditional_reflection = reflect_and_suggest()
    except:
        traditional_reflection = {"note": "Traditional reflector unavailable"}
    
    # Combine both reflections
    combined_reflection = {
        "kernel_reflection": kernel_reflection,
        "traditional_reflection": traditional_reflection,
        "timestamp": kernel_reflection["timestamp"]
    }
    
    return jsonify(combined_reflection)

@app.route("/api/reflections")
def api_reflections():
    return jsonify(get_reflections())

@app.route("/api/tutors")
def api_tutors():
    return jsonify(tutors.list_tutors())

@app.route("/api/kernel/state")
def api_kernel_state():
    """Get current enhanced kernel state"""
    return jsonify(euystacio_kernel.get_current_state())

@app.route("/api/kernel/evolution")
def api_kernel_evolution():
    """Get evolution data for charts"""
    hours = request.args.get('hours', 24, type=int)
    return jsonify(euystacio_kernel.get_evolution_data_for_charts(hours))

@app.route("/api/kernel/health")
def api_kernel_health():
    """Get kernel health metrics"""
    state = euystacio_kernel.get_current_state()
    return jsonify(state["health_metrics"])

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    data = request.get_json()
    emotion = data.get("emotion", "undefined")
    intensity = float(data.get("intensity", 0.5))
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    context = data.get("context", "")
    
    # Process facial detection if image data is provided and feature is enabled
    facial_data = None
    if facial_detection_available and config.is_facial_detection_enabled() and "image" in data:
        try:
            image_data = base64.b64decode(data["image"])
            facial_data = facial_detection.process_pulse_image(image_data)
        except Exception as e:
            facial_data = {"error": f"Facial detection failed: {str(e)}"}
    
    # Process through enhanced kernel
    kernel_event = euystacio_kernel.receive_pulse(emotion, intensity, context, note, clarity)
    
    # Also process through original interface for compatibility
    spi_event = spi.receive_pulse(emotion, intensity, clarity, note)
    
    # Combine results
    event = {
        **kernel_event,
        "ai_signature_status": spi_event.get("ai_signature_status", "verified"),
        "kernel_evolution": True
    }
    
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
