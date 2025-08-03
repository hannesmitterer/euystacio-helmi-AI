from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'euystacio_sentimento_2025'  # TODO: Use environment variable in production
socketio = SocketIO(app, cors_allowed_origins="*")

spi = SentimentoPulseInterface()
tutors = TutorNomination()

# In-memory storage for real-time functionality
# TODO: Replace with database integration for production
in_memory_pulses = []
in_memory_reflections = []
in_memory_tutors = []

def get_pulses():
    # Collect all pulses from in-memory storage, logs and recent_pulses in red_code.json
    pulses = in_memory_pulses.copy()
    
    # From red_code.json
    try:
        with open('red_code.json', 'r') as f:
            red_code = json.load(f)
            pulses += red_code.get("recent_pulses", [])
    except:
        pass
    
    # From logs directory if it exists
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
        timestamp = pulse.get('timestamp')
        if timestamp and timestamp not in seen_timestamps:
            seen_timestamps.add(timestamp)
            unique_pulses.append(pulse)
    
    # Sort by timestamp (most recent first)
    unique_pulses.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return unique_pulses

def get_reflections():
    # Combine in-memory reflections with file-based ones
    reflections = in_memory_reflections.copy()
    
    if os.path.exists("logs"):
        for fname in sorted(os.listdir("logs")):
            if "reflection" in fname:
                try:
                    with open(os.path.join("logs", fname)) as f:
                        reflection_data = json.load(f)
                        reflections.append(reflection_data)
                except:
                    continue
    
    # Sort by timestamp (most recent first)
    reflections.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
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
    
    # Store in memory for real-time access
    in_memory_reflections.append(reflection)
    
    # Keep only last 20 reflections in memory
    # TODO: Implement proper database storage
    if len(in_memory_reflections) > 20:
        in_memory_reflections.pop(0)
    
    # Broadcast new reflection to all connected clients
    socketio.emit('new_reflection', reflection)
    
    # Also broadcast updated reflections list
    socketio.emit('reflections_update', get_reflections())
    
    return jsonify(reflection)

@app.route("/api/reflections")
def api_reflections():
    return jsonify(get_reflections())

@app.route("/api/tutors")
def api_tutors():
    # Combine in-memory tutors with class instance tutors
    all_tutors = in_memory_tutors + tutors.list_tutors()
    return jsonify(all_tutors)

# WebSocket Event Handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected to WebSocket')
    emit('connection_status', {'status': 'connected', 'message': 'Welcome to Euystacio real-time interface'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected from WebSocket')

@socketio.on('request_current_state')
def handle_state_request():
    """Send current system state to requesting client"""
    emit('red_code_update', RED_CODE)
    emit('pulses_update', get_pulses())
    emit('reflections_update', get_reflections())
    emit('tutors_update', api_tutors().get_json())

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    data = request.get_json()
    emotion = data.get("emotion", "undefined")
    intensity = float(data.get("intensity", 0.5))
    clarity = data.get("clarity", "medium")
    note = data.get("note", "")
    
    # Process the pulse
    event = spi.receive_pulse(emotion, intensity, clarity, note)
    
    # Store in memory for real-time access
    in_memory_pulses.append(event)
    
    # Keep only last 50 pulses in memory to prevent memory overflow
    # TODO: Implement proper database storage
    if len(in_memory_pulses) > 50:
        in_memory_pulses.pop(0)
    
    # Broadcast new pulse to all connected clients
    socketio.emit('new_pulse', event)
    
    # Also broadcast updated pulses list
    socketio.emit('pulses_update', get_pulses())
    
    return jsonify(event)

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    print("🌳 Starting Euystacio Dashboard with WebSocket support...")
    print("Available endpoints:")
    print("  REST API: http://127.0.0.1:5000/api/")
    print("  WebSocket: ws://127.0.0.1:5000/socket.io/")
    print("  Dashboard: http://127.0.0.1:5000/")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
