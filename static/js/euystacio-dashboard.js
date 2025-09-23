// Enhanced Euystacio Dashboard JavaScript
class EuystacioDashboard {
    constructor() {
        this.evolutionChart = null;
        this.refreshInterval = 10000; // 10 seconds
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.setupAutoRefresh();
        this.initChart();
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
                intensityValue.textContent = parseFloat(e.target.value).toFixed(1);
            });
        }

        // Reflection button
        const reflectBtn = document.getElementById('reflect-btn');
        if (reflectBtn) {
            reflectBtn.addEventListener('click', () => this.triggerReflection());
        }
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.loadKernelState(),
                this.loadPulseHistory(),
                this.loadEvolutionData()
            ]);
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showMessage('Failed to load initial data', 'error');
        }
    }

    async loadKernelState() {
        try {
            const response = await fetch('/api/kernel/state');
            const state = await response.json();
            this.displayKernelState(state);
        } catch (error) {
            console.error('Error loading kernel state:', error);
            this.showError('kernel-metrics', 'Failed to load kernel state');
        }
    }

    displayKernelState(state) {
        // Display main metrics
        const metricsContainer = document.getElementById('kernel-metrics');
        if (metricsContainer) {
            const metrics = state.mutable_values;
            const healthMetrics = state.health_metrics;
            
            metricsContainer.innerHTML = `
                <div class="state-metric">
                    <div class="metric-value">${(metrics.trust * 100).toFixed(0)}%</div>
                    <div class="metric-label">Trust</div>
                </div>
                <div class="state-metric">
                    <div class="metric-value">${(metrics.harmony * 100).toFixed(0)}%</div>
                    <div class="metric-label">Harmony</div>
                </div>
                <div class="state-metric">
                    <div class="metric-value">${(metrics.resonance * 100).toFixed(0)}%</div>
                    <div class="metric-label">Resonance</div>
                </div>
                <div class="state-metric">
                    <div class="metric-value">${(metrics.learning_rate * 100).toFixed(0)}%</div>
                    <div class="metric-label">Learning Rate</div>
                </div>
                <div class="state-metric">
                    <div class="metric-value">${(metrics.emotional_depth * 100).toFixed(0)}%</div>
                    <div class="metric-label">Emotional Depth</div>
                </div>
                <div class="state-metric">
                    <div class="metric-value">${state.total_pulses}</div>
                    <div class="metric-label">Total Pulses</div>
                </div>
            `;
        }

        // Display emotional state
        const emotionalStateContainer = document.getElementById('emotional-state');
        if (emotionalStateContainer) {
            const emotionalState = state.emotional_state;
            emotionalStateContainer.innerHTML = `
                <h4>Current Emotional State</h4>
                <p><strong>Primary Emotion:</strong> ${emotionalState.primary_emotion}</p>
                <p><strong>Intensity:</strong> ${(emotionalState.intensity * 100).toFixed(0)}%</p>
                <p><strong>Stability:</strong> ${(emotionalState.stability * 100).toFixed(0)}%</p>
                <p><strong>Openness:</strong> ${(emotionalState.openness * 100).toFixed(0)}%</p>
            `;
        }

        // Display health indicators
        const healthContainer = document.getElementById('health-indicators');
        if (healthContainer) {
            const health = state.health_metrics;
            healthContainer.innerHTML = `
                <div class="health-indicator">
                    <div class="health-circle ${this.getHealthClass(health.wellness)}">
                        ${(health.wellness * 100).toFixed(0)}%
                    </div>
                    <div>Wellness</div>
                </div>
                <div class="health-indicator">
                    <div class="health-circle ${this.getHealthClass(health.stability)}">
                        ${(health.stability * 100).toFixed(0)}%
                    </div>
                    <div>Stability</div>
                </div>
                <div class="health-indicator">
                    <div class="health-circle ${this.getHealthClass(health.growth_rate * 10)}">
                        ${(health.growth_rate * 100).toFixed(1)}%
                    </div>
                    <div>Growth Rate</div>
                </div>
            `;
        }
    }

    getHealthClass(value) {
        if (value > 0.7) return 'health-good';
        if (value > 0.4) return 'health-fair';
        return 'health-poor';
    }

    async loadPulseHistory() {
        try {
            const response = await fetch('/api/pulses');
            const pulses = await response.json();
            this.displayPulseHistory(pulses);
        } catch (error) {
            console.error('Error loading pulse history:', error);
            this.showError('pulse-history', 'Failed to load pulse history');
        }
    }

    displayPulseHistory(pulses) {
        const container = document.getElementById('pulse-history');
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
                    Intensity: ${(pulse.intensity * 100).toFixed(0)}% | 
                    Clarity: ${pulse.clarity || 'unknown'} | 
                    ${this.formatTimestamp(pulse.timestamp)}
                    ${pulse.resonance_score ? ` | Resonance: ${(pulse.resonance_score * 100).toFixed(0)}%` : ''}
                </div>
                ${pulse.context ? `<div class="pulse-note"><strong>Context:</strong> ${pulse.context}</div>` : ''}
                ${pulse.note ? `<div class="pulse-note"><strong>Note:</strong> "${pulse.note}"</div>` : ''}
            </div>
        `).join('');
    }

    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown time';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleString();
        } catch (e) {
            return 'Invalid time';
        }
    }

    async loadEvolutionData() {
        try {
            const response = await fetch('/api/kernel/evolution?hours=24');
            const data = await response.json();
            this.updateChart(data);
        } catch (error) {
            console.error('Error loading evolution data:', error);
        }
    }

    initChart() {
        const ctx = document.getElementById('evolution-chart');
        if (!ctx) return;

        this.evolutionChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Trust',
                        data: [],
                        borderColor: '#48bb78',
                        backgroundColor: 'rgba(72, 187, 120, 0.1)',
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'Harmony',
                        data: [],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'Resonance',
                        data: [],
                        borderColor: '#ed8936',
                        backgroundColor: 'rgba(237, 137, 54, 0.1)',
                        fill: false,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            callback: function(value) {
                                return (value * 100).toFixed(0) + '%';
                            }
                        }
                    },
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour',
                            displayFormats: {
                                hour: 'HH:mm'
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Kernel Evolution (Last 24 Hours)'
                    }
                }
            }
        });
    }

    updateChart(data) {
        if (!this.evolutionChart || !data.timestamps) return;

        const timestamps = data.timestamps.map(ts => new Date(ts));
        
        this.evolutionChart.data.labels = timestamps;
        this.evolutionChart.data.datasets[0].data = data.trust || [];
        this.evolutionChart.data.datasets[1].data = data.harmony || [];
        this.evolutionChart.data.datasets[2].data = data.resonance || [];
        
        this.evolutionChart.update();
    }

    async handlePulseSubmission(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        const pulseData = {
            emotion: formData.get('emotion'),
            intensity: parseFloat(formData.get('intensity')),
            context: formData.get('context'),
            note: formData.get('note'),
            clarity: formData.get('clarity')
        };

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
                this.showMessage(`Pulse sent successfully! Resonance: ${(result.resonance_score * 100).toFixed(0)}%`, 'success');
                
                // Reset form
                form.reset();
                document.getElementById('intensity-value').textContent = '0.5';
                
                // Refresh data after a short delay
                setTimeout(() => {
                    this.loadKernelState();
                    this.loadPulseHistory();
                    this.loadEvolutionData();
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
        const reflectBtn = document.getElementById('reflect-btn');
        const reflectionContent = document.getElementById('reflection-content');
        
        if (reflectBtn) reflectBtn.classList.add('loading');
        
        try {
            const response = await fetch('/api/reflect');
            const reflection = await response.json();
            
            if (reflectionContent) {
                reflectionContent.style.display = 'block';
                this.displayReflection(reflection);
            }
            
            this.showMessage('Reflection completed successfully', 'success');
        } catch (error) {
            console.error('Error triggering reflection:', error);
            this.showMessage('Failed to trigger reflection', 'error');
        } finally {
            if (reflectBtn) reflectBtn.classList.remove('loading');
        }
    }

    displayReflection(reflection) {
        const container = document.getElementById('reflection-content');
        if (!container) return;
        
        const kernelReflection = reflection.kernel_reflection || {};
        
        container.innerHTML = `
            <h4>✨ Kernel Reflection</h4>
            <p><strong>Current Wellness:</strong> ${(kernelReflection.current_wellness * 100).toFixed(0)}%</p>
            <p><strong>Growth Pattern:</strong> ${kernelReflection.growth_pattern || 'Unknown'}</p>
            <p><strong>Emotional Balance:</strong> ${kernelReflection.emotional_balance || 'Balanced'}</p>
            
            ${kernelReflection.dominant_values && kernelReflection.dominant_values.length > 0 ? `
                <p><strong>Dominant Values:</strong> ${kernelReflection.dominant_values.join(', ')}</p>
            ` : ''}
            
            ${kernelReflection.recent_insights && kernelReflection.recent_insights.length > 0 ? `
                <div>
                    <strong>Recent Insights:</strong>
                    <ul>
                        ${kernelReflection.recent_insights.map(insight => `<li>${insight}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${kernelReflection.recommendations && kernelReflection.recommendations.length > 0 ? `
                <div>
                    <strong>Recommendations:</strong>
                    <ul>
                        ${kernelReflection.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            <small>Generated: ${new Date(kernelReflection.timestamp).toLocaleString()}</small>
        `;
    }

    setupAutoRefresh() {
        setInterval(() => {
            this.loadKernelState();
            this.loadEvolutionData();
        }, this.refreshInterval);
    }

    showMessage(message, type = 'info') {
        const messagesContainer = document.getElementById('messages');
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;

        messagesContainer.appendChild(messageDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `<div class="message error">${message}</div>`;
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
    
    // Add loading indicators to buttons
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
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl+Enter or Cmd+Enter to submit pulse form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const pulseForm = document.getElementById('pulse-form');
            if (pulseForm) {
                e.preventDefault();
                pulseForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Ctrl+R or Cmd+R to trigger reflection
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            const reflectBtn = document.getElementById('reflect-btn');
            if (reflectBtn) {
                e.preventDefault();
                reflectBtn.click();
            }
        }
    });
});