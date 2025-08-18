from flask import Flask, render_template, jsonify, request
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
import json
import os

# Import cognitive modeling integration (opt-in)
try:
    from cognitive_modeling.unified_api import UnifiedCognitiveAPI
    cognitive_api = UnifiedCognitiveAPI()
    COGNITIVE_MODELING_AVAILABLE = True
except ImportError as e:
    cognitive_api = None
    COGNITIVE_MODELING_AVAILABLE = False
    print(f"Cognitive modeling not available: {e}")

app = Flask(__name__)

spi = SentimentoPulseInterface()
tutors = TutorNomination()

def get_pulses():
    # Collect all pulses from logs and recent_pulses in red_code.json
    pulses = []
    # From red_code.json
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            pulses += red_code.get("recent_pulses", [])
    except:
        pass
    # From logs
    for fname in sorted(os.listdir("logs")):
        if fname.startswith("log_") and fname.endswith(".json"):
            with open(os.path.join("logs", fname)) as f:
                log = json.load(f)
                for k, v in log.items():
                    if isinstance(v, dict) and "emotion" in v:
                        pulses.append(v)
    return pulses

def get_reflections():
    reflections = []
    for fname in sorted(os.listdir("logs")):
        if "reflection" in fname:
            with open(os.path.join("logs", fname)) as f:
                reflections.append(json.load(f))
    return reflections

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/red_code")
def api_red_code():
    return jsonify(RED_CODE)

@app.route("/api/pulses")
def api_pulses():
    return jsonify(get_pulses())

@app.route("/api/reflect")
def api_reflect():
    # Run reflection, return latest
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
    event = spi.receive_pulse(emotion, intensity, clarity, note)
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

# Cognitive Modeling API Endpoints (opt-in)
@app.route("/api/cognitive/status")
def api_cognitive_status():
    """Get cognitive modeling system status"""
    if not COGNITIVE_MODELING_AVAILABLE or not cognitive_api:
        return jsonify({
            "available": False,
            "message": "Cognitive modeling integration not available",
            "note": "This is an opt-in feature that extends Euystacio's capabilities"
        })
    
    return jsonify(cognitive_api.get_system_status())

@app.route("/api/cognitive/reflection", methods=["POST"])
def api_cognitive_reflection():
    """Enhanced reflection using cognitive modeling"""
    if not COGNITIVE_MODELING_AVAILABLE or not cognitive_api:
        # Fall back to basic reflection
        basic_reflection = reflect_and_suggest()
        basic_reflection["note"] = "Using basic reflection - cognitive modeling not available"
        return jsonify(basic_reflection)
    
    data = request.get_json() or {}
    try:
        enhanced_reflection = cognitive_api.enhanced_reflection(data)
        return jsonify(enhanced_reflection)
    except Exception as e:
        # Fall back to basic reflection on error
        basic_reflection = reflect_and_suggest()
        basic_reflection["error"] = str(e)
        basic_reflection["note"] = "Fell back to basic reflection due to error"
        return jsonify(basic_reflection)

@app.route("/api/cognitive/sentiment", methods=["POST"])
def api_cognitive_sentiment():
    """Enhanced sentiment reflection using cognitive modeling"""
    if not COGNITIVE_MODELING_AVAILABLE or not cognitive_api:
        return jsonify({
            "error": "Cognitive modeling not available",
            "message": "This feature requires cognitive modeling to be enabled"
        })
    
    data = request.get_json() or {}
    return jsonify(cognitive_api.sentiment_reflection_api(data))

@app.route("/api/cognitive/environment")
def api_cognitive_environment():
    """Environmental rhythm sensing API"""
    if not COGNITIVE_MODELING_AVAILABLE or not cognitive_api:
        return jsonify({
            "error": "World modeling not available", 
            "message": "This feature requires world modeling to be enabled"
        })
    
    return jsonify(cognitive_api.environmental_rhythm_api())

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
