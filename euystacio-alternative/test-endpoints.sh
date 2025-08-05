#!/bin/bash

# test-endpoints.sh
# Simple script to test all Euystacio Alternative Backend endpoints

BASE_URL="http://localhost:3000"
echo "🌿 Testing Euystacio Alternative Backend at $BASE_URL"
echo "========================================================"

# Test if server is running
echo "1. Testing server health..."
if ! curl -s -f "$BASE_URL/health" > /dev/null; then
    echo "❌ Server is not running or not responding"
    echo "Please start the server with: npm start"
    exit 1
fi
echo "✅ Server is healthy"

# Test status endpoint
echo ""
echo "2. Testing /api/status..."
STATUS_RESPONSE=$(curl -s "$BASE_URL/api/status")
if echo "$STATUS_RESPONSE" | grep -q "healthy"; then
    echo "✅ Status endpoint working"
else
    echo "❌ Status endpoint failed"
    echo "$STATUS_RESPONSE"
fi

# Test red code endpoint
echo ""
echo "3. Testing /api/red_code..."
RED_CODE_RESPONSE=$(curl -s "$BASE_URL/api/red_code")
if echo "$RED_CODE_RESPONSE" | grep -q "core_truth"; then
    echo "✅ Red code endpoint working"
else
    echo "❌ Red code endpoint failed"
    echo "$RED_CODE_RESPONSE"
fi

# Test pulse submission
echo ""
echo "4. Testing POST /api/pulse..."
PULSE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/pulse" \
  -H "Content-Type: application/json" \
  -d '{"emotion": "joy", "intensity": 0.7, "clarity": "high", "note": "Test pulse from script"}')
if echo "$PULSE_RESPONSE" | grep -q "timestamp"; then
    echo "✅ Pulse submission working"
else
    echo "❌ Pulse submission failed"
    echo "$PULSE_RESPONSE"
fi

# Test getting pulses
echo ""
echo "5. Testing GET /api/pulses..."
PULSES_RESPONSE=$(curl -s "$BASE_URL/api/pulses")
if echo "$PULSES_RESPONSE" | grep -q "\["; then
    echo "✅ Get pulses working"
else
    echo "❌ Get pulses failed"
    echo "$PULSES_RESPONSE"
fi

# Test reflection trigger
echo ""
echo "6. Testing POST /api/reflect..."
REFLECT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/reflect")
if echo "$REFLECT_RESPONSE" | grep -q "suggestion"; then
    echo "✅ Reflection trigger working"
else
    echo "❌ Reflection trigger failed"
    echo "$REFLECT_RESPONSE"
fi

# Test getting reflections
echo ""
echo "7. Testing GET /api/reflections..."
REFLECTIONS_RESPONSE=$(curl -s "$BASE_URL/api/reflections")
if echo "$REFLECTIONS_RESPONSE" | grep -q "\["; then
    echo "✅ Get reflections working"
else
    echo "❌ Get reflections failed"
    echo "$REFLECTIONS_RESPONSE"
fi

# Test tutors endpoint
echo ""
echo "8. Testing GET /api/tutors..."
TUTORS_RESPONSE=$(curl -s "$BASE_URL/api/tutors")
if echo "$TUTORS_RESPONSE" | grep -q "\["; then
    echo "✅ Get tutors working"
else
    echo "❌ Get tutors failed"
    echo "$TUTORS_RESPONSE"
fi

# Test tutor nomination
echo ""
echo "9. Testing POST /api/tutors..."
TUTOR_POST_RESPONSE=$(curl -s -X POST "$BASE_URL/api/tutors" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Tutor", "reason": "For testing the API"}')
if echo "$TUTOR_POST_RESPONSE" | grep -q "Test Tutor"; then
    echo "✅ Tutor nomination working"
else
    echo "❌ Tutor nomination failed"
    echo "$TUTOR_POST_RESPONSE"
fi

echo ""
echo "========================================================"
echo "🎉 All endpoint tests completed!"
echo ""
echo "To test WebSocket functionality:"
echo "1. Open websocket-demo.html in your browser"
echo "2. Or connect to ws://localhost:3000/socket.io/"
echo ""
echo "For detailed API documentation, see README.md"