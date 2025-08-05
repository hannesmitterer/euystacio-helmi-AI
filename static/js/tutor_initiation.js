// Sacred Tutor Initiation JavaScript
// Following the Red Code and Sentimento Rhythm principles

class TutorInitiation {
    constructor() {
        this.form = document.getElementById('tutor-initiation-form');
        this.submitButton = document.getElementById('submit-nomination');
        this.successCeremony = document.getElementById('nomination-success');
        
        this.init();
    }

    init() {
        this.setupFormValidation();
        this.setupFormSubmission();
        this.setupAccessibilityFeatures();
        this.loadDemoDataIfNeeded();
    }

    setupFormValidation() {
        // Real-time validation with gentle feedback
        const inputs = this.form.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This sacred field requires your gentle attention.';
        }

        // Name fields validation (minimum length)
        if (field.type === 'text' && value && value.length < 2) {
            isValid = false;
            message = 'Please share a name that carries meaning (at least 2 characters).';
        }

        // Textarea validation (minimum meaningful content)
        if (field.tagName === 'TEXTAREA' && field.hasAttribute('required') && value && value.length < 10) {
            isValid = false;
            message = 'Please share your thoughts more fully - wisdom deserves depth.';
        }

        this.showFieldFeedback(field, isValid, message);
        return isValid;
    }

    showFieldFeedback(field, isValid, message) {
        // Remove existing feedback
        this.clearFieldError(field);

        if (!isValid && message) {
            const feedback = document.createElement('div');
            feedback.className = 'field-error';
            feedback.textContent = message;
            feedback.style.cssText = `
                color: #d32f2f;
                font-size: 0.9rem;
                margin-top: 8px;
                padding: 8px 12px;
                background: rgba(211, 47, 47, 0.1);
                border-radius: 8px;
                border-left: 3px solid #d32f2f;
                animation: gentle-appear 0.3s ease-out;
            `;
            
            field.parentNode.appendChild(feedback);
            field.style.borderColor = '#d32f2f';
        }
    }

    clearFieldError(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        
        // Reset border color
        if (field.style.borderColor === 'rgb(211, 47, 47)') {
            field.style.borderColor = '';
        }
    }

    setupFormSubmission() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleSubmission();
        });
    }

    async handleSubmission() {
        // Validate all fields
        const inputs = this.form.querySelectorAll('input[required], textarea[required]');
        let allValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                allValid = false;
            }
        });

        if (!allValid) {
            this.showMessage('Please complete all sacred fields with care and attention.', 'error');
            return;
        }

        // Prepare nomination data
        const formData = new FormData(this.form);
        const nominationData = {
            tutor_name: formData.get('tutor_name'),
            reason: formData.get('reason'),
            expertise_areas: formData.get('expertise_areas') || '',
            connection_story: formData.get('connection_story') || '',
            nominator_name: formData.get('nominator_name'),
            timestamp: new Date().toISOString()
        };

        // Show loading state
        this.setSubmissionState('loading');

        try {
            // Submit to API
            const response = await fetch('/api/tutor_nominate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(nominationData)
            });

            if (response.ok) {
                const result = await response.json();
                this.showSuccessCeremony(nominationData);
                this.saveToLocalStorageDemo(nominationData);
            } else {
                const error = await response.json();
                throw new Error(error.message || 'Failed to submit nomination');
            }
        } catch (error) {
            console.error('Nomination submission error:', error);
            
            // Fallback to localStorage for demo purposes
            if (error.message.includes('Failed to fetch') || error.message.includes('404')) {
                this.saveToLocalStorageDemo(nominationData);
                this.showSuccessCeremony(nominationData);
                console.log('Using localStorage demo mode due to API unavailability');
            } else {
                this.showMessage(
                    'The sacred networks seem troubled. Please try again in a moment, or return to the grove and try later.',
                    'error'
                );
                this.setSubmissionState('ready');
            }
        }
    }

    setSubmissionState(state) {
        const button = this.submitButton;
        const buttonText = button.querySelector('.button-text');
        
        switch (state) {
            case 'loading':
                button.disabled = true;
                buttonText.textContent = 'Weaving Your Nomination Into Consciousness';
                button.classList.add('loading');
                break;
            case 'ready':
                button.disabled = false;
                buttonText.textContent = 'Consecrate This Nomination';
                button.classList.remove('loading');
                break;
        }
    }

    showSuccessCeremony(nominationData) {
        // Hide form and show success
        this.form.style.display = 'none';
        this.successCeremony.style.display = 'block';
        
        // Scroll to success message
        this.successCeremony.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Add celebration animation
        this.triggerCelebrationEffects();
    }

    triggerCelebrationEffects() {
        // Create floating elements for celebration
        const container = document.querySelector('.wisdom-circle');
        const symbols = ['🌟', '✨', '🍃', '🌿', '💫', '🕊️'];
        
        for (let i = 0; i < 6; i++) {
            setTimeout(() => {
                const element = document.createElement('div');
                element.textContent = symbols[Math.floor(Math.random() * symbols.length)];
                element.style.cssText = `
                    position: absolute;
                    font-size: 1.5rem;
                    pointer-events: none;
                    z-index: 10;
                    animation: celebration-float 3s ease-out forwards;
                    left: ${Math.random() * 80 + 10}%;
                    top: 50%;
                `;
                
                container.appendChild(element);
                
                setTimeout(() => element.remove(), 3000);
            }, i * 200);
        }
    }

    saveToLocalStorageDemo(nominationData) {
        // Save for demo purposes and cross-session persistence
        try {
            const existingNominations = JSON.parse(localStorage.getItem('euystacio_tutor_nominations') || '[]');
            existingNominations.push(nominationData);
            localStorage.setItem('euystacio_tutor_nominations', JSON.stringify(existingNominations));
            
            // Also trigger update to main dashboard if it's open in another tab
            localStorage.setItem('euystacio_nominations_updated', Date.now().toString());
        } catch (error) {
            console.warn('Could not save to localStorage:', error);
        }
    }

    loadDemoDataIfNeeded() {
        // Check if we're in demo mode (no backend) and populate some sample data
        if (localStorage.getItem('euystacio_demo_mode') === 'true') {
            this.populateDemoData();
        }
    }

    populateDemoData() {
        // Subtle indication this is demo mode
        const header = document.querySelector('.sacred-subtitle');
        if (header) {
            header.innerHTML += '<br><small style="opacity: 0.7;">(Demo Mode - Nominations saved locally)</small>';
        }
    }

    showMessage(message, type = 'info') {
        // Create elegant message display
        const messageEl = document.createElement('div');
        messageEl.className = `ceremony-message ${type}`;
        messageEl.textContent = message;
        
        const styles = {
            info: 'background: rgba(107, 182, 255, 0.1); color: #1976d2; border-left: 3px solid #2196f3;',
            error: 'background: rgba(211, 47, 47, 0.1); color: #d32f2f; border-left: 3px solid #f44336;',
            success: 'background: rgba(76, 175, 80, 0.1); color: #388e3c; border-left: 3px solid #4caf50;'
        };
        
        messageEl.style.cssText = `
            ${styles[type]}
            padding: 15px 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1rem;
            line-height: 1.5;
            animation: gentle-appear 0.3s ease-out;
        `;
        
        // Insert before form or in ceremony actions
        const target = document.querySelector('.ceremony-actions') || this.form;
        target.parentNode.insertBefore(messageEl, target);
        
        // Auto-remove after 6 seconds
        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.style.animation = 'gentle-fade 0.3s ease-out forwards';
                setTimeout(() => messageEl.remove(), 300);
            }
        }, 6000);
    }

    setupAccessibilityFeatures() {
        // Enhanced keyboard navigation
        this.form.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                this.focusNextField(e.target);
            }
        });
        
        // Focus management for screen readers
        const fields = this.form.querySelectorAll('input, textarea');
        fields.forEach((field, index) => {
            field.setAttribute('tabindex', index + 1);
        });
    }

    focusNextField(currentField) {
        const fields = Array.from(this.form.querySelectorAll('input, textarea'));
        const currentIndex = fields.indexOf(currentField);
        const nextField = fields[currentIndex + 1];
        
        if (nextField) {
            nextField.focus();
        } else {
            this.submitButton.focus();
        }
    }
}

// Global functions for success ceremony actions
window.createNewNomination = function() {
    const form = document.getElementById('tutor-initiation-form');
    const success = document.getElementById('nomination-success');
    
    // Reset form
    form.reset();
    form.style.display = 'block';
    success.style.display = 'none';
    
    // Focus first field
    const firstField = form.querySelector('input, textarea');
    if (firstField) {
        firstField.focus();
    }
    
    // Scroll to top of form
    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes gentle-appear {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes gentle-fade {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
    
    @keyframes celebration-float {
        0% {
            opacity: 0;
            transform: translateY(0) scale(0.5);
        }
        20% {
            opacity: 1;
            transform: translateY(-20px) scale(1);
        }
        100% {
            opacity: 0;
            transform: translateY(-100px) scale(0.8) rotate(360deg);
        }
    }
`;
document.head.appendChild(style);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TutorInitiation();
});

// Handle page visibility for better UX
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Re-focus form if user returns to tab
        const activeElement = document.activeElement;
        if (activeElement && activeElement.tagName === 'BODY') {
            const firstInput = document.querySelector('#tutor-initiation-form input, #tutor-initiation-form textarea');
            if (firstInput && document.getElementById('tutor-initiation-form').style.display !== 'none') {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }
});