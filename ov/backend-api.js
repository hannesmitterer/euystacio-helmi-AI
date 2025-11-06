/**
 * Backend API Client for OV/OI modules
 * Handles communication with the backend server at https://oi-x3xa.onrender.com
 */

class BackendAPI {
  constructor() {
    this.baseUrl = 'https://oi-x3xa.onrender.com';
    this.apiUrl = `${this.baseUrl}/api`;
  }

  /**
   * Make an API request
   * @private
   */
  async request(endpoint, options = {}) {
    const url = `${this.apiUrl}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const config = { ...defaultOptions, ...options };
    
    // Add authorization token if available
    const token = this.getAuthToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: response.statusText }));
        throw new Error(error.message || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  /**
   * Get stored authentication token
   * @private
   */
  getAuthToken() {
    return localStorage.getItem('ov_auth_token');
  }

  /**
   * Store authentication token
   * @private
   */
  setAuthToken(token) {
    localStorage.setItem('ov_auth_token', token);
  }

  /**
   * Remove authentication token
   * @private
   */
  clearAuthToken() {
    localStorage.removeItem('ov_auth_token');
  }

  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} Registration result
   */
  async register(userData) {
    return await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  /**
   * Login with password
   * @param {string} username - Username
   * @param {string} password - Password
   * @returns {Promise<Object>} Login result with token
   */
  async loginWithPassword(username, password) {
    const result = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });

    if (result.token) {
      this.setAuthToken(result.token);
    }

    return result;
  }

  /**
   * Login with facial recognition
   * @param {string} username - Username
   * @param {Object} facialFeatures - Facial feature data
   * @returns {Promise<Object>} Login result with token
   */
  async loginWithFace(username, facialFeatures) {
    const result = await this.request('/auth/login/facial', {
      method: 'POST',
      body: JSON.stringify({ username, facialFeatures }),
    });

    if (result.token) {
      this.setAuthToken(result.token);
    }

    return result;
  }

  /**
   * Verify current session
   * @returns {Promise<Object>} User session data
   */
  async verifySession() {
    return await this.request('/auth/verify', {
      method: 'GET',
    });
  }

  /**
   * Logout
   * @returns {Promise<void>}
   */
  async logout() {
    try {
      await this.request('/auth/logout', {
        method: 'POST',
      });
    } finally {
      this.clearAuthToken();
    }
  }

  /**
   * Create a workspace
   * @param {Object} workspaceData - Workspace data
   * @returns {Promise<Object>} Created workspace
   */
  async createWorkspace(workspaceData) {
    return await this.request('/workspaces', {
      method: 'POST',
      body: JSON.stringify(workspaceData),
    });
  }

  /**
   * Get all workspaces for current user
   * @returns {Promise<Array>} List of workspaces
   */
  async getWorkspaces() {
    return await this.request('/workspaces', {
      method: 'GET',
    });
  }

  /**
   * Get specific workspace
   * @param {string} workspaceId - Workspace ID
   * @returns {Promise<Object>} Workspace data
   */
  async getWorkspace(workspaceId) {
    return await this.request(`/workspaces/${workspaceId}`, {
      method: 'GET',
    });
  }

  /**
   * Update workspace
   * @param {string} workspaceId - Workspace ID
   * @param {Object} updates - Workspace updates
   * @returns {Promise<Object>} Updated workspace
   */
  async updateWorkspace(workspaceId, updates) {
    return await this.request(`/workspaces/${workspaceId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  /**
   * Delete workspace
   * @param {string} workspaceId - Workspace ID
   * @returns {Promise<void>}
   */
  async deleteWorkspace(workspaceId) {
    return await this.request(`/workspaces/${workspaceId}`, {
      method: 'DELETE',
    });
  }

  /**
   * Add file to workspace
   * @param {string} workspaceId - Workspace ID
   * @param {Object} fileData - File metadata
   * @returns {Promise<Object>} Added file data
   */
  async addFileToWorkspace(workspaceId, fileData) {
    return await this.request(`/workspaces/${workspaceId}/files`, {
      method: 'POST',
      body: JSON.stringify(fileData),
    });
  }

  /**
   * Add collaborator to workspace
   * @param {string} workspaceId - Workspace ID
   * @param {string} userId - User ID to add
   * @returns {Promise<Object>} Updated workspace
   */
  async addCollaborator(workspaceId, userId) {
    return await this.request(`/workspaces/${workspaceId}/collaborators`, {
      method: 'POST',
      body: JSON.stringify({ userId }),
    });
  }

  /**
   * Track analytics event
   * @param {Object} eventData - Event data
   * @returns {Promise<void>}
   */
  async trackEvent(eventData) {
    return await this.request('/analytics/events', {
      method: 'POST',
      body: JSON.stringify(eventData),
    });
  }

  /**
   * Get analytics metrics
   * @param {Object} filters - Optional filters
   * @returns {Promise<Object>} Analytics data
   */
  async getAnalytics(filters = {}) {
    const params = new URLSearchParams(filters);
    return await this.request(`/analytics?${params}`, {
      method: 'GET',
    });
  }

  /**
   * Update user profile
   * @param {Object} profileData - Profile updates
   * @returns {Promise<Object>} Updated profile
   */
  async updateProfile(profileData) {
    return await this.request('/users/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }

  /**
   * Upload file (for documents, etc.)
   * @param {File} file - File to upload
   * @param {string} purpose - Purpose of upload (e.g., 'document', 'avatar')
   * @returns {Promise<Object>} Upload result with file URL
   */
  async uploadFile(file, purpose = 'document') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('purpose', purpose);

    const url = `${this.apiUrl}/upload`;
    const token = this.getAuthToken();
    
    const config = {
      method: 'POST',
      body: formData,
    };

    if (token) {
      config.headers = {
        'Authorization': `Bearer ${token}`,
      };
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ message: response.statusText }));
        throw new Error(error.message || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('File upload failed:', error);
      throw error;
    }
  }
}

export default BackendAPI;
