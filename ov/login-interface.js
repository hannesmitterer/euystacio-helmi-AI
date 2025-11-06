/**
 * OV: Open Visual - Login Interface Component
 * Main interface for login with facial recognition and fallback
 */

import Authentication from './auth/authentication.js';
import FacialRecognition from './facial-recognition.js';

class LoginInterface {
  constructor() {
    this.auth = new Authentication();
    this.facialRecognition = new FacialRecognition();
    this.videoElement = null;
    this.stream = null;
    this.currentUsername = null;
  }

  /**
   * Initialize camera for facial recognition
   * @param {HTMLVideoElement} videoElement - Video element to display camera feed
   * @returns {Promise<boolean>} Success status
   */
  async initializeCamera(videoElement) {
    try {
      this.videoElement = videoElement;
      
      const constraints = {
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        }
      };

      this.stream = await navigator.mediaDevices.getUserMedia(constraints);
      this.videoElement.srcObject = this.stream;
      
      return new Promise((resolve) => {
        this.videoElement.onloadedmetadata = () => {
          this.videoElement.play();
          resolve(true);
        };
      });
    } catch (error) {
      console.error('Camera initialization failed:', error);
      return false;
    }
  }

  /**
   * Stop camera stream
   */
  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
    if (this.videoElement) {
      this.videoElement.srcObject = null;
    }
  }

  /**
   * Attempt facial recognition login
   * @param {string} username - Username to authenticate
   * @returns {Promise<Object>} Login result
   */
  async attemptFacialLogin(username) {
    this.currentUsername = username;

    if (!this.videoElement || !this.stream) {
      return {
        success: false,
        error: 'Camera not initialized',
        fallbackRequired: true
      };
    }

    const profile = this.auth.getUserProfile(username);
    if (!profile) {
      return {
        success: false,
        error: 'User not found',
        fallbackRequired: true
      };
    }

    if (!profile.hasFacialRecognition) {
      return {
        success: false,
        error: 'Facial recognition not enabled for this user',
        fallbackRequired: true
      };
    }

    const result = await this.auth.authenticateWithFace(username, this.videoElement);
    
    if (!result.success) {
      result.fallbackRequired = true;
    }

    return result;
  }

  /**
   * Fallback to manual password login
   * @param {string} username - Username
   * @param {string} password - Password
   * @returns {Promise<Object>} Login result
   */
  async fallbackLogin(username, password) {
    return await this.auth.authenticateWithPassword(username, password);
  }

  /**
   * Combined login attempt: tries facial recognition, falls back to password
   * @param {string} username - Username
   * @param {string} password - Password for fallback
   * @returns {Promise<Object>} Login result
   */
  async login(username, password = null) {
    // First, try facial recognition if camera is available
    if (this.stream && this.videoElement) {
      const facialResult = await this.attemptFacialLogin(username);
      
      if (facialResult.success) {
        this.stopCamera();
        return facialResult;
      }

      console.log('Facial recognition failed, attempting fallback login');
    }

    // Fallback to password if provided
    if (password) {
      const passwordResult = await this.fallbackLogin(username, password);
      this.stopCamera();
      return passwordResult;
    }

    // No password provided and facial failed
    return {
      success: false,
      error: 'Authentication failed. Please provide password.',
      fallbackRequired: true
    };
  }

  /**
   * Get current user session
   * @returns {Object|null} Current session or null
   */
  getCurrentSession() {
    const sessionKey = 'ov_current_session';
    const sessionData = localStorage.getItem(sessionKey);
    
    if (!sessionData) return null;

    try {
      const session = JSON.parse(sessionData);
      
      // Check if session is still valid (24 hours)
      const sessionAge = Date.now() - session.timestamp;
      const maxAge = 24 * 60 * 60 * 1000; // 24 hours
      
      if (sessionAge > maxAge) {
        this.logout();
        return null;
      }

      return session;
    } catch (error) {
      return null;
    }
  }

  /**
   * Create user session after successful login
   * @param {Object} loginResult - Result from successful login
   */
  createSession(loginResult) {
    const session = {
      username: loginResult.username,
      method: loginResult.method,
      timestamp: loginResult.timestamp,
      expiresAt: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
    };

    localStorage.setItem('ov_current_session', JSON.stringify(session));
  }

  /**
   * Logout and clear session
   */
  logout() {
    localStorage.removeItem('ov_current_session');
    this.stopCamera();
    this.currentUsername = null;
  }

  /**
   * Check if user is authenticated
   * @returns {boolean}
   */
  isAuthenticated() {
    const session = this.getCurrentSession();
    return session !== null;
  }

  /**
   * Redirect to OI (Open Interface) after successful authentication
   * @param {string} oiUrl - URL of the OI interface
   */
  redirectToOI(oiUrl = '/oi/interface.html') {
    const session = this.getCurrentSession();
    if (session) {
      window.location.href = oiUrl;
    }
  }
}

export default LoginInterface;
