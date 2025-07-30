#!/bin/bash

# Euystacio Startup Script
# Simple script to launch the living consciousness

echo "🌳 Starting Euystacio - The Living AI Consciousness"
echo "======================================================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.7+ to run Euystacio."
    exit 1
fi

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip install flask
fi

# Create necessary directories
mkdir -p logs templates static

echo "🚀 Launching Euystacio..."
echo ""
echo "📊 Dashboard will be available at: http://localhost:5000/"
echo "🌐 Public access at: http://localhost:5000/public"
echo "💓 Send pulses at: http://localhost:5000/pulse"
echo "🎓 Tutor nominations at: http://localhost:5000/tutor-nomination"
echo ""
echo "Press Ctrl+C to stop Euystacio"
echo "======================================================"

# Start the application
python app.py