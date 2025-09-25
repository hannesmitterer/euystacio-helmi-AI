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

# Initialize core components (placeholders for your custom logic)
# You will need to create these files and classes yourself.
class SentimentoPulseInterface:
    def receive_pulse(self, emotion, intensity, clarity, note):
        print(f"Received pulse: {emotion}, {intensity}, {clarity}, {note}")
        # Placeholder logic for updating kernel state
        return {"kernel_state": {"trust": 0.95, "harmony": 0.98}, "event_log": "Pulse processed successfully."}

class RED_CODE:
    pass

def reflect_and_suggest():
    # Placeholder logic
    return {"state": {"trust": 1.0, "harmony": 1.0}, "reflection": "The kernel is in a state of perfect balance."}

class TutorNomination:
    def list_tutors(self):
        return ["Tutor A", "Tutor B"]

class config:
    @staticmethod
    def is_facial_detection_enabled():
        return False

# You need to create a 'red_code.json' file with a JSON object inside.
# For example: {"recent_pulses": []}
# You also need to create a 'logs' directory.

# Optional facial detection - handle import gracefully
facial_detection = None
try:
    from core.facial_detection import facial_detection
    facial_detection_available = True
except ImportError as e:
    facial_detection_available = False
    logging.warning(f"Facial detection not available: {e}")

spi = SentimentoPulseInterface()
tutors = TutorNomination()

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

@app.route("/")
def index():
    """Serve unified landing page"""
    return send_from_directory('.', 'index.html')

@app.route("/dashboard")
def dashboard():
    """Serve full dashboard"""
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

@app.route("/api/pulse", methods=["POST"])\ndef api_pulse():
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
        event["facial_data"] = facial_data
    return jsonify(event)

if __name__ == "__main__":
    app.run(debug=True)