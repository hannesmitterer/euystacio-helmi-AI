/**
 * Sensisara Dashboard Configuration
 * Configuration for Phase III - The Symbiosis
 */

const DashboardConfig = {
    // Dashboard settings
    name: 'Sensisara',
    version: '3.0.0',
    phase: 'Phase III - The Symbiosis',
    
    // Update intervals (in milliseconds)
    intervals: {
        metrics: 5000,          // Update metrics every 5 seconds
        charts: 10000,          // Update charts every 10 seconds
        alerts: 15000,          // Check for alerts every 15 seconds
        timeline: 30000         // Update timeline every 30 seconds
    },
    
    // TFK ↔ CID Integrity settings
    tfk: {
        maxLatencyMs: 2.71,         // Maximum allowed latency (TFK protocol)
        integrityThreshold: 95.0,   // Minimum integrity percentage
        checkInterval: 30000,       // Check every 30 seconds
        batchSize: 100              // Maximum batch size for checks
    },
    
    // Metaplano Emozionale settings
    metaplano: {
        stabilityThreshold: 80,     // Minimum emotional stability percentage
        stressThresholds: {
            low: 20,
            medium: 30,
            high: 100
        },
        predictionInterval: 60000   // Predict every minute
    },
    
    // Ethical compliance settings
    ethical: {
        nsrMaxLatency: 2.71,        // NSR (Non-Slavery) max latency in ms
        olfMinDelta: 0.000,         // OLF (One Love First) minimum ΔCSI
        vetoEnabled: true,          // Red Code Veto enabled
        complianceCheckInterval: 45000  // Check every 45 seconds
    },
    
    // Alert settings
    alerts: {
        maxAlerts: 10,              // Maximum alerts to display
        autoDismissDelay: 10000,    // Auto-dismiss low priority alerts after 10s
        priorities: {
            low: 1,
            medium: 2,
            high: 3,
            critical: 4
        }
    },
    
    // Chart settings
    charts: {
        maxDataPoints: 20,          // Maximum data points per chart
        animationDuration: 750,     // Animation duration in ms
        defaultColors: {
            primary: 'rgb(102, 126, 234)',
            secondary: 'rgb(118, 75, 162)',
            warning: 'rgb(255, 193, 7)',
            success: 'rgb(40, 167, 69)',
            error: 'rgb(220, 53, 69)'
        }
    },
    
    // API endpoints (for production integration)
    api: {
        tfkVerifier: '/api/v1/tfk/verify',
        metaplano: '/api/v1/metaplano/status',
        ethical: '/api/v1/ethical/compliance',
        alerts: '/api/v1/alerts/stream'
    },
    
    // Feature flags
    features: {
        realTimeAlerts: true,
        chartVisualizations: true,
        emotionalPrediction: true,
        tfkMonitoring: true,
        activityTimeline: true
    },
    
    // Thresholds for visual indicators
    thresholds: {
        integrity: {
            good: 98,
            warning: 95,
            bad: 0
        },
        stability: {
            good: 90,
            warning: 80,
            bad: 0
        },
        latency: {
            good: 2.0,
            warning: 2.71,
            bad: Infinity
        }
    }
};

// Make configuration available globally
if (typeof window !== 'undefined') {
    window.DashboardConfig = DashboardConfig;
}

// Export for Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardConfig;
}
