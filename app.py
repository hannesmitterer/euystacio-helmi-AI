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

@app.route("/submit_tutor_rhythm", methods=["POST"])
def submit_tutor_rhythm():
    """Endpoint for tutor rhythm submissions"""
    try:
        data = request.get_json()
        tutor_name = data.get("tutor_name", "").strip()
        intention = data.get("intention", "").strip()
        offering = data.get("offering", "").strip()
        
        # Validate required fields
        if not tutor_name or not intention or not offering:
            return jsonify({
                "error": "Missing required fields: tutor_name, intention, and offering are all required"
            }), 400
        
        # Process through the sentimento pulse interface
        event = spi.receive_tutor_rhythm(tutor_name, intention, offering)
        
        return jsonify({
            "success": True,
            "message": "Tutor rhythm received and logged",
            "event": event
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to process tutor rhythm: {str(e)}"
        }), 500

@app.route("/tutor-log")
def tutor_log():
    """Display tutor rhythm log"""
    try:
        # Read the markdown log file
        if os.path.exists("tutor_pulse_log.md"):
            with open("tutor_pulse_log.md", "r") as f:
                log_content = f.read()
        else:
            log_content = "# Tutor Pulse Log\n\nNo submissions yet. Join the living pulse!"
        
        # Also get JSON logs for API access
        json_logs = []
        if os.path.exists("logs"):
            for fname in os.listdir("logs"):
                if fname.startswith("tutor_rhythm_") and fname.endswith(".json"):
                    with open(os.path.join("logs", fname)) as f:
                        try:
                            daily_logs = json.load(f)
                            json_logs.extend(daily_logs)
                        except:
                            pass
        
        return render_template("tutor_log.html", log_content=log_content, json_logs=json_logs)
        
    except Exception as e:
        return f"Error loading tutor log: {str(e)}", 500

@app.route("/api/tutor-rhythms")
def api_tutor_rhythms():
    """API endpoint to get all tutor rhythms as JSON"""
    json_logs = []
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if fname.startswith("tutor_rhythm_") and fname.endswith(".json"):
                with open(os.path.join("logs", fname)) as f:
                    try:
                        daily_logs = json.load(f)
                        json_logs.extend(daily_logs)
                    except:
                        pass
    return jsonify(json_logs)

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    app.run(debug=True)
