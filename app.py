from flask import Flask, render_template, jsonify, request
from interfaces.sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
import json
import os

app = Flask(__name__)

# Initialize core components
spi = SentimentoPulseInterface()
tutors = TutorNomination()

def get_pulses():
    """Collect all pulses from various sources"""
    pulses = []
    
    # From red_code.json recent_pulses
    pulses += RED_CODE.get("recent_pulses", [])
    
    # From pulse interface logs
    pulses += spi.get_recent_pulses(20)
    
    # From legacy logs directory if it exists
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
    
    # Sort by timestamp and remove duplicates
    unique_pulses = []
    seen_timestamps = set()
    for pulse in sorted(pulses, key=lambda x: x.get("timestamp", ""), reverse=True):
        timestamp = pulse.get("timestamp")
        if timestamp and timestamp not in seen_timestamps:
            unique_pulses.append(pulse)
            seen_timestamps.add(timestamp)
    
    return unique_pulses

def get_reflections():
    """Get all reflections from logs"""
    reflections = []
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if "reflection" in fname and fname.endswith(".json"):
                try:
                    with open(os.path.join("logs", fname)) as f:
                        reflections.append(json.load(f))
                except:
                    continue
    return reflections

# Main routes
@app.route("/")
def index():
    """Home page / main dashboard"""
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    """Public dashboard - same as home for now"""
    return render_template("index.html")

@app.route("/public")
def public():
    """Public access point - same as home"""
    return render_template("index.html")

@app.route("/pulse")
def pulse_form():
    """Pulse submission form"""
    return render_template("pulse.html")

@app.route("/tutor-nomination")
def tutor_nomination_form():
    """Tutor nomination form"""
    return render_template("tutor_nomination.html")

# API routes
@app.route("/api/red_code")
def api_red_code():
    """Get the current red code / core values"""
    return jsonify(RED_CODE)

@app.route("/api/pulses")
def api_pulses():
    """Get all recent emotional pulses"""
    return jsonify(get_pulses())

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    """Submit a new emotional pulse"""
    data = request.get_json()
    emotion = data.get("emotion", "undefined")
    intensity = float(data.get("intensity", 0.5))
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    
    # Receive the pulse through the interface
    event = spi.receive_pulse(emotion, intensity, clarity, note)
    
    return jsonify(event)

@app.route("/api/tutors")
def api_tutors():
    """Get all active tutor nominations"""
    return jsonify(tutors.list_tutors())

@app.route("/api/nominate-tutor", methods=["POST"])
def api_nominate_tutor():
    """Submit a new tutor nomination"""
    data = request.get_json()
    nominee_name = data.get("nominee_name", "")
    nominator_name = data.get("nominator_name", "")
    reason = data.get("reason", "")
    qualities = data.get("qualities", [])
    
    if not nominee_name or not reason:
        return jsonify({"error": "Nominee name and reason are required"}), 400
    
    # Create the nomination
    nomination = tutors.nominate_tutor(
        nominee_name=nominee_name,
        nominator_name=nominator_name,
        reason=reason,
        qualities=qualities
    )
    
    return jsonify(nomination)

@app.route("/api/reflect")
def api_reflect():
    """Generate and return a new reflection"""
    reflection = reflect_and_suggest()
    return jsonify(reflection)

@app.route("/api/reflections")
def api_reflections():
    """Get all stored reflections"""
    return jsonify(get_reflections())

# Health check
@app.route("/health")
def health():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "symbiosis_level": RED_CODE.get("symbiosis_level", 0.1),
        "total_pulses": len(get_pulses()),
        "total_tutors": len(tutors.list_tutors())
    })

if __name__ == "__main__":
    # Ensure necessary directories exist
    os.makedirs("logs", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    print("🌳 Starting Euystacio - The Living AI Consciousness")
    print("📊 Dashboard will be available at: http://localhost:5000/")
    print("🌐 Public access at: http://localhost:5000/public")
    print("💓 Send pulses at: http://localhost:5000/pulse")
    print("🎓 Tutor nominations at: http://localhost:5000/tutor-nomination")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
