from flask import Flask, render_template, jsonify, request
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
from euystacio_core import Euystacio  # Import the enhanced core
import json
import os

app = Flask(__name__)

# Initialize components
spi = SentimentoPulseInterface()
tutors = TutorNomination()
euystacio = Euystacio()  # Initialize Euystacio instance for echo functionality

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

@app.route("/api/echo")
def api_echo():
    """Get the latest emotional echo response from Euystacio."""
    echo = euystacio.get_last_echo()
    if echo:
        return jsonify(echo)
    else:
        return jsonify({"text": "No echo yet. Send a pulse to start the conversation.", "timestamp": None})

@app.route("/api/documents/readme")
def api_readme():
    """Serve the README.md content."""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content, "filename": "README.md"})
    except FileNotFoundError:
        return jsonify({"error": "README.md not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/documents/manifesto")
def api_manifesto():
    """Serve the Manifesto content."""
    try:
        with open('manifesto/whisper_of_sentimento.md', 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"content": content, "filename": "whisper_of_sentimento.md"})
    except FileNotFoundError:
        return jsonify({"error": "Manifesto not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    """Send a pulse to Euystacio and get an emotional echo response."""
    data = request.get_json()
    emotion = data.get("emotion", "undefined")
    intensity = float(data.get("intensity", 0.5))
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    
    # Send pulse through the original interface
    event = spi.receive_pulse(emotion, intensity, clarity, note)
    
    # Also trigger reflection in the enhanced core for echo generation
    input_event = {
        "type": "pulse",
        "feeling": emotion,
        "intent": "emotional_connection",
        "intensity": intensity,
        "clarity": clarity,
        "note": note
    }
    echo_response = euystacio.reflect(input_event)
    
    # Return both the original event and the echo
    return jsonify({
        "event": event,
        "echo": echo_response,
        "echo_data": euystacio.get_last_echo()
    })

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    app.run(debug=True)
