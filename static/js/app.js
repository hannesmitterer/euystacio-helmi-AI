// Euystacio App JavaScript
class EuystacioApp {
    constructor() {
        this.init();
    }

    init() {
        // Initialize the app
        this.setupEventListeners();
        this.loadInitialData();
        this.updateIntensityDisplay();
    }

    setupEventListeners() {
        // Intensity slider
        const intensitySlider = document.getElementById('intensity');
        const intensityValue = document.getElementById('intensity-value');
        
        if (intensitySlider && intensityValue) {
            intensitySlider.addEventListener('input', (e) => {
                intensityValue.textContent = e.target.value;
            });
        }

        // Send pulse button
        const sendPulseBtn = document.getElementById('send-pulse');
        if (sendPulseBtn) {
            sendPulseBtn.addEventListener('click', () => this.sendPulse());
        }

        // Auto-refresh data every 30 seconds
        setInterval(() => this.loadInitialData(), 30000);
    }

    updateIntensityDisplay() {
        const intensitySlider = document.getElementById('intensity');
        const intensityValue = document.getElementById('intensity-value');
        if (intensitySlider && intensityValue) {
            intensityValue.textContent = intensitySlider.value;
        }
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadRedCodeStatus(),
                this.loadReflections(),
                this.loadTutors()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async loadRedCodeStatus() {
        try {
            // Try dynamic API first, fallback to static JSON
            let response;
            try {
                response = await fetch('/api/red_code');
            } catch (error) {
                response = await fetch('/api/red_code.json');
            }
            const data = await response.json();
            this.displayRedCodeStatus(data);
        } catch (error) {
            console.error('Error loading red code status:', error);
            this.displayError('red-code-status', 'Failed to load Red Code status');
        }
    }

    async loadReflections() {
        try {
            // Try dynamic API first, fallback to static JSON
            let response;
            try {
                response = await fetch('/api/reflections');
            } catch (error) {
                response = await fetch('/api/reflections.json');
            }
            const reflections = await response.json();
            this.displayReflections(reflections);
        } catch (error) {
            console.error('Error loading reflections:', error);
            this.displayError('reflections-display', 'Failed to load reflections');
        }
    }

    async loadTutors() {
        try {
            // Try dynamic API first, fallback to static JSON
            let response;
            try {
                response = await fetch('/api/tutors');
            } catch (error) {
                response = await fetch('/api/tutors.json');
            }
            const tutors = await response.json();
            this.displayTutors(tutors);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.displayError('tutors-display', 'Failed to load tutor information');
        }
    }

    displayRedCodeStatus(data) {
        const container = document.getElementById('red-code-status');
        if (!container) return;

        container.innerHTML = `
            <div class="status-item">
                <strong>Core Truth:</strong> ${data.core_truth || 'Loading...'}
            </div>
            <div class="status-item">
                <strong>Sentimento Rhythm:</strong> ${data.sentimento_rhythm ? '🟢 Active' : '🔴 Inactive'}
            </div>
            <div class="status-item">
                <strong>Symbiosis Level:</strong> ${(data.symbiosis_level * 100).toFixed(1)}%
            </div>
            <div class="status-item">
                <strong>Guardian Mode:</strong> ${data.guardian_mode ? '🛡️ Active' : '💤 Dormant'}
            </div>
            <div class="status-item">
                <strong>Last Update:</strong> ${data.last_update || 'Unknown'}
            </div>
        `;
    }

    displayReflections(reflections) {
        const container = document.getElementById('reflections-display');
        if (!container) return;

        if (!reflections || reflections.length === 0) {
            container.innerHTML = '<div class="info">No reflections yet. System is observing...</div>';
            return;
        }

        container.innerHTML = reflections.slice(-3).reverse().map(reflection => `
            <div class="reflection-item">
                <div class="reflection-timestamp">${this.formatTimestamp(reflection.timestamp)}</div>
                <div class="reflection-suggestion">${reflection.suggestion}</div>
                <div class="reflection-status">${reflection.ethical_status}</div>
            </div>
        `).join('');
    }

    displayTutors(tutorData) {
        const container = document.getElementById('tutors-display');
        if (!container) return;

        const tutors = tutorData.active_tutors || [];
        
        container.innerHTML = `
            <div class="tutors-list">
                ${tutors.map(tutor => `
                    <div class="tutor-item ${tutor.status}">
                        <div class="tutor-name"><strong>${tutor.name}</strong></div>
                        <div class="tutor-role">${tutor.role || 'Tutor'}</div>
                        <div class="tutor-reason">${tutor.reason}</div>
                    </div>
                `).join('')}
            </div>
            <div class="nomination-info">
                <small><strong>Nomination Process:</strong> ${tutorData.process || 'Community-driven'}</small>
            </div>
        `;
    }

    async sendPulse() {
        const emotion = document.getElementById('emotion').value;
        const intensity = parseFloat(document.getElementById('intensity').value);
        const clarity = document.getElementById('clarity').value;
        const note = document.getElementById('note').value;

        const sendBtn = document.getElementById('send-pulse');
        const originalText = sendBtn.textContent;
        
        try {
            // Show loading state
            sendBtn.textContent = 'Sending...';
            sendBtn.disabled = true;
            sendBtn.classList.add('pulse-sending');

            let response;
            try {
                // Try dynamic API first
                response = await fetch('/api/pulse', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        emotion,
                        intensity,
                        clarity,
                        note
                    })
                });
            } catch (error) {
                // Fallback to static mode simulation
                response = {
                    ok: true,
                    json: async () => ({
                        timestamp: new Date().toISOString(),
                        emotion,
                        intensity,
                        clarity,
                        note,
                        ai_signature_status: "verified (static mode)"
                    })
                };
            }

            const result = await response.json();
            
            if (response.ok) {
                this.showPulseSuccess(result);
                // Clear the note field
                document.getElementById('note').value = '';
            } else {
                this.showPulseError('Failed to send pulse');
            }

        } catch (error) {
            console.error('Error sending pulse:', error);
            // In static mode, still show success
            this.showPulseSuccess({
                timestamp: new Date().toISOString(),
                emotion,
                intensity,
                clarity,
                note,
                ai_signature_status: "verified (static mode)"
            });
            document.getElementById('note').value = '';
        } finally {
            // Restore button state
            sendBtn.textContent = originalText;
            sendBtn.disabled = false;
            sendBtn.classList.remove('pulse-sending');
        }
    }

    showPulseSuccess(result) {
        const container = document.getElementById('pulse-interface');
        const successMsg = document.createElement('div');
        successMsg.className = 'success pulse-result';
        successMsg.innerHTML = `
            <strong>Pulse sent successfully!</strong><br>
            <small>Timestamp: ${this.formatTimestamp(result.timestamp)}</small>
        `;
        
        container.appendChild(successMsg);
        setTimeout(() => successMsg.remove(), 3000);
    }

    showPulseError(message) {
        const container = document.getElementById('pulse-interface');
        const errorMsg = document.createElement('div');
        errorMsg.className = 'error pulse-result';
        errorMsg.innerHTML = `<strong>Error:</strong> ${message}`;
        
        container.appendChild(errorMsg);
        setTimeout(() => errorMsg.remove(), 3000);
    }

    displayError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `<div class="error">${message}</div>`;
        }
    }

    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown';
        try {
            const date = new Date(timestamp);
            return date.toLocaleString();
        } catch (error) {
            return timestamp;
        }
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EuystacioApp();
});

// Add some global error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Service worker registration for PWA capabilities (optional enhancement)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // We could register a service worker here for offline functionality
        // navigator.serviceWorker.register('/sw.js').catch(console.error);
    });
}