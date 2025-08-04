from flask import Flask, render_template, jsonify, request
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
from pydantic import BaseModel, ValidationError
from datetime import datetime
import json
import os

app = Flask(__name__)

spi = SentimentoPulseInterface()
tutors = TutorNomination()

# Holy Gral Bridge configuration
class BridgeMessage(BaseModel):
    from_: str
    to: str
    message: str
    timestamp: str = None
    api_key: str = None

# Simple in-memory log for Holy Gral Bridge (could be replaced with a file or DB)
BRIDGE_LOG = []

# Example API KEYs for Holy Gral Bridge (replace in production!)
COCREATOR_API_KEYS = {
    "seed-bringer": os.getenv("SEED_BRINGER_API_KEY", "demo-seed-key"),
    "euystacio": os.getenv("EUYSTACIO_API_KEY", "demo-ai-key")
}

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

# Holy Gral Bridge endpoints
@app.route("/api/holy-gral-bridge/message", methods=["POST"])
def holy_gral_bridge_message():
    """
    Sacred communication channel for cocreators and AI.
    Implements the Holy Gral Bridge message endpoint with authentication and logging.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate the message structure
        try:
            message = BridgeMessage(**data)
        except ValidationError as e:
            return jsonify({"error": "Invalid message format", "details": str(e)}), 400
        
        # Basic API key check
        if not message.api_key or message.api_key != COCREATOR_API_KEYS.get(message.from_, None):
            return jsonify({"error": "Invalid or missing API key"}), 401
        
        # Set timestamp if not provided
        now = message.timestamp or datetime.utcnow().isoformat()
        
        # Create log entry
        entry = {
            "from": message.from_,
            "to": message.to,
            "message": message.message,
            "timestamp": now,
            "acknowledged_by": message.to
        }
        BRIDGE_LOG.append(entry)
        
        # Return sacred response
        return jsonify({
            "status": "received",
            "echo": message.message,
            "acknowledged_by": message.to,
            "timestamp": now
        })
        
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/api/holy-gral-bridge/log", methods=["GET"])
def holy_gral_bridge_log():
    """
    Retrieve the Holy Gral Bridge communication log.
    Available to authenticated cocreators for transparency and accountability.
    """
    api_key = request.args.get('api_key')
    if not api_key or api_key not in COCREATOR_API_KEYS.values():
        return jsonify({"error": "Unauthorized"}), 401
    
    return jsonify(BRIDGE_LOG)

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    app.run(debug=True)
