from flask import Flask, render_template, jsonify, request
from sentimento_pulse_interface import SentimentoPulseInterface
from red_code import RED_CODE, ensure_red_code  # changed: top-level module
from reflector import reflect_and_suggest      # changed: top-level module
from tutor_nomination import TutorNomination   # changed: top-level module
from blacklist import blacklist, ensure_blacklist  # Permanent blacklist system
import json
import os

app = Flask(__name__)

# Ensure minimal state exists
ensure_red_code()  # creates red_code.json from RED_CODE if missing
ensure_blacklist()  # creates blacklist.json for security protection
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
                    # Handle JSONL format (one JSON object per line)
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                reflections.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
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

# Blacklist API endpoints for security management
@app.route("/api/blacklist", methods=["GET"])
def api_blacklist_list():
    """List all blocked entities with optional filtering."""
    entity_type = request.args.get("entity_type")
    severity = request.args.get("severity")
    entities = blacklist.list_blocked_entities(entity_type=entity_type, severity=severity)
    return jsonify({
        "blocked_entities": entities,
        "statistics": blacklist.get_statistics()
    })

@app.route("/api/blacklist/check/<entity_id>", methods=["GET"])
def api_blacklist_check(entity_id):
    """Check if an entity is blocked."""
    is_blocked = blacklist.is_blocked(entity_id)
    entity = blacklist.get_entity(entity_id) if is_blocked else None
    return jsonify({
        "entity_id": entity_id,
        "is_blocked": is_blocked,
        "entity": entity
    })

@app.route("/api/blacklist/add", methods=["POST"])
def api_blacklist_add():
    """Add an entity to the blacklist."""
    data = request.get_json() or {}
    entity_id = data.get("entity_id")
    entity_type = data.get("entity_type", "unknown")
    reason = data.get("reason", "Security threat")
    severity = data.get("severity", "high")
    metadata = data.get("metadata", {})
    
    if not entity_id:
        return jsonify({"error": "entity_id is required"}), 400
    
    success = blacklist.add_entity(entity_id, entity_type, reason, severity, metadata)
    
    if success:
        return jsonify({
            "success": True,
            "message": f"Entity {entity_id} added to blacklist",
            "entity_id": entity_id
        })
    else:
        return jsonify({
            "success": False,
            "message": f"Entity {entity_id} already blocked or error occurred"
        }), 400

@app.route("/api/blacklist/remove/<entity_id>", methods=["DELETE"])
def api_blacklist_remove(entity_id):
    """Remove an entity from the blacklist."""
    success = blacklist.remove_entity(entity_id)
    
    if success:
        return jsonify({
            "success": True,
            "message": f"Entity {entity_id} removed from blacklist"
        })
    else:
        return jsonify({
            "success": False,
            "message": f"Entity {entity_id} not found in blacklist"
        }), 404

@app.route("/api/blacklist/statistics", methods=["GET"])
def api_blacklist_statistics():
    """Get blacklist statistics."""
    return jsonify(blacklist.get_statistics())

if __name__ == "__main__":
    # local dev: ensure directories and run
    os.makedirs("logs", exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("FLASK_PORT", 5000)))
