// Euystacio Dashboard JavaScript with Real-time WebSocket Support
class EuystacioDashboard {
    constructor() {
        this.socket = null;
        this.init();
    }

    init() {
        this.setupWebSocket();
        this.setupEventListeners();
        this.loadInitialData();
        this.setupAutoRefresh();
    }

    setupWebSocket() {
        // Check if Socket.IO is available
        if (typeof io === 'undefined') {
            console.warn('Socket.IO not available, falling back to polling mode');
            this.showMessage('Running in fallback mode (WebSocket unavailable)', 'warning');
            return;
        }
        
        // Initialize Socket.IO connection
        this.socket = io();
        
        // Connection events
        this.socket.on('connect', () => {
            console.log('🌿 Connected to Euystacio real-time interface');
            this.showMessage('Connected to real-time updates! 🌱', 'success');
            // Request current state on connection
            this.socket.emit('request_current_state');
        });

        this.socket.on('disconnect', () => {
            console.log('🍃 Disconnected from real-time interface');
            this.showMessage('Real-time connection lost. Retrying...', 'warning');
        });

        this.socket.on('connection_status', (data) => {
            console.log('Connection status:', data);
        });

        // Real-time data updates
        this.socket.on('new_pulse', (pulse) => {
            console.log('🌿 New pulse received:', pulse);
            this.showMessage(`New pulse: ${pulse.emotion} (${pulse.intensity}) 🌸`, 'info');
            this.addPulseToDisplay(pulse);
        });

        this.socket.on('new_reflection', (reflection) => {
            console.log('🌸 New reflection received:', reflection);
            this.showMessage('New reflection generated! 🌸', 'info');
            this.addReflectionToDisplay(reflection);
        });

        this.socket.on('pulses_update', (pulses) => {
            this.displayPulses(pulses);
        });

        this.socket.on('reflections_update', (reflections) => {
            this.displayReflections(reflections);
        });

        this.socket.on('red_code_update', (redCode) => {
            this.displayRedCode(redCode);
        });

        this.socket.on('tutors_update', (tutors) => {
            this.displayTutors(tutors);
        });
    }

    setupEventListeners() {
        // Pulse form submission
        const pulseForm = document.getElementById('pulse-form');
        if (pulseForm) {
            pulseForm.addEventListener('submit', (e) => this.handlePulseSubmission(e));
        }

        // Intensity slider
        const intensitySlider = document.getElementById('intensity');
        const intensityValue = document.getElementById('intensity-value');
        if (intensitySlider && intensityValue) {
            intensitySlider.addEventListener('input', (e) => {
                intensityValue.textContent = e.target.value;
            });
        }

        // Reflection button
        const reflectBtn = document.getElementById('reflect-btn');
        if (reflectBtn) {
            reflectBtn.addEventListener('click', () => this.triggerReflection());
        }
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadRedCode(),
                this.loadPulses(),
                this.loadTutors(),
                this.loadReflections()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async loadRedCode() {
        try {
            const response = await fetch('/api/red_code');
            const redCode = await response.json();
            this.displayRedCode(redCode);
        } catch (error) {
            console.error('Error loading red code:', error);
            this.showError('red-code', 'Failed to load red code');
        }
    }

    displayRedCode(redCode) {
        const container = document.getElementById('red-code');
        if (!container) return;

        container.innerHTML = `
            <p><strong>Core Truth:</strong> ${redCode.core_truth || 'Not defined'}</p>
            <p><strong>Sentimento Rhythm:</strong> ${redCode.sentimento_rhythm ? 'Active' : 'Inactive'}</p>
            <p><strong>Symbiosis Level:</strong> ${redCode.symbiosis_level || 0}</p>
            <p><strong>Guardian Mode:</strong> ${redCode.guardian_mode ? 'On' : 'Off'}</p>
            <p><strong>Last Update:</strong> ${redCode.last_update || 'Unknown'}</p>
        `;

        // Update symbiosis meter
        const symbiosisBar = document.getElementById('symbiosis-bar');
        const symbiosisValue = document.getElementById('symbiosis-value');
        if (symbiosisBar && symbiosisValue) {
            const level = (redCode.symbiosis_level || 0) * 100;
            symbiosisBar.style.width = `${level}%`;
            symbiosisValue.textContent = redCode.symbiosis_level || '0.0';
        }
    }

    async loadPulses() {
        try {
            const response = await fetch('/api/pulses');
            const pulses = await response.json();
            this.displayPulses(pulses);
        } catch (error) {
            console.error('Error loading pulses:', error);
            this.showError('pulses-list', 'Failed to load pulses');
        }
    }

    displayPulses(pulses) {
        const container = document.getElementById('pulses-list');
        if (!container) return;

        if (!pulses || pulses.length === 0) {
            container.innerHTML = '<div class="loading">No pulses yet. Send the first one!</div>';
            return;
        }

        // Sort pulses by timestamp (most recent first) and show only the 10 most recent
        const sortedPulses = pulses.sort((a, b) => 
            new Date(b.timestamp || 0) - new Date(a.timestamp || 0)
        ).slice(0, 10);

        container.innerHTML = sortedPulses.map(pulse => `
            <div class="pulse-item" data-timestamp="${pulse.timestamp}">
                <div class="pulse-emotion">${pulse.emotion || 'Unknown'}</div>
                <div class="pulse-meta">
                    Intensity: ${pulse.intensity || 0} | 
                    Clarity: ${pulse.clarity || 'unknown'} | 
                    ${this.formatTimestamp(pulse.timestamp)}
                </div>
                ${pulse.note ? `<div class="pulse-note">"${pulse.note}"</div>` : ''}
            </div>
        `).join('');
    }

    addPulseToDisplay(pulse) {
        const container = document.getElementById('pulses-list');
        if (!container) return;

        // Create new pulse element
        const pulseElement = document.createElement('div');
        pulseElement.className = 'pulse-item new-pulse';
        pulseElement.setAttribute('data-timestamp', pulse.timestamp);
        pulseElement.innerHTML = `
            <div class="pulse-emotion">${pulse.emotion || 'Unknown'}</div>
            <div class="pulse-meta">
                Intensity: ${pulse.intensity || 0} | 
                Clarity: ${pulse.clarity || 'unknown'} | 
                ${this.formatTimestamp(pulse.timestamp)}
            </div>
            ${pulse.note ? `<div class="pulse-note">"${pulse.note}"</div>` : ''}
        `;

        // Add to the top of the list
        if (container.querySelector('.loading')) {
            container.innerHTML = '';
        }
        container.insertBefore(pulseElement, container.firstChild);

        // Remove the 'new-pulse' class after animation
        setTimeout(() => {
            pulseElement.classList.remove('new-pulse');
        }, 2000);

        // Keep only 10 items
        const items = container.querySelectorAll('.pulse-item');
        if (items.length > 10) {
            items[items.length - 1].remove();
        }
    }

    async loadTutors() {
        try {
            const response = await fetch('/api/tutors');
            const tutors = await response.json();
            this.displayTutors(tutors);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.showError('tutors-list', 'Failed to load tutor nominations');
        }
    }

    displayTutors(tutors) {
        const container = document.getElementById('tutors-list');
        if (!container) return;

        if (!tutors || tutors.length === 0) {
            container.innerHTML = '<div class="loading">No tutor nominations yet.</div>';
            return;
        }

        container.innerHTML = tutors.map(tutor => `
            <div class="tutor-item">
                <div class="tutor-name">${tutor.name || 'Anonymous Tutor'}</div>
                <div class="tutor-reason">${tutor.reason || 'Nominated for wisdom and guidance'}</div>
            </div>
        `).join('');
    }

    async loadReflections() {
        try {
            const response = await fetch('/api/reflections');
            const reflections = await response.json();
            this.displayReflections(reflections);
        } catch (error) {
            console.error('Error loading reflections:', error);
            this.showError('reflections-list', 'Failed to load reflections');
        }
    }

    displayReflections(reflections) {
        const container = document.getElementById('reflections-list');
        if (!container) return;

        if (!reflections || reflections.length === 0) {
            container.innerHTML = '<div class="loading">No reflections yet. Trigger the first one!</div>';
            return;
        }

        // Sort reflections by timestamp (most recent first) and show only the 5 most recent
        const sortedReflections = reflections.sort((a, b) => 
            new Date(b.timestamp || 0) - new Date(a.timestamp || 0)
        ).slice(0, 5);

        container.innerHTML = sortedReflections.map(reflection => `
            <div class="reflection-item" data-timestamp="${reflection.timestamp}">
                <div class="reflection-timestamp">${this.formatTimestamp(reflection.timestamp)}</div>
                <div class="reflection-content">${this.formatReflectionContent(reflection)}</div>
            </div>
        `).join('');
    }

    addReflectionToDisplay(reflection) {
        const container = document.getElementById('reflections-list');
        if (!container) return;

        // Create new reflection element
        const reflectionElement = document.createElement('div');
        reflectionElement.className = 'reflection-item new-reflection';
        reflectionElement.setAttribute('data-timestamp', reflection.timestamp);
        reflectionElement.innerHTML = `
            <div class="reflection-timestamp">${this.formatTimestamp(reflection.timestamp)}</div>
            <div class="reflection-content">${this.formatReflectionContent(reflection)}</div>
        `;

        // Add to the top of the list
        if (container.querySelector('.loading')) {
            container.innerHTML = '';
        }
        container.insertBefore(reflectionElement, container.firstChild);

        // Remove the 'new-reflection' class after animation
        setTimeout(() => {
            reflectionElement.classList.remove('new-reflection');
        }, 2000);

        // Keep only 5 items
        const items = container.querySelectorAll('.reflection-item');
        if (items.length > 5) {
            items[items.length - 1].remove();
        }
    }

    formatReflectionContent(reflection) {
        if (reflection.suggestion) {
            return `
                <div class="reflection-suggestion">${reflection.suggestion}</div>
                ${reflection.ethical_status ? `<div class="reflection-ethics">${reflection.ethical_status}</div>` : ''}
                ${reflection.next_steps ? `<div class="reflection-steps">Next: ${reflection.next_steps.join(', ')}</div>` : ''}
            `;
        }
        return reflection.content || JSON.stringify(reflection, null, 2);
    }

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
                
                // Refresh pulses and red code
                setTimeout(() => {
                    this.loadPulses();
                    this.loadRedCode();
                }, 500);
            } else {
                throw new Error('Failed to send pulse');
            }
        } catch (error) {
            console.error('Error sending pulse:', error);
            this.showMessage('Failed to send pulse. Please try again.', 'error');
        }
    }

    async triggerReflection() {
        const button = document.getElementById('reflect-btn');
        if (!button) return;

        button.disabled = true;
        button.textContent = 'Reflecting...';

        try {
            const response = await fetch('/api/reflect');
            if (response.ok) {
                const reflection = await response.json();
                this.showMessage('Reflection triggered successfully! 🌸', 'success');
                
                // Refresh reflections and red code
                setTimeout(() => {
                    this.loadReflections();
                    this.loadRedCode();
                }, 1000);
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

    setupAutoRefresh() {
        // Determine refresh intervals based on WebSocket availability
        const hasWebSocket = this.socket && this.socket.connected;
        const shortInterval = hasWebSocket ? 120000 : 30000; // 2min with WS, 30s without
        const longInterval = hasWebSocket ? 300000 : 120000; // 5min with WS, 2min without
        
        // Refresh data periodically
        setInterval(() => {
            if (!this.socket || !this.socket.connected) {
                console.log('Using fallback polling for updates...');
                this.loadPulses();
                this.loadRedCode();
            }
        }, shortInterval);

        // Refresh reflections and tutors
        setInterval(() => {
            if (!this.socket || !this.socket.connected) {
                this.loadReflections();
                this.loadTutors();
            }
        }, longInterval);
    }

    showMessage(message, type = 'info') {
        // Create or update message element
        let messageEl = document.querySelector('.message');
        if (!messageEl) {
            messageEl = document.createElement('div');
            messageEl.className = 'message';
            document.querySelector('.pulse-form').appendChild(messageEl);
        }

        messageEl.className = `message ${type}`;
        messageEl.textContent = message;

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.parentNode.removeChild(messageEl);
            }
        }, 5000);
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `<div class="error">${message}</div>`;
        }
    }

    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown time';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleString();
        } catch (error) {
            return timestamp;
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EuystacioDashboard();
});

// Add some utility functions for better UX
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling for better navigation
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Add loading indicators
    const addLoadingToButtons = () => {
        document.querySelectorAll('button[type="submit"]').forEach(button => {
            button.addEventListener('click', function() {
                if (this.form && this.form.checkValidity()) {
                    this.classList.add('loading');
                    setTimeout(() => this.classList.remove('loading'), 2000);
                }
            });
        });
    };
    
    addLoadingToButtons();
});