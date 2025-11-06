/**
 * OI: Open Interface - Real-time Analytics Module
 * Provides telemetry feeds and analytics for the AR environment
 */

class AnalyticsEngine {
  constructor() {
    this.metrics = {
      activeUsers: 0,
      workspaces: 0,
      interactions: 0,
      performance: {
        fps: 0,
        latency: 0,
        renderTime: 0
      }
    };
    this.telemetryEnabled = false;
    this.listeners = new Map();
    this.metricsHistory = [];
    this.maxHistorySize = 1000;
  }

  /**
   * Enable telemetry collection
   */
  enableTelemetry() {
    this.telemetryEnabled = true;
    this.startMetricsCollection();
  }

  /**
   * Disable telemetry collection
   */
  disableTelemetry() {
    this.telemetryEnabled = false;
    this.stopMetricsCollection();
  }

  /**
   * Toggle telemetry on/off
   * @returns {boolean} New telemetry state
   */
  toggleTelemetry() {
    if (this.telemetryEnabled) {
      this.disableTelemetry();
    } else {
      this.enableTelemetry();
    }
    return this.telemetryEnabled;
  }

  /**
   * Start metrics collection
   * @private
   */
  startMetricsCollection() {
    this.metricsInterval = setInterval(() => {
      if (this.telemetryEnabled) {
        this.collectMetrics();
      }
    }, 1000); // Collect every second
  }

  /**
   * Stop metrics collection
   * @private
   */
  stopMetricsCollection() {
    if (this.metricsInterval) {
      clearInterval(this.metricsInterval);
      this.metricsInterval = null;
    }
  }

  /**
   * Collect current metrics
   * @private
   */
  collectMetrics() {
    const snapshot = {
      timestamp: Date.now(),
      activeUsers: this.metrics.activeUsers,
      workspaces: this.metrics.workspaces,
      interactions: this.metrics.interactions,
      performance: { ...this.metrics.performance }
    };

    // Add to history
    this.metricsHistory.push(snapshot);

    // Trim history if too large
    if (this.metricsHistory.length > this.maxHistorySize) {
      this.metricsHistory.shift();
    }

    // Notify listeners
    this.notifyListeners('metrics', snapshot);
  }

  /**
   * Track user activity
   * @param {string} userId - User ID
   * @param {string} action - Action type
   * @param {Object} data - Additional data
   */
  trackUserActivity(userId, action, data = {}) {
    if (!this.telemetryEnabled) return;

    const activity = {
      timestamp: Date.now(),
      userId,
      action,
      data
    };

    this.metrics.interactions++;
    this.notifyListeners('activity', activity);
  }

  /**
   * Update active users count
   * @param {number} count - Number of active users
   */
  updateActiveUsers(count) {
    this.metrics.activeUsers = count;
  }

  /**
   * Update workspace count
   * @param {number} count - Number of workspaces
   */
  updateWorkspaceCount(count) {
    this.metrics.workspaces = count;
  }

  /**
   * Track performance metrics
   * @param {Object} perfData - Performance data
   */
  trackPerformance(perfData) {
    if (!this.telemetryEnabled) return;

    if (perfData.fps !== undefined) {
      this.metrics.performance.fps = perfData.fps;
    }
    if (perfData.latency !== undefined) {
      this.metrics.performance.latency = perfData.latency;
    }
    if (perfData.renderTime !== undefined) {
      this.metrics.performance.renderTime = perfData.renderTime;
    }

    this.notifyListeners('performance', this.metrics.performance);
  }

  /**
   * Calculate FPS (frames per second)
   * @returns {number} Current FPS
   */
  calculateFPS() {
    if (!this.lastFrameTime) {
      this.lastFrameTime = performance.now();
      this.frameCount = 0;
      return 0;
    }

    this.frameCount++;
    const currentTime = performance.now();
    const elapsed = currentTime - this.lastFrameTime;

    if (elapsed >= 1000) {
      const fps = Math.round((this.frameCount * 1000) / elapsed);
      this.metrics.performance.fps = fps;
      this.frameCount = 0;
      this.lastFrameTime = currentTime;
      return fps;
    }

    return this.metrics.performance.fps;
  }

  /**
   * Get current metrics
   * @returns {Object} Current metrics snapshot
   */
  getCurrentMetrics() {
    return {
      ...this.metrics,
      timestamp: Date.now()
    };
  }

  /**
   * Get metrics history
   * @param {number} limit - Maximum number of records to return
   * @returns {Array} Metrics history
   */
  getMetricsHistory(limit = 100) {
    const start = Math.max(0, this.metricsHistory.length - limit);
    return this.metricsHistory.slice(start);
  }

  /**
   * Get aggregated statistics
   * @param {number} timeWindow - Time window in milliseconds
   * @returns {Object} Aggregated statistics
   */
  getAggregatedStats(timeWindow = 60000) {
    const cutoff = Date.now() - timeWindow;
    const recentMetrics = this.metricsHistory.filter(m => m.timestamp >= cutoff);

    if (recentMetrics.length === 0) {
      return null;
    }

    // Calculate averages
    const avgActiveUsers = recentMetrics.reduce((sum, m) => sum + m.activeUsers, 0) / recentMetrics.length;
    const avgWorkspaces = recentMetrics.reduce((sum, m) => sum + m.workspaces, 0) / recentMetrics.length;
    const avgFPS = recentMetrics.reduce((sum, m) => sum + m.performance.fps, 0) / recentMetrics.length;
    const avgLatency = recentMetrics.reduce((sum, m) => sum + m.performance.latency, 0) / recentMetrics.length;

    return {
      timeWindow,
      sampleCount: recentMetrics.length,
      averages: {
        activeUsers: Math.round(avgActiveUsers),
        workspaces: Math.round(avgWorkspaces),
        fps: Math.round(avgFPS),
        latency: Math.round(avgLatency)
      },
      peak: {
        activeUsers: Math.max(...recentMetrics.map(m => m.activeUsers)),
        workspaces: Math.max(...recentMetrics.map(m => m.workspaces)),
        fps: Math.max(...recentMetrics.map(m => m.performance.fps))
      }
    };
  }

  /**
   * Subscribe to analytics events
   * @param {string} eventType - Event type (metrics, activity, performance)
   * @param {Function} callback - Callback function
   * @returns {string} Subscription ID
   */
  subscribe(eventType, callback) {
    const subscriptionId = `${eventType}_${Date.now()}_${Math.random()}`;
    
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, new Map());
    }

    this.listeners.get(eventType).set(subscriptionId, callback);
    return subscriptionId;
  }

  /**
   * Unsubscribe from analytics events
   * @param {string} subscriptionId - Subscription ID
   */
  unsubscribe(subscriptionId) {
    const [eventType] = subscriptionId.split('_');
    const listeners = this.listeners.get(eventType);
    
    if (listeners) {
      listeners.delete(subscriptionId);
    }
  }

  /**
   * Notify all listeners of an event
   * @private
   */
  notifyListeners(eventType, data) {
    const listeners = this.listeners.get(eventType);
    
    if (listeners) {
      listeners.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Error in analytics listener:', error);
        }
      });
    }
  }

  /**
   * Export analytics data
   * @param {string} format - Export format (json, csv)
   * @returns {string} Exported data
   */
  exportData(format = 'json') {
    if (format === 'json') {
      return JSON.stringify({
        currentMetrics: this.metrics,
        history: this.metricsHistory,
        exportedAt: Date.now()
      }, null, 2);
    } else if (format === 'csv') {
      const headers = 'timestamp,activeUsers,workspaces,interactions,fps,latency,renderTime\n';
      const rows = this.metricsHistory.map(m => 
        `${m.timestamp},${m.activeUsers},${m.workspaces},${m.interactions},${m.performance.fps},${m.performance.latency},${m.performance.renderTime}`
      ).join('\n');
      return headers + rows;
    }

    return '';
  }

  /**
   * Clear all analytics data
   */
  clearData() {
    this.metricsHistory = [];
    this.metrics = {
      activeUsers: 0,
      workspaces: 0,
      interactions: 0,
      performance: {
        fps: 0,
        latency: 0,
        renderTime: 0
      }
    };
  }
}

export default AnalyticsEngine;
