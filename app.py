from flask import Flask, render_template, jsonify, request
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
import json
import os

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

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    app.run(debug=True)
