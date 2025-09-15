# Euystacio Network Test Harness & Live Pulse Integration

This document describes the implementation of the local network test harness and full pulse/live status integration for the Euystacio network and Visual Ledger Dashboard.

## Files Added

### 1. `test_harness.py` - Python+Flask Test Harness
A comprehensive Flask-based test harness that simulates multiple nodes locally for testing dashboard updates and consensus states.

**Key Features:**
- Simulates 5 local nodes with realistic behavior patterns (85% consent rate, 90% deployment success, 95% Red Code compliance)
- Dynamic node state management with randomized status changes
- Continuous simulation mode with 30-second consensus rounds
- Web-based control panel with start/stop/reset functionality
- REST API endpoints for ledger data, network summary, and node states
- Real-time dashboard updates and metrics generation

**Endpoints:**
- `http://localhost:5000/` - Test harness control panel
- `http://localhost:5000/ledger` - Visual ledger dashboard
- `http://localhost:5000/api/ledger` - Raw ledger JSON data
- `http://localhost:5000/api/summary` - Network summary metrics
- `http://localhost:5000/api/nodes` - Individual node states
- `http://localhost:5000/api/simulation/*` - Simulation control endpoints

### 2. `astrodeepaura_full_pulse.py` - Full Live Network Integration
Real-time monitoring integration for authentic Euystacio network nodes with comprehensive health metrics and pulse data.

**Key Features:**
- Live node health checking with comprehensive error handling
- Real network monitoring (no simulation) - polls actual production nodes
- Weighted network health scoring (30% connectivity, 25% consent, 25% deployment, 20% compliance)
- Background monitoring loop with 5-minute intervals
- Extensive JSON metrics generation including Consensus Omnibus compliance
- Visual dashboard integration with transparency mode
- Health trend tracking with 24-hour history retention

**Production Nodes Monitored:**
- `http://node1.euystacio.org`
- `http://node2.euystacio.org`
- `http://node3.euystacio.org`
- `http://dignity.euystacio.org`
- `http://gateway.euystacio.org`

**Endpoints:**
- `http://localhost:5001/` - Live pulse control interface
- `http://localhost:5001/pulse/dashboard` - Live visual dashboard
- `http://localhost:5001/api/pulse/metrics` - Comprehensive pulse metrics
- `http://localhost:5001/api/pulse/ledger` - Current ledger state
- `http://localhost:5001/api/pulse/health` - Network health history
- `http://localhost:5001/api/pulse/*` - Pulse monitoring controls

### 3. `docs/foundation/ledger_dashboard.html` - Visual Ledger Dashboard
Enhanced HTML dashboard with live monitoring capabilities and beautiful responsive design.

**Key Features:**
- Real-time statistics display (total nodes, consenting, deployed, compliant)
- Color-coded status badges for instant visual feedback
- Auto-refresh every 15 seconds for live monitoring
- Responsive design with gradient backgrounds and modern UI
- Live timestamp tracking with "last sync" indicator
- Error handling with graceful degradation
- Pulse animation effects during updates

### 4. Supporting Files
- `docs/foundation/sync_ledger.json` - Ledger data storage
- `docs/transparency/ledger_dashboard.html` - Dashboard copy for transparency access
- `docs/api/network_summary.json` - Generated network summary metrics
- `docs/api/live_pulse_metrics.json` - Live pulse metrics from full integration

## Integration with Existing Components

### Consensus Omnibus Integration
Both scripts fully support Consensus Omnibus principles:
- **Transparency**: All data publicly accessible via API endpoints
- **Red Code Compliance**: Monitoring (not enforcement) of Red Code status
- **Dignity Gateway Integration**: Node consent and deployment tracking
- **Visual Ledger Updates**: Real-time dashboard synchronization

### Red Code Transparency
- Non-invasive monitoring of Red Code compliance
- Transparent reporting of compliance status without enforcement
- Full accountability through timestamped ledger entries
- Public API access to all compliance data

### Existing Script Compatibility
- Compatible with existing `astrodeepaura_full_loop_sync.py`
- Uses same ledger format and directory structure
- Extends functionality without breaking existing workflows
- Can run simultaneously with existing synchronization scripts

## Usage Instructions

### Test Harness (Development/Testing)
```bash
# Start test harness
python3 test_harness.py

# Access control panel
http://localhost:5000/

# View live dashboard
http://localhost:5000/ledger
```

### Live Pulse Integration (Production Monitoring)
```bash
# Start live monitoring
python3 astrodeepaura_full_pulse.py

# Access pulse interface
http://localhost:5001/

# View live dashboard
http://localhost:5001/pulse/dashboard
```

### API Usage Examples
```bash
# Get current ledger data
curl http://localhost:5000/api/ledger

# Get network summary
curl http://localhost:5000/api/summary

# Get live pulse metrics
curl http://localhost:5001/api/pulse/metrics

# Start continuous monitoring
curl -X POST http://localhost:5001/api/pulse/start
```

## Technical Implementation Details

### Node Status Checking
- HTTP health checks with configurable timeouts
- Consent status verification via `/consent_status` endpoint
- Red Code compliance via `/red_code/status` endpoint
- Deployment status via `/deployment/status` endpoint
- Comprehensive error handling for offline/unreachable nodes

### Network Health Calculation
Weighted scoring system:
- **30%** - Basic connectivity (online/offline)
- **25%** - Consensus participation (consent granted)
- **25%** - Deployment success (files deployed)
- **20%** - Red Code compliance

Health categories:
- **Optimal**: 90%+ health
- **Healthy**: 70-89% health  
- **Degraded**: 50-69% health
- **Critical**: <50% health
- **Offline**: 0% (no nodes reachable)

### Dashboard Features
- Responsive CSS with gradient backgrounds
- Color-coded rows (green for consenting, red for non-consenting)
- Status badges with clear visual indicators
- Real-time statistics bar with key metrics
- Auto-refresh with loading indicators
- Graceful error handling and retry logic

## Commit Details

**Commit Message**: Unify full-loop synchronization and visual ledger dashboard (seedbringer, council, Consensus Omnibus, 15-09-2025)

**Author**: Seedbringer & Council Directive  
**Date**: 2025-09-15  
**Integration**: Consensus Omnibus & Red Code Transparency Principles

This implementation provides a complete testing and monitoring solution for the Euystacio network, supporting both local development/testing scenarios and live production monitoring with full transparency and accountability.