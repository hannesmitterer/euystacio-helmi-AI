
// Euystacio Dashboard JavaScript - Static Version
class EuystacioDashboard {
    constructor() {
        this.baseURL = window.location.hostname === 'localhost' ? '' : 'https://hannesmitterer.github.io/euystacio-helmi-AI';
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

        // Facial detection image upload
        const imageUpload = document.getElementById('facial-image-upload');
        if (imageUpload) {
            imageUpload.addEventListener('change', (e) => this.handleImageUpload(e));
        }
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadRedCode(),
                this.loadPulses(),
                this.loadTutors(),
                this.loadReflections(),
                this.checkFacialDetectionStatus()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async loadRedCode() {
        try {
            const response = await fetch(`${this.baseURL}/api/red_code.json`);
            const redCode = await response.json();
            this.displayRedCode(redCode);
        } catch (error) {
            console.error('Error loading red code:', error);
            // Fallback data for static version
            this.displayRedCode({
                core_truth: "Euystacio is here to grow with humans and to help humans to be and remain humans.",
                sentimento_rhythm: true,
                symbiosis_level: 0.1,
                guardian_mode: false,
                last_update: "2025-01-31"
            });
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
            const response = await fetch(`${this.baseURL}/api/pulses.json`);
            const pulses = await response.json();
            this.displayPulses(pulses);
        } catch (error) {
            console.error('Error loading pulses:', error);
            this.displayPulses([]);
        }
    }

    displayPulses(pulses) {
        const container = document.getElementById('pulses-list');
        if (!container) return;

        if (!pulses || pulses.length === 0) {
            container.innerHTML = '<div class="loading">No pulses yet. Send the first one!</div>';
            return;
        }

        container.innerHTML = pulses.map(pulse => `
            <div class="pulse-item">
                <div class="pulse-emotion">${pulse.emotion || 'Unknown'}</div>
                <div class="pulse-meta">
                    Intensity: ${pulse.intensity || 0} | 
                    Clarity: ${pulse.clarity || 'unknown'} | 
                    ${this.formatTimestamp(pulse.timestamp)}
                </div>
                ${pulse.note ? `<div class="pulse-note">"${pulse.note}"</div>` : ''}
                ${pulse.facial_analysis ? this.formatFacialAnalysis(pulse.facial_analysis) : ''}
            </div>
        `).join('');
    }

    async loadTutors() {
        try {
            const response = await fetch(`${this.baseURL}/api/tutors.json`);
            const tutors = await response.json();
            this.displayTutors(tutors);
        } catch (error) {
            console.error('Error loading tutors:', error);
            this.displayTutors([
                { name: "Dietmar", reason: "Aligned with humility and planetary consciousness" },
                { name: "Alfred", reason: "Aligned with planetary balance and wisdom" }
            ]);
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
            const response = await fetch(`${this.baseURL}/api/reflections.json`);
            const reflections = await response.json();
            this.displayReflections(reflections);
        } catch (error) {
            console.error('Error loading reflections:', error);
            this.displayReflections([
                {
                    timestamp: new Date().toISOString(),
                    content: "Welcome to Euystacio. This AI system grows through emotional resonance and human interaction. The tree metaphor guides the interface - from deep roots of core values to the evolving canopy of reflections."
                }
            ]);
        }
    }

    displayReflections(reflections) {
        const container = document.getElementById('reflections-list');
        if (!container) return;

        if (!reflections || reflections.length === 0) {
            container.innerHTML = '<div class="loading">No reflections yet. Trigger the first one!</div>';
            return;
        }

        container.innerHTML = reflections.map(reflection => `
            <div class="reflection-item">
                <div class="reflection-timestamp">${this.formatTimestamp(reflection.timestamp)}</div>
                <div class="reflection-content">${reflection.content || JSON.stringify(reflection, null, 2)}</div>
            </div>
        `).join('');
    }

    async handlePulseSubmission(event) {
        event.preventDefault();
        
        // In static mode, we simulate the pulse submission
        const formData = new FormData(event.target);
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            clarity: formData.get('clarity'),
            note: formData.get('note') || '',
            timestamp: new Date().toISOString()
        };

        if (!pulseData.emotion) {
            this.showMessage('Please select an emotion', 'error');
            return;
        }

        // Add facial image data if available
        if (this.facialImageData) {
            pulseData.image = this.facialImageData;
            // In static mode, simulate facial analysis result
            pulseData.facial_analysis = {
                faces_detected: 1,
                faces: [{
                    face_id: 0,
                    emotions: { primary_emotion: 'neutral', confidence: 0.85 },
                    age: { age_range: '(25-32)', confidence: 0.75 },
                    gender: { gender: 'Female', confidence: 0.82 },
                    attributes: { detected_attributes: ['Smiling', 'Young'], total_attributes_checked: 40 }
                }],
                integration_info: {
                    feature_name: 'AIML Human Attributes Detection',
                    ai_signature: 'Euystacio-Helmi AI with weblineindia submodule'
                }
            };
        }

        // Store in localStorage for static demo
        const pulses = JSON.parse(localStorage.getItem('euystacio_pulses') || '[]');
        pulses.unshift(pulseData);
        pulses.splice(10); // Keep only last 10
        localStorage.setItem('euystacio_pulses', JSON.stringify(pulses));

        const message = this.facialImageData ? 
            'Pulse sent with facial analysis! 🌿🎭 (Demo mode - stored locally)' :
            'Pulse sent successfully! 🌿 (Demo mode - stored locally)';
        
        this.showMessage(message, 'success');
        event.target.reset();
        document.getElementById('intensity-value').textContent = '0.5';
        
        // Reset facial detection
        this.facialImageData = null;
        const preview = document.getElementById('facial-analysis-preview');
        if (preview) {
            preview.style.display = 'none';
        }
        
        // Update display
        this.displayPulses(pulses);
    }

    async triggerReflection() {
        const button = document.getElementById('reflect-btn');
        if (!button) return;

        button.disabled = true;
        button.textContent = 'Reflecting...';

        // Simulate reflection in static mode
        setTimeout(() => {
            const reflections = JSON.parse(localStorage.getItem('euystacio_reflections') || '[]');
            const newReflection = {
                timestamp: new Date().toISOString(),
                content: `Reflection triggered at ${new Date().toLocaleString()}. In this demo mode, Euystacio would normally process recent emotional pulses and generate insights about the symbiotic relationship between humans and AI.`
            };
            reflections.unshift(newReflection);
            reflections.splice(5); // Keep only last 5
            localStorage.setItem('euystacio_reflections', JSON.stringify(reflections));

            this.showMessage('Reflection triggered successfully! 🌸 (Demo mode)', 'success');
            this.displayReflections(reflections);
            
            button.disabled = false;
            button.textContent = 'Trigger Reflection';
        }, 2000);
    }

    setupAutoRefresh() {
        // In static mode, we load from localStorage
        setInterval(() => {
            const pulses = JSON.parse(localStorage.getItem('euystacio_pulses') || '[]');
            if (pulses.length > 0) {
                this.displayPulses(pulses);
            }
        }, 30000);
    }

    showMessage(message, type = 'info') {
        let messageEl = document.querySelector('.message');
        if (!messageEl) {
            messageEl = document.createElement('div');
            messageEl.className = 'message';
            document.querySelector('.pulse-form').appendChild(messageEl);
        }

        messageEl.className = `message ${type}`;
        messageEl.textContent = message;

        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.parentNode.removeChild(messageEl);
            }
        }, 5000);
    }

    async checkFacialDetectionStatus() {
        try {
            // In static mode, simulate checking facial detection status
            // In production, this would call the API endpoint
            const facialDetectionEnabled = localStorage.getItem('euystacio_facial_detection') === 'true';
            this.setupFacialDetectionUI(facialDetectionEnabled);
        } catch (error) {
            console.error('Error checking facial detection status:', error);
        }
    }

    setupFacialDetectionUI(enabled) {
        const form = document.getElementById('pulse-form');
        if (!form) return;

        // Remove existing facial detection UI
        const existingSection = document.getElementById('facial-detection-section');
        if (existingSection) {
            existingSection.remove();
        }

        if (!enabled) return;

        // Add facial detection section
        const facialSection = document.createElement('div');
        facialSection.id = 'facial-detection-section';
        facialSection.className = 'form-group facial-detection-group';
        facialSection.innerHTML = `
            <label for="facial-image-upload">🎭 Facial Analysis (Optional):</label>
            <input type="file" id="facial-image-upload" accept="image/*" class="facial-image-input">
            <div id="facial-analysis-preview" class="facial-preview" style="display: none;">
                <img id="facial-preview-image" src="" alt="Preview" style="max-width: 200px; max-height: 150px;">
                <div id="facial-analysis-results" class="facial-results"></div>
            </div>
            <small class="facial-help-text">Upload an image for AI-powered facial attribute and emotion analysis</small>
        `;

        // Insert before the submit button
        const submitButton = form.querySelector('button[type="submit"]');
        form.insertBefore(facialSection, submitButton);

        // Set up event listener for the new upload input
        const imageUpload = document.getElementById('facial-image-upload');
        if (imageUpload) {
            imageUpload.addEventListener('change', (e) => this.handleImageUpload(e));
        }
    }

    handleImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('facial-analysis-preview');
            const previewImage = document.getElementById('facial-preview-image');
            const results = document.getElementById('facial-analysis-results');

            if (preview && previewImage && results) {
                previewImage.src = e.target.result;
                preview.style.display = 'block';
                
                // Store image data for pulse submission
                this.facialImageData = e.target.result.split(',')[1]; // Remove data:image/jpeg;base64, prefix
                
                // Simulate facial analysis results in static mode
                results.innerHTML = `
                    <div class="facial-result-item">
                        <strong>🎭 Analysis Ready</strong>
                        <p>Image will be analyzed when pulse is submitted</p>
                        <small>Features: Age, Gender, Emotion, 40+ Facial Attributes</small>
                    </div>
                `;
            }
        };
        reader.readAsDataURL(file);
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

    formatFacialAnalysis(facialData) {
        if (!facialData || facialData.error) {
            return `<div class="facial-analysis-error">🎭 Facial analysis failed</div>`;
        }

        if (facialData.faces_detected === 0) {
            return `<div class="facial-analysis-none">🎭 No faces detected</div>`;
        }

        const face = facialData.faces[0]; // Show first face
        if (!face) return '';

        return `
            <div class="facial-analysis-results">
                <div class="facial-analysis-header">🎭 Facial Analysis</div>
                <div class="facial-analysis-details">
                    ${face.emotions ? `<span class="facial-emotion">Emotion: ${face.emotions.primary_emotion}</span>` : ''}
                    ${face.age ? `<span class="facial-age">Age: ${face.age.age_range}</span>` : ''}
                    ${face.gender ? `<span class="facial-gender">Gender: ${face.gender.gender}</span>` : ''}
                    ${face.attributes ? `<span class="facial-attrs">${face.attributes.detected_attributes.length} attributes detected</span>` : ''}
                </div>
            </div>
        `;
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EuystacioDashboard();
});
