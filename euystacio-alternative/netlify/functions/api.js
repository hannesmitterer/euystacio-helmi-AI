/**
 * netlify-adapter.js
 * Adapter to convert Express routes to Netlify Functions
 */

const express = require('express');
const serverless = require('serverless-http');

// Import our API routes
const apiRoutes = require('../src/api/routes');

// Create Express app for Netlify Functions
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Add mock socket.io for Netlify Functions (since WebSocket isn't supported)
app.use((req, res, next) => {
    // Mock socket.io object for compatibility
    req.io = {
        emit: (event, data) => {
            console.log(`[Netlify] Would emit WebSocket event: ${event}`, data);
            // In Netlify Functions, we can't use WebSocket
            // Instead, you could integrate with Netlify's real-time capabilities
            // or use a third-party service like Pusher or Ably
        }
    };
    next();
});

// Use API routes with /.netlify/functions/api prefix
app.use('/.netlify/functions/api', apiRoutes);

// Root function response
app.get('/.netlify/functions/api', (req, res) => {
    res.json({
        message: 'Euystacio Alternative Backend (Netlify Functions)',
        description: 'Node.js/Express API adapted for Netlify Functions deployment',
        version: '1.0.0',
        note: 'WebSocket functionality is not available in Netlify Functions. Consider using Netlify\'s real-time features or third-party services.',
        endpoints: {
            'GET /.netlify/functions/api/red_code': 'Get current Red Code state',
            'GET /.netlify/functions/api/pulses': 'Fetch latest pulses',
            'POST /.netlify/functions/api/pulse': 'Submit new emotional pulse',
            'GET /.netlify/functions/api/reflections': 'Get reflection logs',
            'POST /.netlify/functions/api/reflect': 'Trigger new reflection',
            'GET /.netlify/functions/api/tutors': 'Get tutor nominations',
            'POST /.netlify/functions/api/tutors': 'Nominate new tutor',
            'GET /.netlify/functions/api/status': 'System status'
        },
        timestamp: new Date().toISOString()
    });
});

// Export the serverless function
exports.handler = serverless(app);