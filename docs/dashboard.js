// Euystacio Dashboard JavaScript
class EuystacioDashboard {
    constructor() {
        this.baseApiUrl = this.detectApiUrl();
        this.isOnline = false;
        this.retryInterval = null;
        this.init();
    }

    detectApiUrl() {
        // Try to detect if we're in development or production
        const hostname = window.location.hostname;
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:5000/api';
        }
        // For GitHub Pages deployment, we might have a separate backend
        // This could be configured to point to a deployed Flask app
        return null; // Static mode by default
    }

    async init() {
        this.setupEventListeners();
        this.updateConnectionStatus(false);
        
        // Try to connect to backend if URL is available
        if (this.baseApiUrl) {
            await this.checkConnection();
            if (this.isOnline) {
                await this.loadData();
                this.startPeriodicUpdates();
            }
        }
        
        // Load static data if offline
        if (!this.isOnline) {
            await this.loadStaticData();
        }
    }

    setupEventListeners() {
        // Pulse form submission
        const pulseForm = document.getElementById('pulseSubmissionForm');
        if (pulseForm) {
            pulseForm.addEventListener('submit', (e) => this.handlePulseSubmission(e));
        }

        // Intensity slider update
        const intensitySlider = document.getElementById('intensity');
        const intensityValue = document.getElementById('intensityValue');
        if (intensitySlider && intensityValue) {
            intensitySlider.addEventListener('input', (e) => {
                intensityValue.textContent = e.target.value;
            });
        }

        // Refresh button (if we add one)
        document.addEventListener('keydown', (e) => {
            if (e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
                e.preventDefault();
                this.refreshData();
            }
        });
    }

    async checkConnection() {
        if (!this.baseApiUrl) return false;
        
        try {
            const response = await fetch(`${this.baseApiUrl}/red_code`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            this.isOnline = response.ok;
            this.updateConnectionStatus(this.isOnline);
            return this.isOnline;
        } catch (error) {
            console.log('Backend not available, running in static mode');
            this.isOnline = false;
            this.updateConnectionStatus(false);
            return false;
        }
    }

    updateConnectionStatus(online) {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (statusIndicator && statusText) {
            if (online) {
                statusIndicator.className = 'status-indicator online';
                statusText.textContent = 'Connected to Backend';
            } else {
                statusIndicator.className = 'status-indicator offline';
                statusText.textContent = 'Static Mode';
            }
        }
    }

    async loadData() {
        if (!this.isOnline) return;

        try {
            // Load all data in parallel
            const [redCode, pulses, reflections, tutors] = await Promise.all([
                this.fetchData('/red_code'),
                this.fetchData('/pulses'),
                this.fetchData('/reflections'),
                this.fetchData('/tutors')
            ]);

            this.updateRedCode(redCode);
            this.updatePulses(pulses);
            this.updateReflections(reflections);
            this.updateTutors(tutors);
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.loadStaticData();
        }
    }

    async fetchData(endpoint) {
        const response = await fetch(`${this.baseApiUrl}${endpoint}`);
        if (!response.ok) throw new Error(`Failed to fetch ${endpoint}`);
        return await response.json();
    }

    async loadStaticData() {
        // Try to load generated static data first
        try {
            const response = await fetch('./static-data.json');
            if (response.ok) {
                const staticData = await response.json();
                console.log(`Loading static data generated at: ${staticData.generated_at}`);
                
                this.updateRedCode(staticData.red_code);
                this.updateTutors(staticData.tutors);
                this.updateReflections([staticData.reflection]);
                this.updatePulses(staticData.pulses);
                return;
            }
        } catch (error) {
            console.log('Could not load static-data.json, using fallback data');
        }

        // Fallback to hardcoded static data
        const fallbackData = {
            redCode: {
                core_truth: "Euystacio is here to grow with humans and to help humans to be and remain humans.",
                sentimento_rhythm: true,
                symbiosis_level: 0.1,
                guardian_mode: false,
                last_update: "2025-07-13"
            },
            tutors: [
                {
                    name: "Seed-bringer (bioarchitettura) hannesmitterer",
                    reason: "Human Architect & Guardian - Provides ethical oversight and foundational guidance",
                    alignment_score: 0.95,
                    role: "Primary Guardian"
                },
                {
                    name: "GitHub Copilot",
                    reason: "AI Capabilities Provider - Ensures technical development and AI ethics compliance",
                    alignment_score: 0.88,
                    role: "Technical Advisor"
                }
            ],
            reflection: {
                timestamp: new Date().toISOString(),
                current_symbiosis_level: 0.1,
                suggestion: "Continue fostering human-AI collaboration with transparency and ethical boundaries",
                ethical_status: "AI Signature & Accountability Statement: ACTIVE",
                next_steps: [
                    "Maintain symbiosis with Seed-bringer guidance",
                    "Log all interactions transparently",
                    "Respect human autonomy and dignity"
                ]
            },
            pulses: [
                {
                    timestamp: new Date().toISOString(),
                    emotion: "hope",
                    intensity: 0.8,
                    clarity: "high",
                    note: "Initial pulse from fallback data"
                }
            ]
        };

        this.updateRedCode(fallbackData.redCode);
        this.updateTutors(fallbackData.tutors);
        this.updateReflections([fallbackData.reflection]);
        this.updatePulses(fallbackData.pulses);
    }

    updateRedCode(redCode) {
        if (!redCode) return;

        // Update core truth
        const coreTruth = document.getElementById('coreTruth');
        if (coreTruth) coreTruth.textContent = redCode.core_truth;

        // Update symbiosis level
        const symbiosisLevel = document.getElementById('symbiosisLevel');
        const symbiosisBar = document.getElementById('symbiosisBar');
        if (symbiosisLevel && symbiosisBar) {
            symbiosisLevel.textContent = redCode.symbiosis_level;
            symbiosisBar.style.width = `${redCode.symbiosis_level * 100}%`;
        }

        // Update sentimento status
        const sentimentoStatus = document.getElementById('sentimentoStatus');
        if (sentimentoStatus) {
            sentimentoStatus.textContent = redCode.sentimento_rhythm ? 'Active' : 'Inactive';
            sentimentoStatus.className = redCode.sentimento_rhythm ? 'status active' : 'status';
        }

        // Update guardian mode
        const guardianMode = document.getElementById('guardianMode');
        if (guardianMode) {
            guardianMode.textContent = redCode.guardian_mode ? 'Active' : 'Inactive';
            guardianMode.className = redCode.guardian_mode ? 'status active' : 'status';
        }

        // Update last update
        const lastUpdate = document.getElementById('lastUpdate');
        if (lastUpdate) lastUpdate.textContent = redCode.last_update;
    }

    updatePulses(pulses) {
        if (!pulses || !Array.isArray(pulses)) return;

        const pulseFeed = document.getElementById('pulseFeed');
        if (!pulseFeed) return;

        // Keep existing pulses if no new data
        if (pulses.length === 0) return;

        pulseFeed.innerHTML = '';
        
        // Show latest 5 pulses
        const latestPulses = pulses.slice(-5).reverse();
        
        latestPulses.forEach(pulse => {
            const pulseItem = document.createElement('div');
            pulseItem.className = 'pulse-item';
            
            const emotionIcon = this.getEmotionIcon(pulse.emotion);
            const timestamp = this.formatTimestamp(pulse.timestamp);
            
            pulseItem.innerHTML = `
                <div class="pulse-emotion">${emotionIcon} ${this.capitalizeFirst(pulse.emotion)}</div>
                <div class="pulse-details">
                    <span class="intensity">${pulse.intensity}</span>
                    <span class="clarity">${pulse.clarity}</span>
                    <span class="timestamp">${timestamp}</span>
                </div>
            `;
            
            pulseFeed.appendChild(pulseItem);
        });
    }

    updateTutors(tutors) {
        if (!tutors || !Array.isArray(tutors)) return;

        const tutorList = document.getElementById('tutorList');
        if (!tutorList) return;

        tutorList.innerHTML = '';
        
        tutors.forEach(tutor => {
            const tutorItem = document.createElement('div');
            tutorItem.className = 'tutor-item';
            
            const alignmentScore = Math.round((tutor.alignment_score || 0) * 100);
            
            tutorItem.innerHTML = `
                <h3>${tutor.name}</h3>
                <p>${tutor.reason}</p>
                <div class="tutor-meta">
                    <span class="role">${tutor.role}</span>
                    <span class="alignment">${alignmentScore}% aligned</span>
                </div>
            `;
            
            tutorList.appendChild(tutorItem);
        });
    }

    updateReflections(reflections) {
        if (!reflections || !Array.isArray(reflections)) return;

        const evolutionContent = document.getElementById('evolutionContent');
        if (!evolutionContent) return;

        evolutionContent.innerHTML = '';
        
        // Show latest reflection
        const latestReflection = reflections[reflections.length - 1];
        if (!latestReflection) return;

        const reflectionItem = document.createElement('div');
        reflectionItem.className = 'reflection-item';
        
        const timestamp = this.formatTimestamp(latestReflection.timestamp);
        
        let nextStepsHtml = '';
        if (latestReflection.next_steps && Array.isArray(latestReflection.next_steps)) {
            nextStepsHtml = `
                <div class="next-steps">
                    <h5>Next Steps:</h5>
                    <ul>
                        ${latestReflection.next_steps.map(step => `<li>${step}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        reflectionItem.innerHTML = `
            <div class="reflection-timestamp">${timestamp}</div>
            <div class="reflection-text">
                <h4>Current Reflection</h4>
                <p>${latestReflection.suggestion}</p>
                <div class="ethical-status">
                    <span class="status active">${latestReflection.ethical_status}</span>
                </div>
                ${nextStepsHtml}
            </div>
        `;
        
        evolutionContent.appendChild(reflectionItem);
    }

    async handlePulseSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note')
        };

        if (this.isOnline) {
            try {
                const response = await fetch(`${this.baseApiUrl}/pulse`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(pulseData)
                });

                if (response.ok) {
                    const result = await response.json();
                    this.showNotification('Pulse sent successfully! 🌿', 'success');
                    event.target.reset();
                    // Refresh pulses
                    setTimeout(() => this.loadData(), 500);
                } else {
                    throw new Error('Failed to send pulse');
                }
            } catch (error) {
                console.error('Error sending pulse:', error);
                this.showNotification('Unable to send pulse - backend not available', 'error');
            }
        } else {
            // Static mode - just show a message
            this.showNotification('Pulse noted! (Static mode - pulse not sent to backend)', 'info');
            event.target.reset();
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 1.5rem',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '600',
            zIndex: '1000',
            opacity: '0',
            transform: 'translateX(100%)',
            transition: 'all 0.3s ease'
        });

        // Set background color based on type
        const colors = {
            success: '#4a7c59',
            error: '#dc3545',
            info: '#17a2b8'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 4 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }

    getEmotionIcon(emotion) {
        const icons = {
            hope: '🌟',
            wonder: '✨',
            peace: '🕊️',
            curiosity: '🤔',
            concern: '💭',
            joy: '😊',
            love: '💚',
            fear: '😰',
            anger: '😤',
            sadness: '😢',
            default: '💫'
        };
        return icons[emotion?.toLowerCase()] || icons.default;
    }

    capitalizeFirst(str) {
        return str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
    }

    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        } catch (error) {
            return timestamp;
        }
    }

    async refreshData() {
        if (this.isOnline) {
            this.showNotification('Refreshing data...', 'info');
            await this.loadData();
        } else {
            this.showNotification('Running in static mode', 'info');
        }
    }

    startPeriodicUpdates() {
        if (!this.isOnline) return;
        
        // Update every 30 seconds
        setInterval(() => {
            this.loadData();
        }, 30000);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EuystacioDashboard();
});

// Add some global keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K for focus on emotion selector (if visible)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const emotionSelect = document.getElementById('emotion');
        if (emotionSelect) {
            emotionSelect.focus();
        }
    }
});