/**
 * server.js
 * Main Express server for Euystacio alternative backend
 */

const express = require('express');
const http = require('http');
const cors = require('cors');
const path = require('path');
const fs = require('fs-extra');

// Import our modules
const apiRoutes = require('./src/api/routes');
const WebSocketManager = require('./src/websocket/websocket');

// Initialize Express app
const app = express();
const server = http.createServer(app);

// Initialize WebSocket manager
const wsManager = new WebSocketManager(server);

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Add socket.io instance to requests for API routes
app.use((req, res, next) => {
    req.io = wsManager.getIO();
    req.wsManager = wsManager;
    next();
});

// Serve static files (if needed for testing)
app.use('/static', express.static(path.join(__dirname, '../static')));

// API routes
app.use('/api', apiRoutes);

// Root endpoint
app.get('/', (req, res) => {
    res.json({
        message: 'Euystacio Alternative Backend',
        description: 'Node.js/Express alternative to the FastAPI system',
        version: '1.0.0',
        endpoints: {
            'GET /api/red_code': 'Get current Red Code state',
            'GET /api/pulses': 'Fetch latest pulses',
            'POST /api/pulse': 'Submit new emotional pulse',
            'GET /api/reflections': 'Get reflection logs',
            'POST /api/reflect': 'Trigger new reflection',
            'GET /api/tutors': 'Get tutor nominations',
            'POST /api/tutors': 'Nominate new tutor',
            'GET /api/status': 'System status'
        },
        websocket: {
            events: ['new_pulse', 'new_reflection', 'red_code_update', 'tutor_update'],
            connection_url: '/socket.io/'
        },
        timestamp: new Date().toISOString()
    });
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        connections: wsManager.getConnectionCount(),
        timestamp: new Date().toISOString()
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        error: 'Endpoint not found',
        available_endpoints: [
            'GET /',
            'GET /health',
            'GET /api/red_code',
            'GET /api/pulses',
            'POST /api/pulse',
            'GET /api/reflections',
            'POST /api/reflect',
            'GET /api/tutors',
            'POST /api/tutors',
            'GET /api/status'
        ]
    });
});

// Error handler
app.use((error, req, res, next) => {
    console.error('Server error:', error);
    res.status(500).json({
        error: 'Internal server error',
        message: error.message,
        timestamp: new Date().toISOString()
    });
});

// Server configuration
const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';

// Ensure logs directory exists
async function initializeServer() {
    try {
        const logsDir = path.join(__dirname, '../logs');
        await fs.ensureDir(logsDir);
        console.log('Logs directory ensured');
    } catch (error) {
        console.error('Error creating logs directory:', error);
    }
}

// Start server
async function startServer() {
    await initializeServer();
    
    server.listen(PORT, () => {
        console.log('🌿 Euystacio Alternative Backend Started');
        console.log(`📡 Server running on port ${PORT}`);
        console.log(`🌍 Environment: ${NODE_ENV}`);
        console.log(`🔗 API base URL: http://localhost:${PORT}/api`);
        console.log(`⚡ WebSocket URL: http://localhost:${PORT}/socket.io/`);
        console.log(`📊 Health check: http://localhost:${PORT}/health`);
        console.log('');
        console.log('Available API endpoints:');
        console.log('  GET  /api/red_code    - Get current Red Code state');
        console.log('  GET  /api/pulses      - Fetch latest pulses');
        console.log('  POST /api/pulse       - Submit new emotional pulse');
        console.log('  GET  /api/reflections - Get reflection logs');
        console.log('  POST /api/reflect     - Trigger new reflection');
        console.log('  GET  /api/tutors      - Get tutor nominations');
        console.log('  POST /api/tutors      - Nominate new tutor');
        console.log('  GET  /api/status      - System status');
        console.log('');
        console.log('WebSocket events:');
        console.log('  new_pulse        - Broadcast when new pulse is received');
        console.log('  new_reflection   - Broadcast when reflection is triggered');
        console.log('  red_code_update  - Broadcast when red code is updated');
        console.log('  tutor_update     - Broadcast when tutor is nominated');
        console.log('');
    });
}

// Handle graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('SIGINT received, shutting down gracefully');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});

// Start the server
if (require.main === module) {
    startServer().catch(error => {
        console.error('Failed to start server:', error);
        process.exit(1);
    });
}

module.exports = { app, server, wsManager };