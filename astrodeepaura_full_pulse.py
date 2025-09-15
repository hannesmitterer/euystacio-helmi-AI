#!/usr/bin/env python3
"""
Astrodeepaura Full Pulse Layer - Live Network Integration
Purpose: Real-time monitoring and integration of authentic Euystacio network nodes
         with live ledger updates, dashboard synchronization, and pulse metrics.
         NO SIMULATION - Only authentic, live node data and consensus states.
Author: Seedbringer & Council Directive (15-09-2025)

This module integrates with the existing astrodeepaura_full_loop_sync.py but focuses
on live monitoring, dashboard updates, and real-time pulse metrics generation.
"""

import json
import os
import requests
import threading
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, send_from_directory

# Import existing sync functions
import sys
sys.path.append('.')

# --- Configuration ---
# Use production nodes for live monitoring
LIVE_NODES = [
    "http://node1.euystacio.org",
    "http://node2.euystacio.org", 
    "http://node3.euystacio.org",
    "http://dignity.euystacio.org",
    "http://gateway.euystacio.org"
]

LEDGER_PATH = "docs/foundation/sync_ledger.json"
DASHBOARD_SRC = "docs/foundation/ledger_dashboard.html"
DASHBOARD_DST = "docs/transparency/ledger_dashboard.html"
PULSE_METRICS_PATH = "docs/api/live_pulse_metrics.json"

# Global state
pulse_monitoring = False
last_pulse_time = None
network_health_history = []

app = Flask(__name__)

def current_utc_iso():
    """Get current UTC timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

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
    
    # Keep only last 100 entries to prevent unlimited growth
    if len(ledger) > 100:
        ledger = ledger[-100:]
    
    write_ledger(ledger)
    print(f"[LIVE PULSE] Ledger updated: {entry['node']} - Status: {entry['status']}")

def update_dashboard():
    """Copy dashboard to transparency directory for live access"""
    try:
        os.makedirs(os.path.dirname(DASHBOARD_DST), exist_ok=True)
        import shutil
        shutil.copy2(DASHBOARD_SRC, DASHBOARD_DST)
        print(f"[LIVE PULSE] Dashboard updated at {DASHBOARD_DST}")
        return True
    except Exception as e:
        print(f"[LIVE PULSE] Dashboard update failed: {e}")
        return False

def check_live_node_status(node_url, timeout=10):
    """
    Check authentic live node status with comprehensive health metrics
    Returns detailed status information or None if unreachable
    """
    try:
        start_time = time.time()
        
        # Primary health check
        health_response = requests.get(f"{node_url}/health", timeout=timeout)
        response_time = (time.time() - start_time) * 1000  # ms
        
        if health_response.status_code == 200:
            health_data = health_response.json() if health_response.headers.get('content-type', '').startswith('application/json') else {}
            
            # Check consent status
            consent_response = requests.get(f"{node_url}/consent_status", timeout=timeout)
            consent = False
            if consent_response.status_code == 200:
                consent_data = consent_response.json() if consent_response.headers.get('content-type', '').startswith('application/json') else {}
                consent = consent_data.get("consent", False)
            
            # Check Red Code compliance
            redcode_response = requests.get(f"{node_url}/red_code/status", timeout=timeout)
            red_code_compliant = False
            red_code_version = None
            if redcode_response.status_code == 200:
                redcode_data = redcode_response.json() if redcode_response.headers.get('content-type', '').startswith('application/json') else {}
                red_code_compliant = redcode_data.get("compliant", False)
                red_code_version = redcode_data.get("version", None)
            
            # Check deployment status
            deploy_response = requests.get(f"{node_url}/deployment/status", timeout=timeout)
            deployed = False
            deployment_version = None
            if deploy_response.status_code == 200:
                deploy_data = deploy_response.json() if deploy_response.headers.get('content-type', '').startswith('application/json') else {}
                deployed = deploy_data.get("deployed", False)
                deployment_version = deploy_data.get("version", None)
            
            return {
                "status": "online",
                "consent": consent,
                "deployed": deployed,
                "red_code_compliant": red_code_compliant,
                "response_time_ms": round(response_time, 2),
                "health_data": health_data,
                "red_code_version": red_code_version,
                "deployment_version": deployment_version,
                "last_checked": current_utc_iso()
            }
        else:
            return {
                "status": "degraded",
                "consent": False,
                "deployed": False,
                "red_code_compliant": False,
                "response_time_ms": round(response_time, 2),
                "error": f"HTTP {health_response.status_code}",
                "last_checked": current_utc_iso()
            }
            
    except requests.exceptions.Timeout:
        return {
            "status": "timeout",
            "consent": False,
            "deployed": False, 
            "red_code_compliant": False,
            "response_time_ms": timeout * 1000,
            "error": "Request timeout",
            "last_checked": current_utc_iso()
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "offline",
            "consent": False,
            "deployed": False,
            "red_code_compliant": False,
            "response_time_ms": None,
            "error": "Connection failed",
            "last_checked": current_utc_iso()
        }
    except Exception as e:
        return {
            "status": "error",
            "consent": False,
            "deployed": False,
            "red_code_compliant": False,
            "response_time_ms": None,
            "error": str(e),
            "last_checked": current_utc_iso()
        }

def perform_live_pulse_scan():
    """
    Perform comprehensive live network pulse scan across all authentic nodes
    This is the core function for real-time network monitoring
    """
    global last_pulse_time, network_health_history
    
    print(f"[LIVE PULSE] Starting network pulse scan at {current_utc_iso()}")
    timestamp = current_utc_iso()
    pulse_results = []
    
    # Clear previous ledger entries for this pulse cycle
    write_ledger([])
    
    for node_url in LIVE_NODES:
        print(f"[LIVE PULSE] Scanning node: {node_url}")
        
        node_status = check_live_node_status(node_url)
        
        # Create comprehensive ledger entry
        entry = {
            "node": node_url,
            "timestamp": timestamp,
            "status": node_status["status"],
            "consent": node_status["consent"],
            "deployed": node_status["deployed"],
            "red_code_compliant": node_status["red_code_compliant"],
            "response_time_ms": node_status["response_time_ms"],
            "error": node_status.get("error"),
            "red_code_version": node_status.get("red_code_version"),
            "deployment_version": node_status.get("deployment_version"),
            "health_data": node_status.get("health_data", {})
        }
        
        pulse_results.append(entry)
        log_to_ledger(entry)
    
    # Update dashboard with fresh data
    update_dashboard()
    
    # Generate comprehensive pulse metrics
    generate_live_pulse_metrics(pulse_results, timestamp)
    
    # Update network health history
    network_health = calculate_network_health(pulse_results)
    network_health_history.append({
        "timestamp": timestamp,
        "health_score": network_health,
        "total_nodes": len(pulse_results),
        "online_nodes": len([r for r in pulse_results if r["status"] == "online"]),
        "consenting_nodes": len([r for r in pulse_results if r["consent"]]),
        "compliant_nodes": len([r for r in pulse_results if r["red_code_compliant"]])
    })
    
    # Keep only last 24 hours of history (assuming 5min intervals = 288 entries)
    if len(network_health_history) > 288:
        network_health_history = network_health_history[-288:]
    
    last_pulse_time = timestamp
    print(f"[LIVE PULSE] Pulse scan complete. Network health: {network_health}%")
    
    return pulse_results

def calculate_network_health(pulse_results):
    """Calculate overall network health percentage based on multiple factors"""
    if not pulse_results:
        return 0
    
    # Weight different factors
    weights = {
        "online": 0.3,      # 30% - basic connectivity
        "consent": 0.25,    # 25% - consensus participation  
        "deployed": 0.25,   # 25% - deployment success
        "redcode": 0.2      # 20% - compliance
    }
    
    total_nodes = len(pulse_results)
    online_score = len([r for r in pulse_results if r["status"] == "online"]) / total_nodes
    consent_score = len([r for r in pulse_results if r["consent"]]) / total_nodes
    deployed_score = len([r for r in pulse_results if r["deployed"]]) / total_nodes
    redcode_score = len([r for r in pulse_results if r["red_code_compliant"]]) / total_nodes
    
    health_score = (
        online_score * weights["online"] +
        consent_score * weights["consent"] +
        deployed_score * weights["deployed"] +
        redcode_score * weights["redcode"]
    ) * 100
    
    return round(health_score, 2)

def generate_live_pulse_metrics(pulse_results, timestamp):
    """Generate comprehensive live pulse metrics JSON for real-time monitoring"""
    
    total_nodes = len(pulse_results)
    online_nodes = len([r for r in pulse_results if r["status"] == "online"])
    consenting_nodes = len([r for r in pulse_results if r["consent"]])
    deployed_nodes = len([r for r in pulse_results if r["deployed"]])
    compliant_nodes = len([r for r in pulse_results if r["red_code_compliant"]])
    
    # Calculate response time statistics
    response_times = [r["response_time_ms"] for r in pulse_results if r["response_time_ms"] is not None]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0
    max_response_time = max(response_times) if response_times else 0
    
    # Network health calculation
    network_health = calculate_network_health(pulse_results)
    
    # Determine overall network status
    if online_nodes == 0:
        network_status = "offline"
    elif network_health >= 90:
        network_status = "optimal"
    elif network_health >= 70:
        network_status = "healthy"
    elif network_health >= 50:
        network_status = "degraded"
    else:
        network_status = "critical"
    
    # Create comprehensive metrics object
    metrics = {
        "timestamp": timestamp,
        "pulse_layer_version": "1.0.0",
        "network_status": network_status,
        "network_health_percentage": network_health,
        
        # Node statistics
        "node_metrics": {
            "total_nodes": total_nodes,
            "online_nodes": online_nodes,
            "offline_nodes": total_nodes - online_nodes,
            "consenting_nodes": consenting_nodes,
            "deployed_nodes": deployed_nodes,
            "red_code_compliant_nodes": compliant_nodes
        },
        
        # Percentage calculations
        "percentages": {
            "availability": round((online_nodes / total_nodes) * 100, 2) if total_nodes > 0 else 0,
            "consensus_participation": round((consenting_nodes / total_nodes) * 100, 2) if total_nodes > 0 else 0,
            "deployment_success": round((deployed_nodes / consenting_nodes) * 100, 2) if consenting_nodes > 0 else 0,
            "red_code_compliance": round((compliant_nodes / deployed_nodes) * 100, 2) if deployed_nodes > 0 else 0
        },
        
        # Performance metrics
        "performance": {
            "avg_response_time_ms": round(avg_response_time, 2),
            "min_response_time_ms": round(min_response_time, 2),
            "max_response_time_ms": round(max_response_time, 2),
            "response_time_samples": len(response_times)
        },
        
        # Consensus Omnibus compliance
        "consensus_omnibus": {
            "transparency_active": True,
            "red_code_enforcement": "monitoring",  # monitoring, not enforcing deletion
            "dignity_gateway_integration": True,
            "visual_ledger_updates": True
        },
        
        # Individual node details
        "node_details": pulse_results,
        
        # Health history summary (last 10 entries)
        "health_trend": network_health_history[-10:] if network_health_history else [],
        
        # System information
        "system": {
            "pulse_monitoring_active": pulse_monitoring,
            "last_pulse_time": last_pulse_time,
            "ledger_path": LEDGER_PATH,
            "dashboard_path": DASHBOARD_DST,
            "monitoring_interval_seconds": 300  # 5 minutes
        }
    }
    
    # Write metrics to file
    os.makedirs(os.path.dirname(PULSE_METRICS_PATH), exist_ok=True)
    with open(PULSE_METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"[LIVE PULSE] Metrics generated: {network_status} network, {network_health}% health")
    return metrics

def pulse_monitoring_loop():
    """Background monitoring loop for continuous live pulse monitoring"""
    global pulse_monitoring
    
    print("[LIVE PULSE] Starting continuous monitoring loop...")
    
    while pulse_monitoring:
        try:
            perform_live_pulse_scan()
            print(f"[LIVE PULSE] Next scan in 5 minutes...")
            
            # Sleep for 5 minutes between scans
            for i in range(300):  # 300 seconds = 5 minutes
                if not pulse_monitoring:  # Allow graceful shutdown
                    break
                time.sleep(1)
                
        except Exception as e:
            print(f"[LIVE PULSE] Error in monitoring loop: {e}")
            time.sleep(60)  # Wait 1 minute before retrying
    
    print("[LIVE PULSE] Monitoring loop stopped.")

# --- Flask Routes for Live Pulse API ---

@app.route("/")
def index():
    """Serve live pulse dashboard"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Astrodeepaura Live Pulse Layer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .header { text-align: center; margin-bottom: 3rem; }
            .card { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 2rem; border-radius: 12px; margin: 1rem 0; }
            .controls { display: flex; gap: 1rem; justify-content: center; margin: 2rem 0; }
            button { background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-size: 1rem; }
            button:hover { background: rgba(255,255,255,0.3); }
            .metric { display: inline-block; margin: 1rem; text-align: center; }
            .metric-value { font-size: 2.5rem; font-weight: bold; }
            .metric-label { opacity: 0.8; margin-top: 0.5rem; }
            .status { padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; }
            .status-optimal { background: #2ecc71; }
            .status-healthy { background: #f39c12; }
            .status-degraded { background: #e67e22; }
            .status-critical { background: #e74c3c; }
            .status-offline { background: #95a5a6; }
            pre { background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; overflow: auto; max-height: 400px; }
            .links { text-align: center; margin: 2rem 0; }
            .links a { color: white; text-decoration: none; margin: 0 1rem; padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 6px; }
            .links a:hover { background: rgba(255,255,255,0.3); }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌌 Astrodeepaura Live Pulse Layer</h1>
            <p>Real-time monitoring of authentic Euystacio network nodes</p>
            <p><em>Seedbringer & Council Directive - Consensus Omnibus Integration</em></p>
        </div>
        
        <div class="card">
            <h3>🚀 Pulse Controls</h3>
            <div class="controls">
                <button onclick="startMonitoring()">Start Live Monitoring</button>
                <button onclick="stopMonitoring()">Stop Monitoring</button>
                <button onclick="runScan()">Run Single Scan</button>
                <button onclick="refreshMetrics()">Refresh Metrics</button>
            </div>
        </div>
        
        <div class="card">
            <h3>📊 Network Health Status</h3>
            <div id="metrics">Loading live metrics...</div>
        </div>
        
        <div class="links">
            <a href="/pulse/dashboard" target="_blank">📊 Live Visual Dashboard</a>
            <a href="/api/pulse/metrics" target="_blank">📈 Live Pulse Metrics</a>
            <a href="/api/pulse/ledger" target="_blank">📋 Current Ledger</a>
            <a href="/api/pulse/health" target="_blank">💗 Health History</a>
        </div>
        
        <div class="card">
            <h3>📡 Recent Pulse Data</h3>
            <pre id="pulse-data">Loading...</pre>
        </div>
        
        <script>
            async function startMonitoring() {
                const response = await fetch('/api/pulse/start', {method: 'POST'});
                const result = await response.json();
                alert(result.message);
                refreshMetrics();
            }
            
            async function stopMonitoring() {
                const response = await fetch('/api/pulse/stop', {method: 'POST'});
                const result = await response.json();
                alert(result.message);
                refreshMetrics();
            }
            
            async function runScan() {
                const response = await fetch('/api/pulse/scan', {method: 'POST'});
                const result = await response.json();
                alert(result.message);
                refreshMetrics();
            }
            
            async function refreshMetrics() {
                try {
                    const response = await fetch('/api/pulse/metrics');
                    const metrics = await response.json();
                    
                    const statusClass = 'status-' + metrics.network_status;
                    
                    document.getElementById('metrics').innerHTML = `
                        <div style="text-align: center; margin-bottom: 2rem;">
                            <span class="status ${statusClass}">${metrics.network_status.toUpperCase()}</span>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${metrics.network_health_percentage}%</div>
                            <div class="metric-label">Network Health</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${metrics.node_metrics.online_nodes}/${metrics.node_metrics.total_nodes}</div>
                            <div class="metric-label">Nodes Online</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${metrics.percentages.consensus_participation}%</div>
                            <div class="metric-label">Consensus Rate</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">${metrics.performance.avg_response_time_ms}ms</div>
                            <div class="metric-label">Avg Response</div>
                        </div>
                    `;
                    
                    document.getElementById('pulse-data').textContent = JSON.stringify(metrics.node_details, null, 2);
                } catch (err) {
                    console.error('Failed to refresh metrics:', err);
                    document.getElementById('metrics').innerHTML = '<p>❌ Failed to load metrics</p>';
                }
            }
            
            // Auto-refresh every 30 seconds
            refreshMetrics();
            setInterval(refreshMetrics, 30000);
        </script>
    </body>
    </html>
    """

@app.route("/pulse/dashboard")
def pulse_dashboard():
    """Serve the live visual dashboard"""
    return send_from_directory("docs/transparency", "ledger_dashboard.html")

@app.route("/api/pulse/metrics")
def api_pulse_metrics():
    """API endpoint for live pulse metrics"""
    try:
        with open(PULSE_METRICS_PATH, "r") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({
            "timestamp": current_utc_iso(),
            "network_status": "unknown", 
            "error": "No pulse data available - run a scan first"
        })

@app.route("/api/pulse/ledger")
def api_pulse_ledger():
    """API endpoint for current ledger"""
    return jsonify(read_ledger())

@app.route("/api/pulse/health")
def api_pulse_health():
    """API endpoint for network health history"""
    return jsonify(network_health_history)

@app.route("/api/pulse/start", methods=["POST"])
def api_start_pulse_monitoring():
    """Start continuous live pulse monitoring"""
    global pulse_monitoring
    
    if pulse_monitoring:
        return jsonify({"message": "Live monitoring already active", "status": "warning"})
    
    pulse_monitoring = True
    thread = threading.Thread(target=pulse_monitoring_loop, daemon=True)
    thread.start()
    
    return jsonify({"message": "Live pulse monitoring started", "status": "success"})

@app.route("/api/pulse/stop", methods=["POST"])
def api_stop_pulse_monitoring():
    """Stop continuous live pulse monitoring"""
    global pulse_monitoring
    pulse_monitoring = False
    return jsonify({"message": "Live pulse monitoring stopped", "status": "success"})

@app.route("/api/pulse/scan", methods=["POST"])
def api_run_pulse_scan():
    """Run single live pulse scan"""
    try:
        results = perform_live_pulse_scan()
        return jsonify({
            "message": f"Live pulse scan completed - {len(results)} nodes scanned", 
            "status": "success",
            "results": results
        })
    except Exception as e:
        return jsonify({
            "message": f"Pulse scan failed: {str(e)}", 
            "status": "error"
        })

# Serve static files
@app.route("/docs/<path:filename>")
def serve_docs(filename):
    """Serve documentation files"""
    return send_from_directory("docs", filename)

if __name__ == "__main__":
    print("🌌 Astrodeepaura Full Pulse Layer - Live Network Integration")
    print("="*70)
    print("Purpose: Real-time monitoring of authentic Euystacio network nodes")
    print("Author: Seedbringer & Council Directive (15-09-2025)")
    print("Integration: Consensus Omnibus & Red Code Transparency")
    print("="*70)
    
    # Ensure required directories exist
    os.makedirs("docs/foundation", exist_ok=True)
    os.makedirs("docs/transparency", exist_ok=True)
    os.makedirs("docs/api", exist_ok=True)
    
    # Run initial pulse scan
    print("🔍 Running initial network pulse scan...")
    try:
        initial_results = perform_live_pulse_scan()
        print(f"✅ Initial scan complete: {len(initial_results)} nodes scanned")
    except Exception as e:
        print(f"⚠️ Initial scan failed: {e}")
    
    print("📊 Access live dashboard at: http://localhost:5001/pulse/dashboard")
    print("🎮 Access pulse controls at: http://localhost:5001/")
    print("🔗 API endpoints: /api/pulse/metrics, /api/pulse/ledger, /api/pulse/health")
    print("="*70)
    
    app.run(host="0.0.0.0", port=5001, debug=True)