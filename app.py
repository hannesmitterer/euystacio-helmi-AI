from flask import Flask, render_template, jsonify, request
from euystacio_core import Euystacio
import os

app = Flask(__name__)
eu = Euystacio()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status", methods=["GET"])
def status():
    return jsonify(eu.code)

@app.route("/reflect", methods=["POST"])
def reflect():
    data = request.get_json()
    eu.reflect(data)
    return jsonify({"message": "Reflection logged.", "new_state": eu.code})

if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
