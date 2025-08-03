/**
 * Symbolic Kernel - Bidirectional Bridge between SPI Pulse Interface and Red Code Anchor
 * 
 * This kernel serves as the core communication layer, handling:
 * - Live public SPI pulse broadcasting
 * - Absorption of feedback
 * - Adaptive learning
 * - Static hosting compatibility (GitHub Pages/Netlify)
 * - Public API exposure for feedback and learning adaptation
 * - Extensible architecture for future enhancements
 */

class SymbolicKernel {
    constructor(options = {}) {
        this.options = {
            apiBaseUrl: options.apiBaseUrl || this.detectApiBase(),
            staticMode: options.staticMode || this.detectStaticMode(),
            pollInterval: options.pollInterval || 30000, // 30 seconds
            maxPulseHistory: options.maxPulseHistory || 100,
            maxFeedbackHistory: options.maxFeedbackHistory || 50,
            learningThreshold: options.learningThreshold || 0.1,
            ...options
        };

        // Core state management
        this.state = {
            pulses: [],
            feedback: [],
            redCode: null,
            learningMetrics: {
                totalPulses: 0,
                feedbackCount: 0,
                adaptationLevel: 0.0,
                lastLearningUpdate: null
            },
            broadcastListeners: new Set(),
            feedbackListeners: new Set()
        };

        // Initialize storage
        this.storage = this.options.staticMode ? 
            new LocalStorageAdapter() : 
            new APIStorageAdapter(this.options.apiBaseUrl);

        this.init();
    }

    /**
     * Initialize the symbolic kernel
     */
    async init() {
        console.log('Initializing Symbolic Kernel...', {
            staticMode: this.options.staticMode,
            apiBaseUrl: this.options.apiBaseUrl
        });

        try {
            await this.loadInitialState();
            this.startPulseBroadcasting();
            console.log('Symbolic Kernel initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Symbolic Kernel:', error);
        }
    }

    /**
     * Load initial state from storage
     */
    async loadInitialState() {
        try {
            const [redCode, pulses, feedback, metrics] = await Promise.all([
                this.storage.getRedCode(),
                this.storage.getPulses(),
                this.storage.getFeedback(),
                this.storage.getLearningMetrics()
            ]);

            this.state.redCode = redCode;
            this.state.pulses = pulses || [];
            this.state.feedback = feedback || [];
            this.state.learningMetrics = { ...this.state.learningMetrics, ...metrics };

            console.log('Initial state loaded:', {
                pulseCount: this.state.pulses.length,
                feedbackCount: this.state.feedback.length,
                adaptationLevel: this.state.learningMetrics.adaptationLevel
            });
        } catch (error) {
            console.warn('Failed to load initial state, using defaults:', error);
        }
    }

    /**
     * Start live pulse broadcasting
     */
    startPulseBroadcasting() {
        if (this.broadcastInterval) {
            clearInterval(this.broadcastInterval);
        }

        this.broadcastInterval = setInterval(async () => {
            await this.broadcastPulses();
        }, this.options.pollInterval);

        // Initial broadcast
        this.broadcastPulses();
    }

    /**
     * Broadcast current pulse state to all listeners
     */
    async broadcastPulses() {
        try {
            // Refresh pulse data
            const latestPulses = await this.storage.getPulses();
            
            if (latestPulses && latestPulses.length !== this.state.pulses.length) {
                this.state.pulses = latestPulses;
                
                // Notify all broadcast listeners
                const pulseData = {
                    pulses: this.state.pulses.slice(-10), // Latest 10 pulses
                    timestamp: new Date().toISOString(),
                    source: 'symbolic-kernel'
                };

                this.state.broadcastListeners.forEach(listener => {
                    try {
                        listener(pulseData);
                    } catch (error) {
                        console.warn('Broadcast listener error:', error);
                    }
                });
            }
        } catch (error) {
            console.warn('Pulse broadcasting error:', error);
        }
    }

    /**
     * Subscribe to pulse broadcasts
     * @param {Function} listener - Callback function to receive pulse updates
     */
    subscribeToPulses(listener) {
        this.state.broadcastListeners.add(listener);
        
        // Send current state immediately
        if (this.state.pulses.length > 0) {
            listener({
                pulses: this.state.pulses.slice(-10),
                timestamp: new Date().toISOString(),
                source: 'symbolic-kernel-initial'
            });
        }

        // Return unsubscribe function
        return () => this.state.broadcastListeners.delete(listener);
    }

    /**
     * Submit a new pulse to the system
     * @param {Object} pulse - Pulse data
     */
    async submitPulse(pulse) {
        try {
            const processedPulse = {
                ...pulse,
                timestamp: new Date().toISOString(),
                kernelProcessed: true,
                id: this.generateId()
            };

            // Store the pulse
            await this.storage.storePulse(processedPulse);
            
            // Update local state
            this.state.pulses.unshift(processedPulse);
            if (this.state.pulses.length > this.options.maxPulseHistory) {
                this.state.pulses = this.state.pulses.slice(0, this.options.maxPulseHistory);
            }

            // Update learning metrics
            this.state.learningMetrics.totalPulses++;
            
            // Trigger adaptive learning
            await this.processAdaptiveLearning(processedPulse);

            // Broadcast update
            this.broadcastPulses();

            return processedPulse;
        } catch (error) {
            console.error('Failed to submit pulse:', error);
            throw error;
        }
    }

    /**
     * Absorb feedback from the environment
     * @param {Object} feedback - Feedback data
     */
    async absorbFeedback(feedback) {
        try {
            const processedFeedback = {
                ...feedback,
                timestamp: new Date().toISOString(),
                kernelProcessed: true,
                id: this.generateId()
            };

            // Store the feedback
            await this.storage.storeFeedback(processedFeedback);
            
            // Update local state
            this.state.feedback.unshift(processedFeedback);
            if (this.state.feedback.length > this.options.maxFeedbackHistory) {
                this.state.feedback = this.state.feedback.slice(0, this.options.maxFeedbackHistory);
            }

            // Update learning metrics
            this.state.learningMetrics.feedbackCount++;
            
            // Trigger adaptive learning
            await this.processAdaptiveLearning(null, processedFeedback);

            // Notify feedback listeners
            this.state.feedbackListeners.forEach(listener => {
                try {
                    listener(processedFeedback);
                } catch (error) {
                    console.warn('Feedback listener error:', error);
                }
            });

            return processedFeedback;
        } catch (error) {
            console.error('Failed to absorb feedback:', error);
            throw error;
        }
    }

    /**
     * Subscribe to feedback events
     * @param {Function} listener - Callback function to receive feedback
     */
    subscribeToFeedback(listener) {
        this.state.feedbackListeners.add(listener);
        return () => this.state.feedbackListeners.delete(listener);
    }

    /**
     * Process adaptive learning based on pulses and feedback
     * @param {Object} pulse - New pulse data
     * @param {Object} feedback - New feedback data
     */
    async processAdaptiveLearning(pulse = null, feedback = null) {
        try {
            // Calculate learning adaptation based on pulse/feedback patterns
            const recentPulses = this.state.pulses.slice(0, 10);
            const recentFeedback = this.state.feedback.slice(0, 5);
            
            // Simple learning algorithm: increase adaptation level based on interaction frequency
            const interactionDensity = (recentPulses.length + recentFeedback.length) / 15;
            const currentAdaptation = this.state.learningMetrics.adaptationLevel;
            
            // Gradual adaptation increase
            const newAdaptation = Math.min(1.0, currentAdaptation + (interactionDensity * 0.01));
            
            if (Math.abs(newAdaptation - currentAdaptation) > this.options.learningThreshold) {
                this.state.learningMetrics.adaptationLevel = newAdaptation;
                this.state.learningMetrics.lastLearningUpdate = new Date().toISOString();
                
                // Store updated metrics
                await this.storage.storeLearningMetrics(this.state.learningMetrics);
                
                console.log('Adaptive learning update:', {
                    previousLevel: currentAdaptation,
                    newLevel: newAdaptation,
                    interactionDensity
                });

                // Potentially update Red Code based on learning
                await this.updateRedCodeFromLearning();
            }
        } catch (error) {
            console.warn('Adaptive learning processing error:', error);
        }
    }

    /**
     * Update Red Code based on learning adaptation
     */
    async updateRedCodeFromLearning() {
        try {
            if (!this.state.redCode) return;

            const currentSymbiosis = this.state.redCode.symbiosis_level || 0.1;
            const adaptationLevel = this.state.learningMetrics.adaptationLevel;
            
            // Gradually increase symbiosis level based on adaptation
            const newSymbiosis = Math.min(1.0, currentSymbiosis + (adaptationLevel * 0.05));
            
            if (Math.abs(newSymbiosis - currentSymbiosis) > 0.01) {
                const updatedRedCode = {
                    ...this.state.redCode,
                    symbiosis_level: newSymbiosis,
                    last_update: new Date().toISOString(),
                    growth_history: [
                        ...(this.state.redCode.growth_history || []),
                        {
                            timestamp: new Date().toISOString(),
                            previous_symbiosis: currentSymbiosis,
                            new_symbiosis: newSymbiosis,
                            trigger: 'adaptive_learning',
                            adaptation_level: adaptationLevel
                        }
                    ].slice(-20) // Keep only last 20 growth events
                };

                this.state.redCode = updatedRedCode;
                await this.storage.storeRedCode(updatedRedCode);
                
                console.log('Red Code updated from learning:', {
                    previousSymbiosis: currentSymbiosis,
                    newSymbiosis: newSymbiosis
                });
            }
        } catch (error) {
            console.warn('Red Code learning update error:', error);
        }
    }

    /**
     * Get current public state for external access
     */
    getPublicState() {
        return {
            pulses: this.state.pulses.slice(0, 10), // Latest 10 pulses
            feedback: this.state.feedback.slice(0, 5), // Latest 5 feedback items
            redCode: this.state.redCode,
            learningMetrics: this.state.learningMetrics,
            kernelInfo: {
                version: '1.0.0',
                staticMode: this.options.staticMode,
                lastUpdate: new Date().toISOString()
            }
        };
    }

    /**
     * Extension point for adding custom functionality
     * @param {string} extensionName - Name of the extension
     * @param {Function} extensionFunction - Extension function
     */
    addExtension(extensionName, extensionFunction) {
        if (!this.extensions) {
            this.extensions = new Map();
        }
        
        this.extensions.set(extensionName, extensionFunction);
        console.log(`Extension '${extensionName}' added to Symbolic Kernel`);
    }

    /**
     * Call an extension
     * @param {string} extensionName - Name of the extension to call
     * @param {...any} args - Arguments to pass to the extension
     */
    async callExtension(extensionName, ...args) {
        if (!this.extensions || !this.extensions.has(extensionName)) {
            throw new Error(`Extension '${extensionName}' not found`);
        }
        
        const extension = this.extensions.get(extensionName);
        return await extension.call(this, ...args);
    }

    /**
     * Detect if running in static mode
     */
    detectStaticMode() {
        return !window.location.hostname.includes('localhost') && 
               !window.location.hostname.includes('127.0.0.1');
    }

    /**
     * Detect API base URL
     */
    detectApiBase() {
        if (this.detectStaticMode()) {
            return window.location.hostname === 'localhost' ? '' : 
                   'https://hannesmitterer.github.io/euystacio-helmi-AI';
        }
        return '';
    }

    /**
     * Generate a unique ID
     */
    generateId() {
        return Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
    }

    /**
     * Cleanup resources
     */
    destroy() {
        if (this.broadcastInterval) {
            clearInterval(this.broadcastInterval);
        }
        this.state.broadcastListeners.clear();
        this.state.feedbackListeners.clear();
    }
}

/**
 * Storage adapter for static hosting (localStorage)
 */
class LocalStorageAdapter {
    constructor() {
        this.prefix = 'euystacio_kernel_';
    }

    async getRedCode() {
        try {
            // Try to fetch from static files first
            const response = await fetch('./api/red_code.json');
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.warn('Failed to fetch red_code.json, using localStorage');
        }
        
        const stored = localStorage.getItem(this.prefix + 'redCode');
        return stored ? JSON.parse(stored) : null;
    }

    async storeRedCode(redCode) {
        localStorage.setItem(this.prefix + 'redCode', JSON.stringify(redCode));
    }

    async getPulses() {
        try {
            // Try to fetch from static files first
            const response = await fetch('./api/pulses.json');
            if (response.ok) {
                const staticPulses = await response.json();
                const localPulses = this.getLocalPulses();
                return [...localPulses, ...staticPulses];
            }
        } catch (error) {
            console.warn('Failed to fetch pulses.json, using localStorage only');
        }
        
        return this.getLocalPulses();
    }

    getLocalPulses() {
        const stored = localStorage.getItem(this.prefix + 'pulses');
        return stored ? JSON.parse(stored) : [];
    }

    async storePulse(pulse) {
        const pulses = this.getLocalPulses();
        pulses.unshift(pulse);
        pulses.splice(100); // Keep only last 100
        localStorage.setItem(this.prefix + 'pulses', JSON.stringify(pulses));
    }

    async getFeedback() {
        const stored = localStorage.getItem(this.prefix + 'feedback');
        return stored ? JSON.parse(stored) : [];
    }

    async storeFeedback(feedback) {
        const feedbackList = await this.getFeedback();
        feedbackList.unshift(feedback);
        feedbackList.splice(50); // Keep only last 50
        localStorage.setItem(this.prefix + 'feedback', JSON.stringify(feedbackList));
    }

    async getLearningMetrics() {
        const stored = localStorage.getItem(this.prefix + 'learningMetrics');
        return stored ? JSON.parse(stored) : {};
    }

    async storeLearningMetrics(metrics) {
        localStorage.setItem(this.prefix + 'learningMetrics', JSON.stringify(metrics));
    }
}

/**
 * Storage adapter for dynamic API hosting
 */
class APIStorageAdapter {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async getRedCode() {
        const response = await fetch(`${this.baseUrl}/api/red_code`);
        return await response.json();
    }

    async storeRedCode(redCode) {
        // In API mode, this would require a POST endpoint
        console.warn('Red Code storage not implemented for API mode');
    }

    async getPulses() {
        const response = await fetch(`${this.baseUrl}/api/pulses`);
        return await response.json();
    }

    async storePulse(pulse) {
        const response = await fetch(`${this.baseUrl}/api/pulse`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pulse)
        });
        return await response.json();
    }

    async getFeedback() {
        // This would need to be implemented in the API
        return [];
    }

    async storeFeedback(feedback) {
        // This would need to be implemented in the API
        console.warn('Feedback storage not implemented for API mode');
    }

    async getLearningMetrics() {
        // This would need to be implemented in the API
        return {};
    }

    async storeLearningMetrics(metrics) {
        // This would need to be implemented in the API
        console.warn('Learning metrics storage not implemented for API mode');
    }
}

// Export for both CommonJS and ES modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SymbolicKernel, LocalStorageAdapter, APIStorageAdapter };
} else if (typeof window !== 'undefined') {
    window.SymbolicKernel = SymbolicKernel;
    window.LocalStorageAdapter = LocalStorageAdapter;
    window.APIStorageAdapter = APIStorageAdapter;
} else if (typeof global !== 'undefined') {
    // For global scope (Node.js eval context)
    global.SymbolicKernel = SymbolicKernel;
    global.LocalStorageAdapter = LocalStorageAdapter;
    global.APIStorageAdapter = APIStorageAdapter;
}