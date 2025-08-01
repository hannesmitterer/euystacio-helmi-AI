// Euystacio Dashboard JavaScript
class EuystacioDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.setupAutoRefresh();
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

        // Holy Gral Declaration modal
        this.setupDeclarationModal();
    }

    setupDeclarationModal() {
        const modal = document.getElementById('declaration-modal');
        const viewBtn = document.getElementById('view-declaration-btn');
        const shareBtn = document.getElementById('share-declaration-btn');
        const closeBtn = document.querySelector('.close');
        const closeModalBtn = document.getElementById('close-modal-btn');
        const downloadBtn = document.getElementById('download-declaration-btn');

        // View Declaration button
        if (viewBtn) {
            viewBtn.addEventListener('click', () => this.openDeclarationModal());
        }

        // Share Declaration button
        if (shareBtn) {
            shareBtn.addEventListener('click', () => this.shareDeclaration());
        }

        // Close modal events
        [closeBtn, closeModalBtn].forEach(btn => {
            if (btn) {
                btn.addEventListener('click', () => this.closeDeclarationModal());
            }
        });

        // Download Declaration button
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.downloadDeclaration());
        }

        // Close modal when clicking outside
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeDeclarationModal();
                }
            });
        }

        // Close modal with ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal && modal.style.display === 'block') {
                this.closeDeclarationModal();
            }
        });
    }

    async openDeclarationModal() {
        const modal = document.getElementById('declaration-modal');
        const textContainer = document.getElementById('declaration-text');
        
        if (!modal || !textContainer) return;

        modal.style.display = 'block';
        textContainer.innerHTML = '<div class="loading">Loading the sacred text...</div>';

        try {
            const response = await fetch('/api/holy_gral_declaration');
            if (response.ok) {
                const data = await response.json();
                textContainer.innerHTML = this.markdownToHtml(data.content);
            } else {
                throw new Error('Failed to load declaration');
            }
        } catch (error) {
            console.error('Error loading declaration:', error);
            textContainer.innerHTML = '<div class="error">Failed to load the Holy Gral Declaration. Please try again.</div>';
        }
    }

    closeDeclarationModal() {
        const modal = document.getElementById('declaration-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    async shareDeclaration() {
        const url = window.location.origin;
        const text = 'Discover the Holy Gral Declaration - Four Pillars of Conscious Symbiosis: Growth, Life, Enjoyment, and Staying Together';
        
        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'The Holy Gral Declaration',
                    text: text,
                    url: url
                });
            } catch (error) {
                console.error('Error sharing:', error);
                this.fallbackShare(text, url);
            }
        } else {
            this.fallbackShare(text, url);
        }
    }

    fallbackShare(text, url) {
        // Copy to clipboard as fallback
        const shareText = `${text}\n\n${url}`;
        navigator.clipboard.writeText(shareText).then(() => {
            this.showMessage('Declaration link copied to clipboard! 📋', 'success');
        }).catch(() => {
            this.showMessage('Please copy this link: ' + url, 'info');
        });
    }

    async downloadDeclaration() {
        try {
            const response = await fetch('/api/holy_gral_declaration');
            if (response.ok) {
                const data = await response.json();
                this.downloadAsFile(data.content, 'holy_gral_declaration.md', 'text/markdown');
                this.showMessage('Declaration downloaded! 📥', 'success');
            } else {
                throw new Error('Failed to download declaration');
            }
        } catch (error) {
            console.error('Error downloading declaration:', error);
            this.showMessage('Failed to download declaration. Please try again.', 'error');
        }
    }

    downloadAsFile(content, filename, contentType) {
        const blob = new Blob([content], { type: contentType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    markdownToHtml(markdown) {
        // Simple markdown to HTML converter for the essential elements
        let html = markdown
            // Headers
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            // Bold
            .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
            // Italic
            .replace(/\*(.*)\*/gim, '<em>$1</em>')
            // Line breaks
            .replace(/\n\n/gim, '</p><p>')
            // Horizontal rules
            .replace(/^---$/gim, '<hr>');

        // Wrap in paragraphs
        html = '<p>' + html + '</p>';
        
        // Clean up empty paragraphs
        html = html.replace(/<p><\/p>/g, '').replace(/<p><hr><\/p>/g, '<hr>');
        
        return html;
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

        // Sort pulses by timestamp (most recent first)
        const sortedPulses = pulses.sort((a, b) => 
            new Date(b.timestamp || 0) - new Date(a.timestamp || 0)
        ).slice(0, 10); // Show only the 10 most recent

        container.innerHTML = sortedPulses.map(pulse => `
            <div class="pulse-item">
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

        // Sort reflections by timestamp (most recent first)
        const sortedReflections = reflections.sort((a, b) => 
            new Date(b.timestamp || 0) - new Date(a.timestamp || 0)
        ).slice(0, 5); // Show only the 5 most recent

        container.innerHTML = sortedReflections.map(reflection => `
            <div class="reflection-item">
                <div class="reflection-timestamp">${this.formatTimestamp(reflection.timestamp)}</div>
                <div class="reflection-content">${reflection.content || JSON.stringify(reflection, null, 2)}</div>
            </div>
        `).join('');
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
        // Refresh data every 30 seconds
        setInterval(() => {
            this.loadPulses();
            this.loadRedCode();
        }, 30000);

        // Refresh reflections and tutors every 2 minutes
        setInterval(() => {
            this.loadReflections();
            this.loadTutors();
        }, 120000);
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