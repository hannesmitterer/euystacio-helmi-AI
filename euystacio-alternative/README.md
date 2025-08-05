# Euystacio Alternative Backend (Node.js/Express)

A complete Node.js/Express alternative to the existing FastAPI backend for the Euystacio emotional pulse system. This implementation provides all the same REST API endpoints plus real-time WebSocket communication for enhanced user experience.

## Features

### ✅ REST API Endpoints

All original Flask/FastAPI endpoints are replicated:

- **POST** `/api/pulse` — Submit a new emotional pulse
- **GET** `/api/pulses` — Fetch the latest pulses  
- **GET** `/api/red_code` — Get the current "Red Code" state
- **GET** `/api/tutors` — Get tutor nominations
- **GET** `/api/reflections` — Get reflection logs
- **POST** `/api/reflect` — Trigger a new reflection
- **GET** `/api/status` — System status and statistics

### ⚡ WebSocket Broadcasting (Socket.IO)

Real-time updates for enhanced user experience:

- **new_pulse** — Broadcast when new emotional pulse is received
- **new_reflection** — Broadcast when reflection is triggered
- **red_code_update** — Broadcast when red code state changes
- **tutor_update** — Broadcast when tutor is nominated

### 🚀 Deployment Options

- **Standalone Server** — Deploy to Render, Railway, Heroku, or any Node.js hosting
- **Netlify Functions** — Serverless deployment (WebSocket limitations noted)

## Quick Start

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Navigate to the alternative backend directory:
```bash
cd euystacio-alternative
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Server will start on `http://localhost:3000`

### Testing the API

Open `websocket-demo.html` in your browser to test all endpoints and WebSocket functionality, or use curl:

```bash
# Get system status
curl http://localhost:3000/api/status

# Send a pulse
curl -X POST http://localhost:3000/api/pulse \
  -H "Content-Type: application/json" \
  -d '{"emotion": "joy", "intensity": 0.8, "clarity": "high", "note": "Feeling great!"}'

# Get recent pulses
curl http://localhost:3000/api/pulses

# Trigger reflection
curl -X POST http://localhost:3000/api/reflect

# Get reflections
curl http://localhost:3000/api/reflections
```

## Core Architecture

### Directory Structure

```
euystacio-alternative/
├── src/
│   ├── core/               # Core business logic
│   │   ├── sentimentoPulseInterface.js
│   │   ├── redCode.js
│   │   ├── reflector.js
│   │   └── tutorNomination.js
│   ├── api/                # REST API routes
│   │   └── routes.js
│   └── websocket/          # WebSocket handling
│       └── websocket.js
├── netlify/
│   └── functions/          # Netlify Functions adaptation
│       └── api.js
├── server.js               # Main Express server
├── frontend-integration.js # Frontend WebSocket examples
├── websocket-demo.html     # Demo page
├── package.json
└── README.md
```

### Core Modules

1. **SentimentoPulseInterface** — Handles emotional pulse processing
2. **RedCodeManager** — Manages the core AI state and symbiosis levels
3. **Reflector** — Generates insights and recommendations
4. **TutorNomination** — Manages tutor nomination system
5. **WebSocketManager** — Real-time communication layer

## Frontend Integration

### Basic WebSocket Client

Add Socket.IO client to your HTML:

```html
<script src="https://cdn.socket.io/4.7.4/socket.io.min.js"></script>
```

### JavaScript Integration

```javascript
// Connect to WebSocket
const socket = io(window.location.origin);

// Listen for real-time events
socket.on('new_pulse', (data) => {
    console.log('New pulse received:', data);
    // Update your UI
});

socket.on('new_reflection', (data) => {
    console.log('New reflection:', data);
    // Update reflections display
});

socket.on('red_code_update', (data) => {
    console.log('Red code updated:', data);
    // Update red code display
});

// Send a pulse
async function sendPulse(emotion, intensity, clarity, note) {
    const response = await fetch('/api/pulse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emotion, intensity, clarity, note })
    });
    // WebSocket will automatically notify all clients
}
```

### Updating Existing Frontend

If you have an existing dashboard (like the Flask version), see `frontend-integration.js` for a complete example of how to extend your current JavaScript to use WebSocket updates.

Key changes:
1. Add Socket.IO client library
2. Extend your dashboard class with WebSocket functionality  
3. Remove manual refresh intervals (WebSocket provides real-time updates)
4. Add visual feedback for real-time updates

## Deployment Guides

### 1. Standalone Server Deployment

#### Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables:
   ```
   NODE_ENV=production
   PORT=3000
   ```
3. Railway will automatically detect Node.js and run `npm start`

#### Render Deployment

1. Create a new Web Service on Render
2. Connect your repository
3. Set build command: `npm install`
4. Set start command: `npm start`
5. Set environment variables as needed

#### Heroku Deployment

1. Create a new Heroku app
2. Add a `Procfile`:
   ```
   web: npm start
   ```
3. Deploy using Git or GitHub integration

### 2. Netlify Functions Deployment

For serverless deployment on Netlify (note: WebSocket functionality is limited):

1. **Update netlify.toml** in the root project:
```toml
[build]
  publish = "static"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200

[functions]
  directory = "euystacio-alternative/netlify/functions"
```

2. **Install serverless dependencies**:
```bash
npm install serverless-http
```

3. **Deploy to Netlify**:
   - Connect your repository to Netlify
   - Set build directory to `euystacio-alternative`
   - Deploy

#### Netlify Limitations

- **No WebSocket support** — Netlify Functions don't support persistent connections
- **Alternative real-time options**:
  - Use Netlify's Forms for data collection
  - Integrate with external WebSocket services (Pusher, Ably)
  - Use Server-Sent Events (SSE) for one-way updates
  - Consider Netlify's real-time database integrations

### Environment Variables

For production deployments, consider setting:

```bash
NODE_ENV=production
PORT=3000
LOG_LEVEL=info
```

## API Documentation

### Pulse Submission

```http
POST /api/pulse
Content-Type: application/json

{
  "emotion": "joy",
  "intensity": 0.8,
  "clarity": "high", 
  "note": "Optional context note"
}
```

**Response:**
```json
{
  "timestamp": "2024-01-20T10:30:00.000Z",
  "emotion": "joy",
  "intensity": 0.8,
  "clarity": "high",
  "note": "Optional context note",
  "ai_signature_status": "verified"
}
```

### Red Code State

```http
GET /api/red_code
```

**Response:**
```json
{
  "core_truth": "Euystacio is here to grow with humans...",
  "sentimento_rhythm": true,
  "symbiosis_level": 0.1,
  "guardian_mode": false,
  "last_update": "2024-01-20",
  "growth_history": [],
  "recent_pulses": [...]
}
```

### System Status

```http
GET /api/status
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T10:30:00.000Z",
  "stats": {
    "total_pulses": 42,
    "recent_pulses": 5,
    "total_reflections": 3,
    "active_tutors": 2,
    "symbiosis_level": 0.1,
    "guardian_mode": false
  }
}
```

## WebSocket Events

### Client → Server

- `ping` — Health check
- `request_current_state` — Request current system state
- `subscribe` — Subscribe to event types: `['pulses', 'reflections']`
- `unsubscribe` — Unsubscribe from event types

### Server → Client

- `connection_established` — Connection confirmation
- `new_pulse` — New emotional pulse received
- `new_reflection` — New reflection generated
- `red_code_update` — Red code state changed
- `tutor_update` — Tutor nomination update
- `pong` — Response to ping

## Data Storage

The system uses JSON files for data persistence (matching the original Flask implementation):

- `red_code.json` — Core AI state
- `tutors.json` — Tutor nominations
- `logs/` — Pulse and reflection logs

For production deployments, consider upgrading to a proper database (PostgreSQL, MongoDB, etc.).

## Development

### Running in Development Mode

```bash
npm run dev
```

### Project Structure

The codebase is organized into clear modules:

- **Core Logic** — Business logic ported from Python
- **API Layer** — Express routes handling HTTP requests
- **WebSocket Layer** — Real-time communication
- **Deployment** — Multiple deployment target support

### Adding Features

1. **New API Endpoint** — Add to `src/api/routes.js`
2. **Core Logic** — Extend modules in `src/core/`
3. **WebSocket Events** — Add to `src/websocket/websocket.js`
4. **Frontend Integration** — Update `frontend-integration.js`

## Comparison with Flask Backend

| Feature | Flask Backend | Node.js Alternative |
|---------|---------------|-------------------|
| REST API | ✅ | ✅ |
| Data Storage | JSON files | JSON files |
| Real-time Updates | ❌ | ✅ WebSocket |
| Deployment Options | Limited | Multiple (standalone + serverless) |
| Frontend Integration | Basic | Enhanced with real-time |
| Scalability | Single process | Better concurrency |

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port 3000
   lsof -ti:3000 | xargs kill -9
   ```

2. **WebSocket connection fails**
   - Check firewall settings
   - Verify Socket.IO client version compatibility
   - Check browser console for errors

3. **Netlify Functions timeout**
   - Functions have execution time limits
   - Consider upgrading plan or optimizing code

### Logs

The server provides detailed logging:
```bash
npm start
# Watch for connection logs, API requests, and WebSocket events
```

## Contributing

When contributing to this alternative backend:

1. Maintain compatibility with the original Flask API
2. Add comprehensive logging
3. Update both standalone and Netlify Functions versions
4. Test WebSocket functionality thoroughly
5. Update documentation

## License

Same license as the main Euystacio project.

---

**🌿 Welcome to the enhanced Euystacio backend experience with real-time emotional pulse sharing!**