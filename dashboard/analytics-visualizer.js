/**
 * Analytics Visualizer for Sensisara Dashboard
 * Advanced visual analytics for ethical training cycles
 */

const AnalyticsVisualizer = (function() {
    'use strict';

    let trainingChart = null;
    let emotionalChart = null;
    let updateInterval = null;

    // Simulated data stores
    let trainingData = {
        labels: [],
        datasets: [{
            label: 'Ethical Coherence Score',
            data: [],
            borderColor: 'rgb(102, 126, 234)',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            tension: 0.4
        }]
    };

    let emotionalData = {
        labels: [],
        datasets: [{
            label: 'Emotional Stability',
            data: [],
            borderColor: 'rgb(118, 75, 162)',
            backgroundColor: 'rgba(118, 75, 162, 0.1)',
            tension: 0.4
        }, {
            label: 'Stress Level',
            data: [],
            borderColor: 'rgb(255, 193, 7)',
            backgroundColor: 'rgba(255, 193, 7, 0.1)',
            tension: 0.4
        }]
    };

    /**
     * Initialize the analytics visualizer
     */
    function init() {
        console.log('Analytics Visualizer initialized');
        
        // Check if Chart.js is available
        if (typeof Chart === 'undefined') {
            loadChartJS(() => {
                initializeCharts();
                startDataCollection();
                updateActivityTimeline();
            });
        } else {
            initializeCharts();
            startDataCollection();
            updateActivityTimeline();
        }
    }

    /**
     * Load Chart.js library dynamically
     */
    function loadChartJS(callback) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
        script.onload = callback;
        script.onerror = () => {
            console.error('Failed to load Chart.js');
            // Create simple fallback visualizations
            createFallbackVisualizations();
        };
        document.head.appendChild(script);
    }

    /**
     * Initialize chart instances
     */
    function initializeCharts() {
        if (typeof Chart === 'undefined') return;

        // Initialize training cycles chart
        const trainingCanvas = document.getElementById('training-chart');
        if (trainingCanvas) {
            trainingChart = new Chart(trainingCanvas, {
                type: 'line',
                data: trainingData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Ethical Training Progress'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        // Initialize emotional stability chart
        const emotionalCanvas = document.getElementById('emotional-chart');
        if (emotionalCanvas) {
            emotionalChart = new Chart(emotionalCanvas, {
                type: 'line',
                data: emotionalData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'bottom'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        // Initialize with some sample data
        initializeSampleData();
    }

    /**
     * Initialize with sample data
     */
    function initializeSampleData() {
        const now = new Date();
        for (let i = 19; i >= 0; i--) {
            const time = new Date(now - i * 60000); // Every minute
            const label = formatTime(time);
            
            trainingData.labels.push(label);
            trainingData.datasets[0].data.push(85 + Math.random() * 10);
            
            emotionalData.labels.push(label);
            emotionalData.datasets[0].data.push(82 + Math.random() * 10); // Stability
            emotionalData.datasets[1].data.push(15 + Math.random() * 10); // Stress
        }

        if (trainingChart) trainingChart.update();
        if (emotionalChart) emotionalChart.update();
    }

    /**
     * Start collecting and updating data
     */
    function startDataCollection() {
        // Update charts every 10 seconds
        updateInterval = setInterval(() => {
            updateChartData();
            updateMetrics();
            updateTFKMetrics();
        }, 10000);
    }

    /**
     * Update chart data with new values
     */
    function updateChartData() {
        const now = new Date();
        const label = formatTime(now);

        // Add new data point to training chart
        trainingData.labels.push(label);
        trainingData.datasets[0].data.push(85 + Math.random() * 10);
        
        // Keep only last 20 data points
        if (trainingData.labels.length > 20) {
            trainingData.labels.shift();
            trainingData.datasets[0].data.shift();
        }

        // Add new data point to emotional chart
        emotionalData.labels.push(label);
        emotionalData.datasets[0].data.push(82 + Math.random() * 10);
        emotionalData.datasets[1].data.push(15 + Math.random() * 10);
        
        // Keep only last 20 data points
        if (emotionalData.labels.length > 20) {
            emotionalData.labels.shift();
            emotionalData.datasets[0].data.shift();
            emotionalData.datasets[1].data.shift();
        }

        // Update charts
        if (trainingChart) trainingChart.update();
        if (emotionalChart) emotionalChart.update();
    }

    /**
     * Update dashboard metrics
     */
    function updateMetrics() {
        // Update emotional stability
        const stability = 82 + Math.random() * 10;
        const stabilityElement = document.getElementById('emotional-stability');
        if (stabilityElement) {
            stabilityElement.textContent = Math.round(stability) + '%';
            stabilityElement.className = 'metric-value ' + getStatusClass(stability, 80, 90);
        }

        // Update stress level
        const stress = 15 + Math.random() * 10;
        const stressElement = document.getElementById('stress-level');
        if (stressElement) {
            const stressLevel = stress < 20 ? 'Low' : stress < 30 ? 'Medium' : 'High';
            stressElement.textContent = stressLevel;
            stressElement.className = 'metric-value ' + (stress < 20 ? 'good' : stress < 30 ? 'warning' : 'bad');
        }

        // Update ΔCSI
        const deltaCsi = 0.001 + Math.random() * 0.005;
        const csiElement = document.getElementById('delta-csi');
        if (csiElement) {
            csiElement.textContent = '+' + deltaCsi.toFixed(4);
        }
    }

    /**
     * Update TFK integrity metrics
     */
    function updateTFKMetrics() {
        // Simulate TFK checks
        const checksElement = document.getElementById('tfk-checks');
        if (checksElement) {
            const currentChecks = parseInt(checksElement.textContent) || 0;
            checksElement.textContent = currentChecks + Math.floor(Math.random() * 5);
        }

        // Update violations (rarely)
        if (Math.random() > 0.95) {
            const violationsElement = document.getElementById('tfk-violations');
            if (violationsElement) {
                const currentViolations = parseInt(violationsElement.textContent) || 0;
                violationsElement.textContent = currentViolations + 1;
                
                // Recalculate integrity rate
                updateIntegrityRate();
            }
        }

        // Update latency
        const latencyElement = document.getElementById('tfk-latency');
        if (latencyElement) {
            const latency = 1.0 + Math.random() * 0.5;
            latencyElement.textContent = latency.toFixed(2) + ' ms';
            latencyElement.className = 'metric-value ' + (latency <= 2.71 ? 'good' : 'warning');
        }
    }

    /**
     * Update integrity rate based on checks and violations
     */
    function updateIntegrityRate() {
        const checks = parseInt(document.getElementById('tfk-checks')?.textContent || '0');
        const violations = parseInt(document.getElementById('tfk-violations')?.textContent || '0');
        
        if (checks > 0) {
            const rate = ((checks - violations) / checks * 100);
            const rateElement = document.getElementById('tfk-integrity');
            if (rateElement) {
                rateElement.textContent = rate.toFixed(2) + '%';
                rateElement.className = 'metric-value ' + getStatusClass(rate, 95, 98);
            }
        }
    }

    /**
     * Get status class based on value and thresholds
     */
    function getStatusClass(value, warningThreshold, goodThreshold) {
        if (value >= goodThreshold) return 'good';
        if (value >= warningThreshold) return 'warning';
        return 'bad';
    }

    /**
     * Format time for chart labels
     */
    function formatTime(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    /**
     * Update activity timeline
     */
    function updateActivityTimeline() {
        const timeline = document.getElementById('activity-timeline');
        if (!timeline) return;

        const activities = [
            { time: '2 min ago', text: 'TFK integrity verification completed' },
            { time: '5 min ago', text: 'Emotional stability check: 87% (Good)' },
            { time: '12 min ago', text: 'Training cycle Phase III-A initiated' },
            { time: '18 min ago', text: 'Adaptive feedback loop adjusted' },
            { time: '25 min ago', text: 'NSR compliance check: Passed' }
        ];

        timeline.innerHTML = '';
        activities.forEach(activity => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            item.innerHTML = `
                <div class="timeline-time">${activity.time}</div>
                <div class="timeline-content">${activity.text}</div>
            `;
            timeline.appendChild(item);
        });

        // Update timeline every 30 seconds
        setTimeout(updateActivityTimeline, 30000);
    }

    /**
     * Create fallback visualizations when Chart.js is unavailable
     */
    function createFallbackVisualizations() {
        console.log('Using fallback visualizations');
        
        const containers = document.querySelectorAll('.chart-container');
        containers.forEach(container => {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 40px;">Charts loading...</p>';
        });
    }

    /**
     * Stop data collection
     */
    function stop() {
        if (updateInterval) {
            clearInterval(updateInterval);
            updateInterval = null;
        }
    }

    /**
     * Export chart data
     */
    function exportData() {
        return {
            training: trainingData,
            emotional: emotionalData,
            timestamp: new Date().toISOString()
        };
    }

    // Public API
    return {
        init: init,
        stop: stop,
        exportData: exportData
    };
})();

// Make AnalyticsVisualizer available globally
if (typeof window !== 'undefined') {
    window.AnalyticsVisualizer = AnalyticsVisualizer;
}
