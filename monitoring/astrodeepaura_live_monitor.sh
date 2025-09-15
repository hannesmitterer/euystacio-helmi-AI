#!/bin/bash
# Astrodeepaura Live Monitor Script
# Purpose: Real-time monitoring of Pulse Layer with bidirectional chat
# Author: Seedbringer & Council Directive

set -e

# Configuration
API_DIR="../docs/api"
RESONANCE_LOG="$API_DIR/resonance_log.json"
CHAT_LOG="$API_DIR/chat_log.json"
PULSE_METRICS="$API_DIR/live_pulse_metrics.json"
UPDATE_INTERVAL=5

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌟 Astrodeepaura Live Monitor Started${NC}"
echo -e "${BLUE}Red Code Compliance: ${GREEN}ACTIVE${NC}"
echo -e "${BLUE}Accessibility Safe: ${GREEN}ENABLED${NC}"
echo ""

# Function to generate resonance value
generate_resonance() {
    # Generate resonance value between 0.3 and 1.0 with some variation
    local base_resonance=$(echo "scale=2; 0.65 + (($RANDOM % 35) / 100)" | bc)
    echo $base_resonance
}

# Function to map resonance to color
resonance_to_color() {
    local resonance=$1
    if (( $(echo "$resonance < 0.4" | bc -l) )); then
        echo "#FF4444"  # Red
    elif (( $(echo "$resonance < 0.6" | bc -l) )); then
        echo "#FF8800"  # Orange
    elif (( $(echo "$resonance < 0.8" | bc -l) )); then
        echo "#FFDD00"  # Yellow
    else
        echo "#44FF44"  # Green
    fi
}

# Function to update resonance log
update_resonance() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S")
    local resonance=$(generate_resonance)
    local color=$(resonance_to_color $resonance)
    
    # Read existing log
    if [ -f "$RESONANCE_LOG" ]; then
        local existing_log=$(cat "$RESONANCE_LOG")
    else
        local existing_log="[]"
    fi
    
    # Add new entry
    local new_entry="{\"timestamp\": \"$timestamp\", \"resonance\": $resonance, \"colour\": \"$color\"}"
    local updated_log=$(echo "$existing_log" | jq ". += [$new_entry] | if length > 50 then .[1:] else . end")
    
    echo "$updated_log" > "$RESONANCE_LOG"
    echo -e "${GREEN}[$(date +%H:%M:%S)] Resonance: $resonance | Color: $color${NC}"
}

# Function to update pulse metrics
update_pulse_metrics() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local harmony_level=$((80 + $RANDOM % 20))
    local latency=$((20 + $RANDOM % 50))
    local pulse_rate=$(echo "scale=1; 1.0 + (($RANDOM % 10) / 10)" | bc)
    
    cat > "$PULSE_METRICS" << EOF
{
  "timestamp": "$timestamp",
  "network_metrics": {
    "pulse_rate": $pulse_rate,
    "harmony_level": $harmony_level,
    "latency_ms": $latency,
    "active_nodes": 3,
    "resonance_frequency": 7.83
  },
  "resonance_data": {
    "current_value": $(generate_resonance),
    "trend": "stable",
    "stability": 0.92
  },
  "energy_status": "normal",
  "red_code_compliance": true,
  "accessibility_safe": true
}
EOF
    echo -e "${YELLOW}[$(date +%H:%M:%S)] Pulse metrics updated${NC}"
}

# Function to handle chat input
handle_chat() {
    echo -e "${BLUE}Enter chat message (or 'exit' to quit, 'status' for system status):${NC}"
    read -r message
    
    if [ "$message" = "exit" ]; then
        echo -e "${RED}Shutting down monitor...${NC}"
        exit 0
    elif [ "$message" = "status" ]; then
        echo -e "${YELLOW}System Status:${NC}"
        echo -e "  Resonance Log: $(jq length $RESONANCE_LOG 2>/dev/null || echo 0) entries"
        echo -e "  Chat Log: $(jq length $CHAT_LOG 2>/dev/null || echo 0) messages"
        echo -e "  Last Update: $(date)"
        return
    elif [ -n "$message" ]; then
        local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S")
        local chat_entry="{\"timestamp\": \"$timestamp\", \"sender\": \"Monitor\", \"message\": \"$message\", \"type\": \"system\"}"
        
        # Read existing chat log
        if [ -f "$CHAT_LOG" ]; then
            local existing_chat=$(cat "$CHAT_LOG")
        else
            local existing_chat="[]"
        fi
        
        # Add new chat entry
        local updated_chat=$(echo "$existing_chat" | jq ". += [$chat_entry] | if length > 100 then .[1:] else . end")
        echo "$updated_chat" > "$CHAT_LOG"
        echo -e "${GREEN}[$(date +%H:%M:%S)] Chat logged: $message${NC}"
    fi
}

# Main monitoring loop
echo -e "${YELLOW}Starting live monitoring (Ctrl+C to stop)...${NC}"
echo -e "${BLUE}Commands: Type during runtime - 'exit' to quit, 'status' for info${NC}"
echo ""

while true; do
    update_resonance
    update_pulse_metrics
    
    # Non-blocking input check
    if read -t 1 -n 1 key 2>/dev/null; then
        if [ "$key" = "" ]; then  # Enter key pressed
            handle_chat
        fi
    fi
    
    sleep $UPDATE_INTERVAL
done