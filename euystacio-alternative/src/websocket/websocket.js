/**
 * websocket.js
 * WebSocket handling using Socket.IO for real-time updates
 */

const { Server } = require('socket.io');

class WebSocketManager {
    constructor(httpServer) {
        this.io = new Server(httpServer, {
            cors: {
                origin: "*",
                methods: ["GET", "POST"]
            }
        });

        this.setupEventHandlers();
    }

    setupEventHandlers() {
        this.io.on('connection', (socket) => {
            console.log(`Client connected: ${socket.id}`);

            // Send welcome message
            socket.emit('connection_established', {
                message: 'Connected to Euystacio real-time updates',
                timestamp: new Date().toISOString(),
                client_id: socket.id
            });

            // Handle client requests for current data
            socket.on('request_current_state', async () => {
                try {
                    // This would ideally get current state from the core modules
                    // For now, send a status update
                    socket.emit('current_state', {
                        message: 'Current state requested',
                        timestamp: new Date().toISOString(),
                        status: 'active'
                    });
                } catch (error) {
                    console.error('Error sending current state:', error);
                    socket.emit('error', { message: 'Failed to get current state' });
                }
            });

            // Handle ping/pong for connection health
            socket.on('ping', () => {
                socket.emit('pong', { timestamp: new Date().toISOString() });
            });

            // Handle subscription to specific events
            socket.on('subscribe', (eventTypes) => {
                if (Array.isArray(eventTypes)) {
                    eventTypes.forEach(eventType => {
                        socket.join(eventType);
                        console.log(`Client ${socket.id} subscribed to ${eventType}`);
                    });
                }
            });

            // Handle unsubscription
            socket.on('unsubscribe', (eventTypes) => {
                if (Array.isArray(eventTypes)) {
                    eventTypes.forEach(eventType => {
                        socket.leave(eventType);
                        console.log(`Client ${socket.id} unsubscribed from ${eventType}`);
                    });
                }
            });

            // Handle disconnection
            socket.on('disconnect', (reason) => {
                console.log(`Client disconnected: ${socket.id}, reason: ${reason}`);
            });

            // Handle errors
            socket.on('error', (error) => {
                console.error(`Socket error for client ${socket.id}:`, error);
            });
        });

        console.log('WebSocket server initialized');
    }

    /**
     * Broadcast a new pulse to all connected clients
     * @param {Object} pulse - The pulse data to broadcast
     */
    broadcastNewPulse(pulse) {
        console.log('Broadcasting new pulse to all clients');
        this.io.emit('new_pulse', {
            type: 'new_pulse',
            data: pulse,
            timestamp: new Date().toISOString()
        });

        // Also emit to subscribers of pulse events
        this.io.to('pulses').emit('pulse_update', {
            type: 'pulse_update',
            data: pulse,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Broadcast a new reflection to all connected clients
     * @param {Object} reflection - The reflection data to broadcast
     */
    broadcastNewReflection(reflection) {
        console.log('Broadcasting new reflection to all clients');
        this.io.emit('new_reflection', {
            type: 'new_reflection',
            data: reflection,
            timestamp: new Date().toISOString()
        });

        // Also emit to subscribers of reflection events
        this.io.to('reflections').emit('reflection_update', {
            type: 'reflection_update',
            data: reflection,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Broadcast red code updates
     * @param {Object} redCode - The updated red code data
     */
    broadcastRedCodeUpdate(redCode) {
        console.log('Broadcasting red code update to all clients');
        this.io.emit('red_code_update', {
            type: 'red_code_update',
            data: redCode,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Broadcast tutor nomination updates
     * @param {Object} tutor - The tutor data
     */
    broadcastTutorUpdate(tutor) {
        console.log('Broadcasting tutor update to all clients');
        this.io.emit('tutor_update', {
            type: 'tutor_update',
            data: tutor,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Send a custom message to all clients
     * @param {string} eventName - Name of the event
     * @param {Object} data - Data to send
     */
    broadcast(eventName, data) {
        this.io.emit(eventName, {
            type: eventName,
            data: data,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Send a message to a specific client
     * @param {string} socketId - Socket ID of the client
     * @param {string} eventName - Name of the event
     * @param {Object} data - Data to send
     */
    sendToClient(socketId, eventName, data) {
        this.io.to(socketId).emit(eventName, {
            type: eventName,
            data: data,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Get the socket.io instance
     * @returns {Server} Socket.IO server instance
     */
    getIO() {
        return this.io;
    }

    /**
     * Get connection count
     * @returns {number} Number of connected clients
     */
    getConnectionCount() {
        return this.io.engine.clientsCount;
    }

    /**
     * Get connected client IDs
     * @returns {Array} Array of connected socket IDs
     */
    getConnectedClients() {
        return Array.from(this.io.sockets.sockets.keys());
    }
}

module.exports = WebSocketManager;