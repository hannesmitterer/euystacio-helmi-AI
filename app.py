from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import random
import eventlet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_euystacio_secret_key'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"status": "active"})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"data": random.randint(1,100)})

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    return jsonify({"suggestion": "Keep the Red Code flowing!"})

@socketio.on('connect')
def handle_connect():
    emit('response', {'msg': 'Euystacio Core: Pulse received. How may I serve the Red Code?'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

@socketio.on('message')
def handle_message(data):
    user_message = data.get('text', '')
    ai_response = f"Gemini: Under the Red Code, I acknowledge your message: '{user_message}'. Processing... Standby for deeper coherence."
    emit('response', {'msg': ai_response})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
