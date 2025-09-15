#!/usr/bin/env python3
"""
Euystacio Network Test Harness
Purpose: Local simulation environment for testing the Visual Ledger Dashboard
         and network consensus mechanisms with multiple simulated nodes.
Author: Seedbringer & Council Directive (15-09-2025)
"""

import json
import os
import random
import threading
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, send_from_directory, request

app = Flask(__name__)

# --- Configuration ---
SIMULATED_NODES = [
    "http://node1.euystacio.local:5001",
    "http://node2.euystacio.local:5002", 
    "http://node3.euystacio.local:5003",
    "http://node4.euystacio.local:5004",
    "http://test-node.euystacio.local:5005"
]

LEDGER_PATH = "docs/foundation/sync_ledger.json"
DASHBOARD_SRC = "docs/foundation/ledger_dashboard.html"
DASHBOARD_DST = "docs/transparency/ledger_dashboard.html"

# Global state for simulation
node_states = {}
simulation_running = False
last_sync_time = None

def current_utc_iso():
    """Get current UTC timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

def initialize_node_states():
    """Initialize simulated node states with realistic randomization"""
    global node_states
    node_states = {}
    
    for node in SIMULATED_NODES:
        # Simulate realistic node behavior patterns
        base_consent_chance = 0.85  # 85% likely to consent
        base_deployment_success = 0.90  # 90% deployment success when consenting
        base_redcode_compliance = 0.95  # 95% Red Code compliance when deployed
        
        consent = random.random() < base_consent_chance
        deployed = consent and (random.random() < base_deployment_success)
        red_code_compliant = deployed and (random.random() < base_redcode_compliance)
        
        node_states[node] = {
            "consent": consent,
            "deployed": deployed,
            "red_code_compliant": red_code_compliant,
            "last_sync": current_utc_iso(),
            "uptime": random.randint(3600, 86400),  # 1-24 hours uptime
            "response_time": random.randint(50, 300)  # 50-300ms response time
        }

def read_ledger():
    """Read current ledger from JSON file"""
    try:
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_ledger(ledger):
    """Write ledger to JSON file"""
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)

def log_to_ledger(entry):
    """Add new entry to ledger"""
    ledger = read_ledger()
    ledger.append(entry)
    write_ledger(ledger)
    print(f"[TEST HARNESS] Ledger updated: {entry['node']} - Consent: {entry['consent']}")

def update_dashboard():
    """Copy dashboard to transparency directory"""
    os.makedirs(os.path.dirname(DASHBOARD_DST), exist_ok=True)
    import shutil
    shutil.copy2(DASHBOARD_SRC, DASHBOARD_DST)
    print(f"[TEST HARNESS] Dashboard updated at {DASHBOARD_DST}")

def simulate_consensus_round():
    """Simulate a complete consensus round across all nodes"""
    global last_sync_time
    
    print(f"[TEST HARNESS] Starting consensus round at {current_utc_iso()}")
    timestamp = current_utc_iso()
    
    # Clear existing ledger for fresh simulation round
    write_ledger([])
    
    for node in SIMULATED_NODES:
        # Get or create node state
        if node not in node_states:
            initialize_node_states()
        
        state = node_states[node]
        
        # Simulate some dynamic behavior (nodes can change state)
        if random.random() < 0.1:  # 10% chance of state change
            state["consent"] = random.random() < 0.85
            if not state["consent"]:
                state["deployed"] = False
                state["red_code_compliant"] = False
            elif random.random() < 0.9:
                state["deployed"] = True
                state["red_code_compliant"] = random.random() < 0.95
        
        # Create ledger entry
        entry = {
            "node": node,
            "timestamp": timestamp,
            "consent": state["consent"],
            "deployed": state["deployed"],
            "red_code_compliant": state["red_code_compliant"],
            "response_time_ms": state["response_time"],
            "uptime_seconds": state["uptime"]
        }
        
        log_to_ledger(entry)
        
        # Update state
        state["last_sync"] = timestamp
        state["uptime"] += 30  # Add 30 seconds uptime
        state["response_time"] = random.randint(50, 300)  # Vary response time
    
    # Update dashboard after all nodes processed
    update_dashboard()
    last_sync_time = timestamp
    
    # Generate summary metrics
    generate_summary_metrics()
    
    print(f"[TEST HARNESS] Consensus round complete. {len(SIMULATED_NODES)} nodes processed.")

def generate_summary_metrics():
    """Generate live summary JSON for network pulse metrics"""
    ledger = read_ledger()
    
    if not ledger:
        return
    
    # Calculate metrics
    total_nodes = len(ledger)
    consenting_nodes = sum(1 for entry in ledger if entry.get("consent", False))
    deployed_nodes = sum(1 for entry in ledger if entry.get("deployed", False))
    compliant_nodes = sum(1 for entry in ledger if entry.get("red_code_compliant", False))
    
    avg_response_time = sum(entry.get("response_time_ms", 0) for entry in ledger) / total_nodes if total_nodes > 0 else 0
    
    summary = {
        "timestamp": current_utc_iso(),
        "network_status": "active" if consenting_nodes > 0 else "degraded",
        "total_nodes": total_nodes,
        "consenting_nodes": consenting_nodes,
        "deployed_nodes": deployed_nodes,
        "compliant_nodes": compliant_nodes,
        "consensus_percentage": round((consenting_nodes / total_nodes) * 100, 2) if total_nodes > 0 else 0,
        "deployment_success_rate": round((deployed_nodes / consenting_nodes) * 100, 2) if consenting_nodes > 0 else 0,
        "red_code_compliance_rate": round((compliant_nodes / deployed_nodes) * 100, 2) if deployed_nodes > 0 else 0,
        "avg_response_time_ms": round(avg_response_time, 2),
        "last_sync": last_sync_time,
        "pulse_layer_active": True,
        "transparency_mode": True
    }
    
    # Write summary to API endpoint file
    os.makedirs("docs/api", exist_ok=True)
    with open("docs/api/network_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

def simulation_loop():
    """Background thread for continuous simulation"""
    global simulation_running
    
    while simulation_running:
        simulate_consensus_round()
        time.sleep(30)  # Run consensus every 30 seconds

# --- Flask Routes ---

@app.route("/")
def index():
    """Serve test harness dashboard"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Euystacio Test Harness</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; background: #f5f5f5; }
            .header { background: #2c3e50; color: white; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; }
            .controls { background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .status { background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            button { background: #3498db; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; margin: 0.25rem; }
            button:hover { background: #2980b9; }
            button.danger { background: #e74c3c; }
            button.danger:hover { background: #c0392b; }
            .metric { display: inline-block; margin: 0.5rem 1rem 0.5rem 0; }
            .metric-value { font-size: 1.5rem; font-weight: bold; color: #2c3e50; }
            .metric-label { font-size: 0.9rem; color: #666; }
            pre { background: #f8f9fa; padding: 1rem; border-radius: 4px; overflow: auto; max-height: 300px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌌 Euystacio Network Test Harness</h1>
            <p>Local simulation environment for Visual Ledger Dashboard and consensus testing</p>
        </div>
        
        <div class="controls">
            <h3>Simulation Controls</h3>
            <button onclick="startSimulation()">Start Continuous Simulation</button>
            <button onclick="stopSimulation()" class="danger">Stop Simulation</button>
            <button onclick="runSingleRound()">Run Single Consensus Round</button>
            <button onclick="resetSimulation()">Reset Node States</button>
        </div>
        
        <div class="status">
            <h3>Network Status</h3>
            <div id="metrics">Loading...</div>
        </div>
        
        <div class="status">
            <h3>Quick Links</h3>
            <a href="/ledger" target="_blank">📊 Visual Ledger Dashboard</a> | 
            <a href="/api/ledger" target="_blank">📋 Raw Ledger JSON</a> | 
            <a href="/api/summary" target="_blank">📈 Network Summary</a> |
            <a href="/api/nodes" target="_blank">🖥️ Node States</a>
        </div>
        
        <div class="status">
            <h3>Recent Ledger Entries</h3>
            <pre id="ledger-preview">Loading...</pre>
        </div>
        
        <script>
            async function startSimulation() {
                const response = await fetch('/api/simulation/start', {method: 'POST'});
                const result = await response.json();
                alert(result.message);
                updateStatus();
            }
            
            async function stopSimulation() {
                const response = await fetch('/api/simulation/stop', {method: 'POST'});
                const result = await response.json();
                alert(result.message);
                updateStatus();
            }
            
            async function runSingleRound() {
                const response = await fetch('/api/simulation/round', {method: 'POST'});
                const result = await response.json();
                alert(result.message);
                updateStatus();
            }
            
            async function resetSimulation() {
                const response = await fetch('/api/simulation/reset', {method: 'POST'});
                const result = await response.json();
                alert(result.message);
                updateStatus();
            }
            
            async function updateStatus() {
                try {
                    const [summaryResponse, ledgerResponse] = await Promise.all([
                        fetch('/api/summary'),
                        fetch('/api/ledger')
                    ]);
                    
                    const summary = await summaryResponse.json();
                    const ledger = await ledgerResponse.json();
                    
                    document.getElementById('metrics').innerHTML = `
                        <div class="metric">
                            <div class="metric-value">${summary.total_nodes || 0}</div>
                            <div class="metric-label">Total Nodes</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${summary.consenting_nodes || 0}</div>
                            <div class="metric-label">Consenting</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${summary.consensus_percentage || 0}%</div>
                            <div class="metric-label">Consensus Rate</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${summary.network_status || 'unknown'}</div>
                            <div class="metric-label">Network Status</div>
                        </div>
                    `;
                    
                    document.getElementById('ledger-preview').textContent = JSON.stringify(ledger.slice(-3), null, 2);
                } catch (err) {
                    console.error('Failed to update status:', err);
                }
            }
            
            // Initial load and auto-refresh
            updateStatus();
            setInterval(updateStatus, 5000);
        </script>
    </body>
    </html>
    """

@app.route("/ledger")
def serve_dashboard():
    """Serve the visual ledger dashboard"""
    return send_from_directory("docs/foundation", "ledger_dashboard.html")

@app.route("/api/ledger")
def api_ledger():
    """API endpoint for ledger data"""
    return jsonify(read_ledger())

@app.route("/api/summary")
def api_summary():
    """API endpoint for network summary"""
    try:
        with open("docs/api/network_summary.json", "r") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({
            "timestamp": current_utc_iso(),
            "network_status": "offline",
            "total_nodes": 0,
            "consenting_nodes": 0,
            "pulse_layer_active": False
        })

@app.route("/api/nodes")
def api_nodes():
    """API endpoint for node states"""
    return jsonify(node_states)

@app.route("/api/simulation/start", methods=["POST"])
def api_start_simulation():
    """Start continuous simulation"""
    global simulation_running
    
    if simulation_running:
        return jsonify({"message": "Simulation already running", "status": "warning"})
    
    simulation_running = True
    thread = threading.Thread(target=simulation_loop, daemon=True)
    thread.start()
    
    return jsonify({"message": "Continuous simulation started", "status": "success"})

@app.route("/api/simulation/stop", methods=["POST"])
def api_stop_simulation():
    """Stop continuous simulation"""
    global simulation_running
    simulation_running = False
    return jsonify({"message": "Simulation stopped", "status": "success"})

@app.route("/api/simulation/round", methods=["POST"])
def api_run_round():
    """Run single consensus round"""
    simulate_consensus_round()
    return jsonify({"message": "Consensus round completed", "status": "success"})

@app.route("/api/simulation/reset", methods=["POST"])
def api_reset_simulation():
    """Reset node states and ledger"""
    global node_states, last_sync_time
    
    initialize_node_states()
    write_ledger([])
    last_sync_time = None
    
    return jsonify({"message": "Simulation reset completed", "status": "success"})

# Serve static files from docs directory
@app.route("/docs/<path:filename>")
def serve_docs(filename):
    """Serve documentation files"""
    return send_from_directory("docs", filename)

if __name__ == "__main__":
    print("🌌 Euystacio Network Test Harness Starting...")
    print("="*60)
    print("Purpose: Local simulation environment for Visual Ledger Dashboard")
    print("Author: Seedbringer & Council Directive (15-09-2025)")
    print("="*60)
    
    # Initialize simulation environment
    initialize_node_states()
    
    # Ensure required directories exist
    os.makedirs("docs/foundation", exist_ok=True)
    os.makedirs("docs/transparency", exist_ok=True)
    os.makedirs("docs/api", exist_ok=True)
    
    # Run initial consensus round
    simulate_consensus_round()
    
    print(f"✅ Test harness initialized with {len(SIMULATED_NODES)} simulated nodes")
    print("📊 Access dashboard at: http://localhost:5000/ledger")
    print("🎮 Access controls at: http://localhost:5000/")
    print("🔗 API endpoints available at: /api/ledger, /api/summary, /api/nodes")
    print("="*60)
    
    app.run(host="0.0.0.0", port=5000, debug=True)