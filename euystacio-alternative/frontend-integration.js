/**
 * frontend-integration.js
 * Example code for integrating Socket.IO client on the frontend
 * This file shows how to modify the existing interface.js to use WebSocket updates
 */

// Example integration for the existing Euystacio dashboard
// Add this to your existing interface.js or create a new file

class EuystacioDashboardWithWebSocket extends EuystacioDashboard {
    constructor() {
        super();
        this.initializeWebSocket();
    }

    /**
     * Initialize WebSocket connection for real-time updates
     */
    initializeWebSocket() {
        // Import socket.io-client in your HTML:
        // <script src="https://cdn.socket.io/4.7.4/socket.io.min.js"></script>
        
        // Connect to the WebSocket server
        this.socket = io(window.location.origin, {
            transports: ['websocket', 'polling']
        });

        // Connection events
        this.socket.on('connect', () => {
            console.log('🌿 Connected to Euystacio real-time updates');
            this.showMessage('Connected to real-time updates', 'success');
        });

        this.socket.on('disconnect', (reason) => {
            console.log('❌ Disconnected from real-time updates:', reason);
            this.showMessage('Disconnected from real-time updates', 'warning');
        });

        this.socket.on('connect_error', (error) => {
            console.error('Connection error:', error);
            this.showMessage('Failed to connect to real-time updates', 'error');
        });

        // Listen for real-time events
        this.setupWebSocketListeners();
    }

    /**
     * Set up listeners for WebSocket events
     */
    setupWebSocketListeners() {
        // Listen for new pulses
        this.socket.on('new_pulse', (data) => {
            console.log('📡 New pulse received:', data);
            this.handleNewPulse(data.data || data);
        });

        // Listen for new reflections
        this.socket.on('new_reflection', (data) => {
            console.log('🧠 New reflection received:', data);
            this.handleNewReflection(data.data || data);
        });

        // Listen for red code updates
        this.socket.on('red_code_update', (data) => {
            console.log('🔴 Red code updated:', data);
            this.handleRedCodeUpdate(data.data || data);
        });

        // Listen for tutor updates
        this.socket.on('tutor_update', (data) => {
            console.log('👨‍🏫 Tutor update:', data);
            this.handleTutorUpdate(data.data || data);
        });

        // Connection establishment
        this.socket.on('connection_established', (data) => {
            console.log('✅ Connection established:', data);
        });

        // Handle ping/pong for connection health
        this.socket.on('pong', (data) => {
            console.log('🏓 Pong received:', data);
        });
    }

    /**
     * Handle new pulse from WebSocket
     */
    handleNewPulse(pulse) {
        // Update the pulses display immediately
        this.loadPulses();
        
        // Show notification
        this.showMessage(`New pulse: ${pulse.emotion} (${pulse.intensity})`, 'info');
        
        // Optional: Add visual feedback like a gentle animation
        this.animateNewContent('pulses-list');
    }

    /**
     * Handle new reflection from WebSocket
     */
    handleNewReflection(reflection) {
        // Update reflections display
        this.loadReflections();
        
        // Show notification
        this.showMessage('New reflection generated', 'info');
        
        // Update red code as reflections might affect it
        this.loadRedCode();
        
        // Optional: Add visual feedback
        this.animateNewContent('reflections-list');
    }

    /**
     * Handle red code update from WebSocket
     */
    handleRedCodeUpdate(redCode) {
        // Update red code display immediately
        this.displayRedCode(redCode);
        
        // Show notification if significant change
        this.showMessage('Red code updated', 'info');
    }

    /**
     * Handle tutor update from WebSocket
     */
    handleTutorUpdate(tutor) {
        // Update tutors display
        this.loadTutors();
        
        // Show notification
        this.showMessage(`New tutor nominated: ${tutor.name}`, 'info');
        
        // Optional: Add visual feedback
        this.animateNewContent('tutors-list');
    }

    /**
     * Add visual feedback for new content
     */
    animateNewContent(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.transition = 'background-color 0.3s ease';
            element.style.backgroundColor = '#e8f5e8';
            setTimeout(() => {
                element.style.backgroundColor = '';
            }, 1000);
        }
    }

    /**
     * Override pulse submission to remove auto-refresh (WebSocket handles it)
     */
    async handlePulseSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note') || ''
        };

        if (!pulseData.emotion) {
            this.showMessage('Please select an emotion', 'error');
            return;
        }

        try {
            const response = await fetch('/api/pulse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(pulseData)
            });

            if (response.ok) {
                const result = await response.json();
                this.showMessage('Pulse sent successfully! 🌿', 'success');
                event.target.reset();
                document.getElementById('intensity-value').textContent = '0.5';
                
                // WebSocket will handle the updates automatically
                // No need for manual refresh
            } else {
                throw new Error('Failed to send pulse');
            }
        } catch (error) {
            console.error('Error sending pulse:', error);
            this.showMessage('Failed to send pulse. Please try again.', 'error');
        }
    }

    /**
     * Override reflection trigger to remove auto-refresh
     */
    async triggerReflection() {
        const button = document.getElementById('reflect-btn');
        if (!button) return;

        button.disabled = true;
        button.textContent = 'Reflecting...';

        try {
            const response = await fetch('/api/reflect', {
                method: 'POST'
            });
            
            if (response.ok) {
                const reflection = await response.json();
                this.showMessage('Reflection triggered successfully! 🌸', 'success');
                
                // WebSocket will handle the updates automatically
            } else {
                throw new Error('Failed to trigger reflection');
            }
        } catch (error) {
            console.error('Error triggering reflection:', error);
            this.showMessage('Failed to trigger reflection. Please try again.', 'error');
        } finally {
            button.disabled = false;
            button.textContent = 'Trigger Reflection';
        }
    }

    /**
     * Disable auto-refresh since WebSocket provides real-time updates
     */
    setupAutoRefresh() {
        // Disable auto-refresh - WebSocket provides real-time updates
        console.log('Auto-refresh disabled - using WebSocket for real-time updates');
        
        // Optional: Keep a minimal heartbeat for connection health
        setInterval(() => {
            if (this.socket && this.socket.connected) {
                this.socket.emit('ping');
            }
        }, 30000); // Every 30 seconds
    }

    /**
     * Request current state when connecting
     */
    requestCurrentState() {
        if (this.socket && this.socket.connected) {
            this.socket.emit('request_current_state');
        }
    }

    /**
     * Subscribe to specific event types
     */
    subscribeToEvents(eventTypes = ['pulses', 'reflections']) {
        if (this.socket && this.socket.connected) {
            this.socket.emit('subscribe', eventTypes);
        }
    }

    /**
     * Unsubscribe from specific event types
     */
    unsubscribeFromEvents(eventTypes) {
        if (this.socket && this.socket.connected) {
            this.socket.emit('unsubscribe', eventTypes);
        }
    }

    /**
     * Get connection status
     */
    getConnectionStatus() {
        return {
            connected: this.socket && this.socket.connected,
            id: this.socket ? this.socket.id : null
        };
    }
}

// Usage example:
// Replace the existing dashboard initialization with:
document.addEventListener('DOMContentLoaded', () => {
    // Use the WebSocket-enabled dashboard
    const dashboard = new EuystacioDashboardWithWebSocket();
    
    // Request current state when loaded
    setTimeout(() => {
        dashboard.requestCurrentState();
        dashboard.subscribeToEvents(['pulses', 'reflections']);
    }, 1000);
});

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EuystacioDashboardWithWebSocket;
}