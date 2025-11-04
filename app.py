from flask import Flask, render_template, jsonify, request
from sentimento_pulse_interface import SentimentoPulseInterface
from red_code import RED_CODE, ensure_red_code  # changed: top-level module
from reflector import reflect_and_suggest      # changed: top-level module
from tutor_nomination import TutorNomination   # changed: top-level module
import json
import os

app = Flask(__name__)

# Ensure minimal state exists
ensure_red_code()  # creates red_code.json from RED_CODE if missing
os.makedirs("logs", exist_ok=True)

spi = SentimentoPulseInterface()
tutors = TutorNomination()

def get_pulses():
    # Collect all pulses from red_code.json and logs
    pulses = []
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            pulses += red_code.get("recent_pulses", [])
    except Exception:
        # If red_code.json missing or malformed, return empty list (already ensured above)
        pass

    # From logs
    try:
        for fname in sorted(os.listdir("logs")):
            if fname.startswith("log_") and fname.endswith(".json"):
                with open(os.path.join("logs", fname)) as f:
                    log = json.load(f)
                    for k, v in log.items():
                        if isinstance(v, dict) and ("emotion" in v or "feeling" in v):
                            pulses.append(v)
    except FileNotFoundError:
        # logs directory may be empty
        pass
    return pulses

def get_reflections():
    reflections = []
    try:
        for fname in sorted(os.listdir("logs")):
            if "reflection" in fname:
                with open(os.path.join("logs", fname)) as f:
                    reflections.append(json.load(f))
    except FileNotFoundError:
        pass
    return reflections

@app.route("/")
def index():
    # serve the static index in templates/ or the public/ index.html
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
    data = request.get_json() or {}
    emotion = data.get("emotion", data.get("feeling", "undefined"))
    try:
        intensity = float(data.get("intensity", 0.5))
    except (TypeError, ValueError):
        intensity = 0.5
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    event = spi.receive_pulse(emotion, intensity, clarity, note)
    return jsonify(event)

if __name__ == "__main__":
    # local dev: ensure directories and run
    os.makedirs("logs", exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("FLASK_PORT", 5000)))
