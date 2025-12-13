/**
 * Alert Service for Sensisara Dashboard
 * Real-time alert mechanisms for ethical inconsistencies
 */

const AlertService = (function() {
    'use strict';

    let paused = false;
    let alertQueue = [];
    let alertCount = 0;
    const MAX_ALERTS = 10;

    const AlertTypes = {
        SUCCESS: 'success',
        WARNING: 'warning',
        ERROR: 'error',
        INFO: 'info'
    };

    const AlertPriority = {
        LOW: 1,
        MEDIUM: 2,
        HIGH: 3,
        CRITICAL: 4
    };

    /**
     * Initialize the alert service
     */
    function init() {
        console.log('Alert Service initialized');
        startMonitoring();
        
        // Display welcome message
        addAlert({
            type: AlertTypes.SUCCESS,
            message: 'Sensisara Alert System Active',
            priority: AlertPriority.LOW
        });
    }

    /**
     * Add an alert to the dashboard
     * @param {Object} alert - Alert object with type, message, and priority
     */
    function addAlert(alert) {
        if (paused) {
            alertQueue.push(alert);
            return;
        }

        const container = document.getElementById('alert-container');
        if (!container) return;

        // Remove placeholder if present
        if (container.querySelector('p[style*="color: #999"]')) {
            container.innerHTML = '';
        }

        // Remove oldest alert if at max capacity
        const alerts = container.querySelectorAll('.alert');
        if (alerts.length >= MAX_ALERTS) {
            alerts[0].remove();
        }

        const alertElement = createAlertElement(alert);
        container.appendChild(alertElement);
        alertCount++;

        // Auto-dismiss low priority alerts after 10 seconds
        if (alert.priority <= AlertPriority.MEDIUM) {
            setTimeout(() => {
                if (alertElement.parentNode) {
                    alertElement.remove();
                }
            }, 10000);
        }
    }

    /**
     * Create an alert DOM element
     * @param {Object} alert - Alert configuration
     * @returns {HTMLElement} Alert element
     */
    function createAlertElement(alert) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${alert.type}`;
        
        const message = document.createElement('span');
        message.textContent = `${getAlertIcon(alert.type)} ${alert.message}`;
        
        const closeButton = document.createElement('button');
        closeButton.className = 'alert-close';
        closeButton.innerHTML = '×';
        closeButton.onclick = () => alertDiv.remove();
        
        alertDiv.appendChild(message);
        alertDiv.appendChild(closeButton);
        
        return alertDiv;
    }

    /**
     * Get icon for alert type
     * @param {string} type - Alert type
     * @returns {string} Icon emoji
     */
    function getAlertIcon(type) {
        const icons = {
            success: '✓',
            warning: '⚠️',
            error: '❌',
            info: 'ℹ️'
        };
        return icons[type] || 'ℹ️';
    }

    /**
     * Monitor ethical metrics and trigger alerts
     */
    function startMonitoring() {
        // Check TFK integrity
        setInterval(() => {
            checkTFKIntegrity();
        }, 30000); // Every 30 seconds

        // Check emotional stability
        setInterval(() => {
            checkEmotionalStability();
        }, 60000); // Every minute

        // Check ethical compliance
        setInterval(() => {
            checkEthicalCompliance();
        }, 45000); // Every 45 seconds

        // Simulate periodic alerts for demonstration
        setInterval(() => {
            if (!paused) {
                simulateRandomAlert();
            }
        }, 15000); // Every 15 seconds
    }

    /**
     * Check TFK ↔ CID integrity
     */
    function checkTFKIntegrity() {
        // In production, this would query the TFKVerifier contract
        const integrityRate = parseFloat(document.getElementById('tfk-integrity')?.textContent || '100');
        
        if (integrityRate < 95) {
            addAlert({
                type: AlertTypes.ERROR,
                message: `TFK Integrity degraded: ${integrityRate}%`,
                priority: AlertPriority.CRITICAL
            });
        } else if (integrityRate < 98) {
            addAlert({
                type: AlertTypes.WARNING,
                message: `TFK Integrity warning: ${integrityRate}%`,
                priority: AlertPriority.HIGH
            });
        }
    }

    /**
     * Check emotional stability metrics
     */
    function checkEmotionalStability() {
        // In production, this would query the Metaplano Emozionale module
        const stability = parseFloat(document.getElementById('emotional-stability')?.textContent || '87');
        
        if (stability < 70) {
            addAlert({
                type: AlertTypes.ERROR,
                message: `Emotional stability critical: ${stability}%`,
                priority: AlertPriority.CRITICAL
            });
        } else if (stability < 80) {
            addAlert({
                type: AlertTypes.WARNING,
                message: `Emotional stability low: ${stability}%`,
                priority: AlertPriority.MEDIUM
            });
        }
    }

    /**
     * Check ethical compliance (NSR, OLF, TFK)
     */
    function checkEthicalCompliance() {
        const nsrStatus = document.getElementById('nsr-status')?.textContent || '';
        const olfStatus = document.getElementById('olf-status')?.textContent || '';
        const vetoStatus = document.getElementById('veto-status')?.textContent || '';
        
        if (vetoStatus.includes('Triggered')) {
            addAlert({
                type: AlertTypes.ERROR,
                message: 'Red Code Veto TRIGGERED - Immediate review required',
                priority: AlertPriority.CRITICAL
            });
        }
        
        if (!nsrStatus.includes('Compliant')) {
            addAlert({
                type: AlertTypes.ERROR,
                message: 'NSR (Non-Slavery) compliance violation detected',
                priority: AlertPriority.CRITICAL
            });
        }
        
        if (!olfStatus.includes('Active')) {
            addAlert({
                type: AlertTypes.WARNING,
                message: 'OLF (One Love First) protocol inactive',
                priority: AlertPriority.HIGH
            });
        }
    }

    /**
     * Simulate random alerts for demonstration
     */
    function simulateRandomAlert() {
        const scenarios = [
            {
                type: AlertTypes.SUCCESS,
                message: 'TFK integrity check completed successfully',
                priority: AlertPriority.LOW
            },
            {
                type: AlertTypes.INFO,
                message: 'Ethical training cycle Phase III-A in progress',
                priority: AlertPriority.LOW
            },
            {
                type: AlertTypes.SUCCESS,
                message: 'Adaptive feedback loop optimization complete',
                priority: AlertPriority.LOW
            },
            {
                type: AlertTypes.INFO,
                message: 'Metaplano Emozionale prediction updated',
                priority: AlertPriority.LOW
            }
        ];
        
        const random = scenarios[Math.floor(Math.random() * scenarios.length)];
        if (Math.random() > 0.7) { // 30% chance of showing an alert
            addAlert(random);
        }
    }

    /**
     * Set paused state
     * @param {boolean} state - Paused state
     */
    function setPaused(state) {
        paused = state;
        
        if (!paused && alertQueue.length > 0) {
            // Process queued alerts
            alertQueue.forEach(alert => addAlert(alert));
            alertQueue = [];
        }
    }

    /**
     * Clear all alerts
     */
    function clearAll() {
        const container = document.getElementById('alert-container');
        if (container) {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No active alerts</p>';
        }
        alertQueue = [];
    }

    /**
     * Get alert statistics
     * @returns {Object} Statistics object
     */
    function getStatistics() {
        return {
            totalAlerts: alertCount,
            queuedAlerts: alertQueue.length,
            isPaused: paused
        };
    }

    /**
     * Trigger a custom alert
     * @param {string} type - Alert type (success, warning, error, info)
     * @param {string} message - Alert message
     * @param {number} priority - Priority level (1-4)
     */
    function triggerAlert(type, message, priority = AlertPriority.MEDIUM) {
        addAlert({
            type: type,
            message: message,
            priority: priority
        });
    }

    // Public API
    return {
        init: init,
        setPaused: setPaused,
        clearAll: clearAll,
        getStatistics: getStatistics,
        triggerAlert: triggerAlert,
        AlertTypes: AlertTypes,
        AlertPriority: AlertPriority
    };
})();

// Make AlertService available globally
if (typeof window !== 'undefined') {
    window.AlertService = AlertService;
}
