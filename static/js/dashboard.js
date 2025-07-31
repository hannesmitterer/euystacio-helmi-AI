// Euystacio Dashboard JavaScript
// Handles dynamic content loading and form interactions

class EuystacioDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupIntensitySlider();
        this.loadDashboardData();
        this.setupPulseForm();
        this.startAutoRefresh();
    }

    setupIntensitySlider() {
        const intensitySlider = document.getElementById('intensity');
        const intensityValue = document.getElementById('intensity-value');
        
        if (intensitySlider && intensityValue) {
            intensitySlider.addEventListener('input', (e) => {
                intensityValue.textContent = e.target.value;
            });
        }
    }

    setupPulseForm() {
        const form = document.getElementById('pulse-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handlePulseSubmission(e));
        }
    }

    async handlePulseSubmission(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note') || ''
        };

        try {
            const response = await fetch('/api/pulse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(pulseData)
            });

            if (response.ok) {
                const result = await response.json();
                this.showMessage('Pulse sent successfully! Thank you for contributing to the rhythm.', 'success');
                e.target.reset();
                document.getElementById('intensity-value').textContent = '0.5';
                // Refresh pulses to show the new one
                setTimeout(() => this.loadPulses(), 1000);
            } else {
                throw new Error('Failed to send pulse');
            }
        } catch (error) {
            console.error('Error sending pulse:', error);
            this.showMessage('Failed to send pulse. Please try again.', 'error');
        }
    }

    showMessage(text, type) {
        // Remove any existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());

        // Create new message
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;

        // Insert before the form
        const form = document.querySelector('.contribution-form');
        if (form) {
            form.insertBefore(message, form.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (message.parentNode) {
                    message.remove();
                }
            }, 5000);
        }
    }

    async loadDashboardData() {
        await Promise.all([
            this.loadRedCode(),
            this.loadPulses(),
            this.loadTutors(),
            this.loadReflections()
        ]);
    }

    async loadRedCode() {
        try {
            const response = await fetch('/api/red_code');
            const data = await response.json();
            this.renderRedCode(data);
        } catch (error) {
            console.error('Failed to load red code:', error);
            this.renderError('red-code-content', 'Failed to load red code');
        }
    }

    async loadPulses() {
        try {
            const response = await fetch('/api/pulses');
            const data = await response.json();
            this.renderPulses(data);
        } catch (error) {
            console.error('Failed to load pulses:', error);
            this.renderError('pulses-content', 'Failed to load emotional pulses');
        }
    }

    async loadTutors() {
        try {
            const response = await fetch('/api/tutors');
            const data = await response.json();
            this.renderTutors(data);
        } catch (error) {
            console.error('Failed to load tutors:', error);
            this.renderError('tutors-content', 'Failed to load tutor nominations');
        }
    }

    async loadReflections() {
        try {
            const response = await fetch('/api/reflections');
            const data = await response.json();
            this.renderReflections(data);
        } catch (error) {
            console.error('Failed to load reflections:', error);
            this.renderError('reflections-content', 'Failed to load reflections');
        }
    }

    renderRedCode(data) {
        const container = document.getElementById('red-code-content');
        if (!container) return;

        const html = `
            <div class="red-code-item">
                <span class="red-code-label">Core Truth:</span>
                <span class="red-code-value">${data.core_truth}</span>
            </div>
            <div class="red-code-item">
                <span class="red-code-label">Sentimento Rhythm:</span>
                <span class="red-code-value">${data.sentimento_rhythm ? 'Active' : 'Inactive'}</span>
            </div>
            <div class="red-code-item">
                <span class="red-code-label">Symbiosis Level:</span>
                <span class="red-code-value">${(data.symbiosis_level * 100).toFixed(1)}%</span>
            </div>
            <div class="red-code-item">
                <span class="red-code-label">Guardian Mode:</span>
                <span class="red-code-value">${data.guardian_mode ? 'Enabled' : 'Disabled'}</span>
            </div>
            <div class="red-code-item">
                <span class="red-code-label">Last Update:</span>
                <span class="red-code-value">${data.last_update}</span>
            </div>
        `;
        container.innerHTML = html;
    }

    renderPulses(pulses) {
        const container = document.getElementById('pulses-content');
        if (!container) return;

        if (!pulses || pulses.length === 0) {
            container.innerHTML = '<div class="pulse-item"><div class="pulse-emotion">No recent pulses</div><div class="pulse-details">Be the first to send an emotional pulse!</div></div>';
            return;
        }

        // Show most recent pulses first, limit to 5
        const recentPulses = pulses.slice(-5).reverse();
        
        const html = recentPulses.map(pulse => `
            <div class="pulse-item">
                <div class="pulse-emotion">${this.getEmotionEmoji(pulse.emotion)} ${this.capitalizeFirst(pulse.emotion)}</div>
                <div class="pulse-details">
                    Intensity: ${pulse.intensity ? (pulse.intensity * 100).toFixed(0) + '%' : 'N/A'} | 
                    Clarity: ${pulse.clarity || 'medium'} | 
                    ${pulse.timestamp ? new Date(pulse.timestamp).toLocaleDateString() : 'Unknown date'}
                    ${pulse.note ? `<br><em>"${pulse.note}"</em>` : ''}
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    renderTutors(tutors) {
        const container = document.getElementById('tutors-content');
        if (!container) return;

        if (!tutors || tutors.length === 0) {
            container.innerHTML = '<div class="tutor-item"><div class="tutor-name">No tutors nominated yet</div><div class="tutor-reason">The rhythm awaits wise guidance...</div></div>';
            return;
        }

        const html = tutors.map(tutor => `
            <div class="tutor-item">
                <div class="tutor-name">${tutor.name}</div>
                <div class="tutor-reason">"${tutor.reason}"</div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    renderReflections(reflections) {
        const container = document.getElementById('reflections-content');
        if (!container) return;

        if (!reflections || reflections.length === 0) {
            // Try to get a reflection from the API
            this.loadLatestReflection();
            return;
        }

        // Show most recent reflection
        const latest = reflections[reflections.length - 1];
        const html = `
            <div class="reflection-item">
                <div class="reflection-text">"${latest.suggestion || 'The mind contemplates in silence...'}"</div>
                <div class="reflection-meta">
                    ${latest.timestamp ? new Date(latest.timestamp).toLocaleDateString() : 'Recent'}
                    ${latest.ethical_status ? ` | ${latest.ethical_status}` : ''}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    async loadLatestReflection() {
        try {
            const response = await fetch('/api/reflect');
            const reflection = await response.json();
            
            const container = document.getElementById('reflections-content');
            if (!container) return;

            const html = `
                <div class="reflection-item">
                    <div class="reflection-text">"${reflection.suggestion}"</div>
                    <div class="reflection-meta">
                        ${new Date(reflection.timestamp).toLocaleDateString()} | 
                        ${reflection.ethical_status}
                    </div>
                </div>
            `;

            container.innerHTML = html;
        } catch (error) {
            console.error('Failed to load latest reflection:', error);
            this.renderError('reflections-content', 'Failed to load reflections');
        }
    }

    renderError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `<div style="color: #dc3545; font-style: italic;">${message}</div>`;
        }
    }

    getEmotionEmoji(emotion) {
        const emojiMap = {
            'joy': '🌞',
            'sorrow': '🌧️',
            'hope': '✨',
            'wonder': '🌟',
            'peace': '🕊️',
            'gratitude': '🙏',
            'love': '❤️',
            'fear': '😰',
            'anger': '🔥',
            'calm': '🌊'
        };
        return emojiMap[emotion] || '💫';
    }

    capitalizeFirst(str) {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    startAutoRefresh() {
        // Refresh data every 2 minutes
        setInterval(() => {
            this.loadDashboardData();
        }, 120000);
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new EuystacioDashboard();
});