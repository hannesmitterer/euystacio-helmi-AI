// Euystacio Sentimento Kernel - Interactive Interface
class EuystacioInterface {
    constructor() {
        this.isLoading = false;
        this.init();
    }

    init() {
        this.loadInitialData();
        this.setupEventListeners();
        this.setupResponsiveHandlers();
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadRedCodeStatus(),
                this.loadTutorStatus(),
                this.loadReflectionStatus(),
                this.loadPulseHistory()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showError('Failed to load some components. Please refresh the page.');
        }
    }

    async loadRedCodeStatus() {
        try {
            const response = await fetch('/api/red_code');
            if (!response.ok) throw new Error('Failed to load red code');
            
            const redCode = await response.json();
            const statusElement = document.getElementById('red-code-status');
            
            statusElement.innerHTML = `
                <div class="status-item">
                    <strong>Core Truth:</strong> ${redCode.core_truth || 'Loading...'}
                </div>
                <div class="status-item">
                    <strong>Symbiosis Level:</strong> ${(redCode.symbiosis_level * 100).toFixed(1)}%
                </div>
                <div class="status-item">
                    <strong>Last Update:</strong> ${redCode.last_update || 'Unknown'}
                </div>
            `;
            statusElement.classList.remove('loading');
        } catch (error) {
            console.error('Error loading red code:', error);
            this.updateElementSafely('red-code-status', 'Error loading red code status');
        }
    }

    async loadTutorStatus() {
        try {
            const response = await fetch('/api/tutors');
            if (!response.ok) throw new Error('Failed to load tutors');
            
            const tutors = await response.json();
            const statusElement = document.getElementById('tutor-status');
            
            if (tutors && tutors.length > 0) {
                statusElement.innerHTML = `
                    <div class="tutor-list">
                        ${tutors.map(tutor => `
                            <div class="tutor-item">
                                <strong>${tutor.name || 'Anonymous'}</strong>
                                <span class="resonance">Resonance: ${tutor.resonance || 'Unknown'}</span>
                            </div>
                        `).join('')}
                    </div>
                `;
            } else {
                statusElement.innerHTML = '<div class="status-item">No active tutors</div>';
            }
            statusElement.classList.remove('loading');
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.updateElementSafely('tutor-status', 'Error loading tutor status');
        }
    }

    async loadReflectionStatus() {
        try {
            const response = await fetch('/api/reflect');
            if (!response.ok) throw new Error('Failed to load reflection');
            
            const reflection = await response.json();
            const statusElement = document.getElementById('reflection-status');
            
            statusElement.innerHTML = `
                <div class="reflection-item">
                    <strong>Suggestion:</strong> ${reflection.suggestion || 'No suggestions'}
                </div>
                <div class="reflection-item">
                    <strong>Ethical Status:</strong> ${reflection.ethical_status || 'Unknown'}
                </div>
                <div class="reflection-item">
                    <strong>Last Reflection:</strong> ${this.formatTimestamp(reflection.timestamp)}
                </div>
            `;
            statusElement.classList.remove('loading');
        } catch (error) {
            console.error('Error loading reflection:', error);
            this.updateElementSafely('reflection-status', 'Error loading reflection status');
        }
    }

    async loadPulseHistory() {
        try {
            const response = await fetch('/api/pulses');
            if (!response.ok) throw new Error('Failed to load pulses');
            
            const pulses = await response.json();
            const historyElement = document.getElementById('pulse-history');
            
            if (pulses && pulses.length > 0) {
                const recentPulses = pulses.slice(-5); // Show last 5 pulses
                historyElement.innerHTML = recentPulses.map(pulse => `
                    <div class="pulse-item">
                        <span class="pulse-emotion">${pulse.emotion}</span>
                        <span class="pulse-intensity">Intensity: ${pulse.intensity}</span>
                        <span class="pulse-time">${this.formatTimestamp(pulse.timestamp)}</span>
                    </div>
                `).join('');
            } else {
                historyElement.innerHTML = '<div class="no-pulses">No recent pulses</div>';
            }
        } catch (error) {
            console.error('Error loading pulse history:', error);
            this.updateElementSafely('pulse-history', 'Error loading pulse history');
        }
    }

    async sendPulse() {
        if (this.isLoading) return;

        // Simple pulse sending - in a real implementation, this could be a modal with emotion selection
        const emotions = ['joy', 'curiosity', 'calm', 'wonder', 'gratitude', 'hope'];
        const emotion = emotions[Math.floor(Math.random() * emotions.length)];
        const intensity = Math.random() * 0.5 + 0.3; // 0.3 to 0.8
        
        try {
            this.isLoading = true;
            const response = await fetch('/api/pulse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    emotion: emotion,
                    intensity: intensity,
                    clarity: 'medium',
                    note: 'Sent from web interface'
                })
            });

            if (!response.ok) throw new Error('Failed to send pulse');
            
            const result = await response.json();
            
            // Show feedback
            this.showPulseFeedback(result);
            
            // Reload pulse history
            await this.loadPulseHistory();
            
        } catch (error) {
            console.error('Error sending pulse:', error);
            this.showError('Failed to send pulse. Please try again.');
        } finally {
            this.isLoading = false;
        }
    }

    showPulseFeedback(pulse) {
        const button = document.querySelector('.pulse-interface button');
        const originalText = button.textContent;
        
        button.textContent = `Sent: ${pulse.emotion}`;
        button.style.background = '#27ae60';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '#3498db';
        }, 2000);
    }

    showError(message) {
        // Simple error display - could be enhanced with a proper notification system
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 5px;
            z-index: 1000;
            max-width: 300px;
        `;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    setupEventListeners() {
        // Set up periodic updates
        setInterval(() => {
            this.loadReflectionStatus();
            this.loadPulseHistory();
        }, 30000); // Update every 30 seconds

        // Handle visibility change to refresh when tab becomes active
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.loadInitialData();
            }
        });
    }

    setupResponsiveHandlers() {
        // Handle window resize for responsive adjustments
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 250);
        });
    }

    handleResize() {
        // Responsive adjustments if needed
        const components = document.querySelectorAll('.component');
        components.forEach(component => {
            // Ensure components maintain proper spacing on resize
            component.style.transition = 'all 0.3s ease';
        });
    }

    updateElementSafely(elementId, content) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = content;
            element.classList.remove('loading');
        }
    }

    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleString();
        } catch (error) {
            return 'Invalid date';
        }
    }
}

// Global function for the pulse button
function sendPulse() {
    if (window.euystacioInterface) {
        window.euystacioInterface.sendPulse();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add loading class to status elements
    const statusElements = ['red-code-status', 'tutor-status', 'reflection-status'];
    statusElements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.add('loading');
            element.textContent = 'Loading...';
        }
    });

    // Initialize the interface
    window.euystacioInterface = new EuystacioInterface();
});

// Service Worker registration for offline capability (Progressive Web App)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
        try {
            // This would register a service worker if we create one
            // await navigator.serviceWorker.register('/sw.js');
            console.log('Service worker registration capability detected');
        } catch (error) {
            console.log('Service worker registration not available');
        }
    });
}