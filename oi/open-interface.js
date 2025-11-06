/**
 * OI: Open Interface - Main Interface Controller
 * Manages the augmented reality environment and user interactions
 * Integrates with backend server at https://oi-x3xa.onrender.com
 */

import AREnvironment from './ar/ar-environment.js';
import AnalyticsEngine from './analytics/analytics-engine.js';
import BackendAPI from '../ov/backend-api.js';

class OpenInterface {
  constructor(containerElement) {
    this.container = containerElement;
    this.arEnvironment = null;
    this.analytics = new AnalyticsEngine();
    this.api = new BackendAPI();
    this.currentUser = null;
    this.isInitialized = false;
    this.useBackend = true; // Use backend API by default
  }

  /**
   * Initialize the Open Interface
   * @param {Object} userSession - User session from OV authentication
   */
  initialize(userSession) {
    if (this.isInitialized) return;

    // Validate user session
    if (!userSession || !userSession.username) {
      throw new Error('Valid user session required');
    }

    this.currentUser = userSession;

    // Initialize AR environment
    this.arEnvironment = new AREnvironment(this.container);
    this.arEnvironment.initialize();

    // Enable analytics
    this.analytics.enableTelemetry();

    // Create default workspace for user
    const workspaceId = `workspace_${userSession.username}_${Date.now()}`;
    this.arEnvironment.allocateWorkspace(workspaceId, {
      owner: userSession.username,
      color: 0x0f766e
    });
    this.arEnvironment.setActiveWorkspace(workspaceId);

    // Track initialization
    this.analytics.updateActiveUsers(1);
    this.analytics.updateWorkspaceCount(1);
    this.analytics.trackUserActivity(userSession.username, 'initialized', {
      workspaceId
    });

    this.isInitialized = true;

    // Start performance tracking
    this.startPerformanceTracking();
  }

  /**
   * Start performance tracking
   * @private
   */
  startPerformanceTracking() {
    setInterval(() => {
      const fps = this.analytics.calculateFPS();
      this.analytics.trackPerformance({ fps });
    }, 1000);
  }

  /**
   * Create a new collaborative workspace
   * @param {string} name - Workspace name
   * @param {Object} config - Workspace configuration
   * @returns {Promise<string>} Workspace ID
   */
  async createWorkspace(name, config = {}) {
    const workspaceData = {
      name,
      owner: this.currentUser.username,
      ...config
    };

    if (this.useBackend) {
      try {
        const result = await this.api.createWorkspace(workspaceData);
        const workspaceId = result.id || `workspace_${name}_${Date.now()}`;
        
        // Also create in local AR environment
        this.arEnvironment.allocateWorkspace(workspaceId, {
          owner: this.currentUser.username,
          ...config
        });

        this.analytics.updateWorkspaceCount(
          this.arEnvironment.workspaces.size
        );

        this.analytics.trackUserActivity(
          this.currentUser.username,
          'create_workspace',
          { workspaceId, name }
        );

        return workspaceId;
      } catch (error) {
        console.error('Failed to create workspace on backend:', error);
        // Fallback to local creation
      }
    }

    // Local creation (fallback or when backend disabled)
    const workspaceId = `workspace_${name}_${Date.now()}`;
    
    this.arEnvironment.allocateWorkspace(workspaceId, {
      owner: this.currentUser.username,
      ...config
    });

    this.analytics.updateWorkspaceCount(
      this.arEnvironment.workspaces.size
    );

    this.analytics.trackUserActivity(
      this.currentUser.username,
      'create_workspace',
      { workspaceId, name }
    );

    return workspaceId;
  }

  /**
   * Switch to a different workspace
   * @param {string} workspaceId - Target workspace ID
   * @returns {boolean} Success status
   */
  switchWorkspace(workspaceId) {
    const success = this.arEnvironment.setActiveWorkspace(workspaceId);
    
    if (success) {
      this.analytics.trackUserActivity(
        this.currentUser.username,
        'switch_workspace',
        { workspaceId }
      );
    }

    return success;
  }

  /**
   * Add a file to the current workspace
   * @param {Object} fileInfo - File information
   * @returns {Promise<Object>} File object data
   */
  async addFile(fileInfo) {
    const workspaceId = this.arEnvironment.activeWorkspace;
    if (!workspaceId) {
      throw new Error('No active workspace');
    }

    if (this.useBackend) {
      try {
        await this.api.addFileToWorkspace(workspaceId, fileInfo);
      } catch (error) {
        console.error('Failed to add file to backend:', error);
      }
    }

    const fileObject = this.arEnvironment.createFileObject(fileInfo);
    
    // Position file in 3D space
    fileObject.position.set(
      Math.random() * 2 - 1,
      Math.random() * 2 - 1,
      Math.random() * 2 - 1
    );

    const objectData = this.arEnvironment.addObjectToWorkspace(
      workspaceId,
      fileObject,
      { type: 'file', ...fileInfo }
    );

    this.analytics.trackUserActivity(
      this.currentUser.username,
      'add_file',
      { workspaceId, fileId: objectData.id, fileName: fileInfo.name }
    );

    return objectData;
  }

    this.analytics.trackUserActivity(
      this.currentUser.username,
      'add_file',
      { workspaceId, fileId: objectData.id, fileName: fileInfo.name }
    );

    return objectData;
  }

  /**
   * Invite collaborator to workspace
   * @param {string} workspaceId - Workspace ID
   * @param {string} userId - User ID to invite
   * @param {Object} userData - User data
   */
  inviteCollaborator(workspaceId, userId, userData = {}) {
    const collaborator = this.arEnvironment.addCollaborator(
      workspaceId,
      userId,
      userData
    );

    if (collaborator) {
      this.analytics.trackUserActivity(
        this.currentUser.username,
        'invite_collaborator',
        { workspaceId, invitedUser: userId }
      );
    }

    return collaborator;
  }

  /**
   * Get workspace information
   * @param {string} workspaceId - Workspace ID
   * @returns {Object} Workspace information
   */
  getWorkspaceInfo(workspaceId) {
    return this.arEnvironment.getWorkspaceInfo(workspaceId);
  }

  /**
   * Get all workspaces
   * @returns {Array} Array of workspace information
   */
  getAllWorkspaces() {
    const workspaces = [];
    
    this.arEnvironment.workspaces.forEach((workspace, id) => {
      workspaces.push(this.getWorkspaceInfo(id));
    });

    return workspaces;
  }

  /**
   * Toggle analytics telemetry
   * @returns {boolean} New telemetry state
   */
  toggleAnalytics() {
    const newState = this.analytics.toggleTelemetry();
    
    this.analytics.trackUserActivity(
      this.currentUser.username,
      'toggle_analytics',
      { enabled: newState }
    );

    return newState;
  }

  /**
   * Get current analytics metrics
   * @returns {Object} Current metrics
   */
  getMetrics() {
    return this.analytics.getCurrentMetrics();
  }

  /**
   * Get analytics dashboard data
   * @returns {Object} Dashboard data
   */
  getAnalyticsDashboard() {
    return {
      current: this.analytics.getCurrentMetrics(),
      history: this.analytics.getMetricsHistory(50),
      aggregated: this.analytics.getAggregatedStats(300000) // Last 5 minutes
    };
  }

  /**
   * Subscribe to analytics events
   * @param {string} eventType - Event type
   * @param {Function} callback - Callback function
   * @returns {string} Subscription ID
   */
  subscribeToAnalytics(eventType, callback) {
    return this.analytics.subscribe(eventType, callback);
  }

  /**
   * Unsubscribe from analytics events
   * @param {string} subscriptionId - Subscription ID
   */
  unsubscribeFromAnalytics(subscriptionId) {
    this.analytics.unsubscribe(subscriptionId);
  }

  /**
   * Export analytics data
   * @param {string} format - Export format (json, csv)
   * @returns {string} Exported data
   */
  exportAnalytics(format = 'json') {
    return this.analytics.exportData(format);
  }

  /**
   * Cleanup and shutdown
   */
  shutdown() {
    this.analytics.trackUserActivity(
      this.currentUser.username,
      'shutdown',
      {}
    );

    this.analytics.disableTelemetry();
    
    if (this.arEnvironment) {
      this.arEnvironment.dispose();
    }

    this.isInitialized = false;
  }
}

export default OpenInterface;
