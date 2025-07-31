from flask import Flask, render_template, jsonify, request
from sentimento_pulse_interface import SentimentoPulseInterface
from core.red_code import RED_CODE
from core.reflector import reflect_and_suggest
from tutor_nomination import TutorNomination
import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

try:
    spi = SentimentoPulseInterface()
    tutors = TutorNomination()
    logger.info("Application components initialized successfully")
except Exception as e:
    logger.error(f"Error initializing application components: {e}")
    raise

def get_pulses():
    """Collect all pulses from logs and recent_pulses in red_code.json"""
    pulses = []
    
    # From red_code.json
    try:
        red_code_path = os.path.join(os.path.dirname(__file__), 'red_code.json')
        with open(red_code_path, 'r') as f:
            red_code = json.load(f)
            pulses.extend(red_code.get("recent_pulses", []))
        logger.debug(f"Loaded {len(pulses)} pulses from red_code.json")
    except FileNotFoundError:
        logger.warning("red_code.json not found")
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing red_code.json: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading red_code.json: {e}")
    
    # From logs directory
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    if os.path.exists(logs_dir):
        try:
            for fname in sorted(os.listdir(logs_dir)):
                if fname.startswith("log_") and fname.endswith(".json"):
                    try:
                        with open(os.path.join(logs_dir, fname), 'r') as f:
                            log = json.load(f)
                            for k, v in log.items():
                                if isinstance(v, dict) and "emotion" in v:
                                    pulses.append(v)
                    except (json.JSONDecodeError, IOError) as e:
                        logger.warning(f"Error reading log file {fname}: {e}")
        except OSError as e:
            logger.error(f"Error accessing logs directory: {e}")
    
    logger.debug(f"Total pulses collected: {len(pulses)}")
    return pulses

def get_reflections():
    """Get all reflection files from logs directory"""
    reflections = []
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    
    if not os.path.exists(logs_dir):
        logger.warning("Logs directory does not exist")
        return reflections
    
    try:
        for fname in sorted(os.listdir(logs_dir)):
            if "reflection" in fname and fname.endswith(".json"):
                try:
                    with open(os.path.join(logs_dir, fname), 'r') as f:
                        reflection = json.load(f)
                        reflections.append(reflection)
                except (json.JSONDecodeError, IOError) as e:
                    logger.warning(f"Error reading reflection file {fname}: {e}")
    except OSError as e:
        logger.error(f"Error accessing logs directory: {e}")
    
    logger.debug(f"Total reflections collected: {len(reflections)}")
    return reflections

@app.route("/")
def index():
    """Serve the main page"""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Error rendering index page: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/red_code")
def api_red_code():
    """API endpoint for red code data"""
    try:
        return jsonify(RED_CODE)
    except Exception as e:
        logger.error(f"Error serving red code: {e}")
        return jsonify({"error": "Failed to load red code"}), 500

@app.route("/api/pulses")
def api_pulses():
    """API endpoint for pulse data"""
    try:
        pulses = get_pulses()
        return jsonify(pulses)
    except Exception as e:
        logger.error(f"Error serving pulses: {e}")
        return jsonify({"error": "Failed to load pulses"}), 500

@app.route("/api/reflect")
def api_reflect():
    """API endpoint for reflection data"""
    try:
        reflection = reflect_and_suggest()
        return jsonify(reflection)
    except Exception as e:
        logger.error(f"Error generating reflection: {e}")
        return jsonify({"error": "Failed to generate reflection"}), 500

@app.route("/api/reflections")
def api_reflections():
    """API endpoint for all reflections"""
    try:
        reflections = get_reflections()
        return jsonify(reflections)
    except Exception as e:
        logger.error(f"Error serving reflections: {e}")
        return jsonify({"error": "Failed to load reflections"}), 500

@app.route("/api/tutors")
def api_tutors():
    """API endpoint for tutor nominations"""
    try:
        tutor_data = tutors.nominate_tutors()
        return jsonify(tutor_data)
    except Exception as e:
        logger.error(f"Error serving tutors: {e}")
        return jsonify({"error": "Failed to load tutors"}), 500

@app.route("/api/pulse", methods=["POST"])
def api_pulse():
    """API endpoint for receiving pulses"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        emotion = data.get("emotion", "undefined")
        intensity = float(data.get("intensity", 0.5))
        clarity = data.get("clarity", "medium")
        note = data.get("note", "")
        
        # Validate intensity range
        if not 0 <= intensity <= 1:
            return jsonify({"error": "Intensity must be between 0 and 1"}), 400
        
        event = spi.receive_pulse(emotion, intensity, clarity, note)
        logger.info(f"Pulse received: {emotion} (intensity: {intensity})")
        
        return jsonify(event)
    except ValueError as e:
        logger.warning(f"Invalid pulse data: {e}")
        return jsonify({"error": "Invalid intensity value"}), 400
    except Exception as e:
        logger.error(f"Error processing pulse: {e}")
        return jsonify({"error": "Failed to process pulse"}), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.url}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    logger.info("Starting Euystacio application")
    app.run(debug=True, host='0.0.0.0', port=5000)
