/**
 * OV: Open Visual - Authentication Module
 * Handles user authentication with facial recognition and manual login fallback
 */

import CryptoJS from 'crypto-js';
import FacialRecognition from '../facial-recognition.js';

class Authentication {
  constructor() {
    this.facialRecognition = new FacialRecognition();
    this.storageKey = 'ov_credentials';
    this.encryptionKey = this.getOrCreateEncryptionKey();
  }

  /**
   * Get or create AES-256 encryption key
   * @private
   */
  getOrCreateEncryptionKey() {
    const keyName = 'ov_encryption_key';
    let key = localStorage.getItem(keyName);
    
    if (!key) {
      // Generate a random 256-bit key
      key = CryptoJS.lib.WordArray.random(32).toString();
      localStorage.setItem(keyName, key);
    }
    
    return key;
  }

  /**
   * Encrypt data using AES-256
   * @private
   */
  encrypt(data) {
    const jsonStr = JSON.stringify(data);
    return CryptoJS.AES.encrypt(jsonStr, this.encryptionKey).toString();
  }

  /**
   * Decrypt data using AES-256
   * @private
   */
  decrypt(encryptedData) {
    try {
      const bytes = CryptoJS.AES.decrypt(encryptedData, this.encryptionKey);
      const decryptedStr = bytes.toString(CryptoJS.enc.Utf8);
      return JSON.parse(decryptedStr);
    } catch (error) {
      console.error('Decryption failed:', error);
      return null;
    }
  }

  /**
   * Store user credentials securely
   * @param {string} username - Username
   * @param {string} password - Password (will be hashed)
   * @param {Object} facialFeatures - Facial recognition features
   */
  storeCredentials(username, password, facialFeatures = null) {
    const credentials = this.getCredentials() || {};
    
    // Hash password
    const passwordHash = CryptoJS.SHA256(password).toString();
    
    credentials[username] = {
      passwordHash,
      facialFeatures,
      createdAt: Date.now(),
      lastLogin: null
    };

    const encrypted = this.encrypt(credentials);
    localStorage.setItem(this.storageKey, encrypted);
  }

  /**
   * Get all stored credentials
   * @private
   */
  getCredentials() {
    const encrypted = localStorage.getItem(this.storageKey);
    if (!encrypted) return null;
    return this.decrypt(encrypted);
  }

  /**
   * Update last login timestamp
   * @private
   */
  updateLastLogin(username) {
    const credentials = this.getCredentials();
    if (credentials && credentials[username]) {
      credentials[username].lastLogin = Date.now();
      const encrypted = this.encrypt(credentials);
      localStorage.setItem(this.storageKey, encrypted);
    }
  }

  /**
   * Authenticate user with facial recognition
   * @param {string} username - Username
   * @param {HTMLVideoElement} videoElement - Video element with camera feed
   * @returns {Promise<Object>} Authentication result
   */
  async authenticateWithFace(username, videoElement) {
    const credentials = this.getCredentials();
    
    if (!credentials || !credentials[username]) {
      return {
        success: false,
        method: 'facial',
        error: 'User not found'
      };
    }

    const storedFeatures = credentials[username].facialFeatures;
    if (!storedFeatures) {
      return {
        success: false,
        method: 'facial',
        error: 'No facial data registered for this user'
      };
    }

    try {
      await this.facialRecognition.initialize();
      const isMatch = await this.facialRecognition.verifyFace(videoElement, storedFeatures);
      
      if (isMatch) {
        this.updateLastLogin(username);
        return {
          success: true,
          method: 'facial',
          username,
          timestamp: Date.now()
        };
      } else {
        return {
          success: false,
          method: 'facial',
          error: 'Face verification failed'
        };
      }
    } catch (error) {
      console.error('Facial authentication error:', error);
      return {
        success: false,
        method: 'facial',
        error: error.message
      };
    }
  }

  /**
   * Authenticate user with manual credentials (fallback)
   * @param {string} username - Username
   * @param {string} password - Password
   * @returns {Object} Authentication result
   */
  authenticateWithPassword(username, password) {
    const credentials = this.getCredentials();
    
    if (!credentials || !credentials[username]) {
      return {
        success: false,
        method: 'password',
        error: 'User not found'
      };
    }

    const passwordHash = CryptoJS.SHA256(password).toString();
    
    if (credentials[username].passwordHash === passwordHash) {
      this.updateLastLogin(username);
      return {
        success: true,
        method: 'password',
        username,
        timestamp: Date.now()
      };
    } else {
      return {
        success: false,
        method: 'password',
        error: 'Incorrect password'
      };
    }
  }

  /**
   * Check if user exists
   * @param {string} username - Username to check
   * @returns {boolean}
   */
  userExists(username) {
    const credentials = this.getCredentials();
    return credentials && credentials[username] !== undefined;
  }

  /**
   * Get user profile (without sensitive data)
   * @param {string} username - Username
   * @returns {Object|null} User profile
   */
  getUserProfile(username) {
    const credentials = this.getCredentials();
    if (!credentials || !credentials[username]) {
      return null;
    }

    const user = credentials[username];
    return {
      username,
      hasFacialRecognition: !!user.facialFeatures,
      createdAt: user.createdAt,
      lastLogin: user.lastLogin
    };
  }

  /**
   * Delete user credentials
   * @param {string} username - Username to delete
   * @returns {boolean} Success status
   */
  deleteUser(username) {
    const credentials = this.getCredentials();
    if (!credentials || !credentials[username]) {
      return false;
    }

    delete credentials[username];
    const encrypted = this.encrypt(credentials);
    localStorage.setItem(this.storageKey, encrypted);
    return true;
  }
}

export default Authentication;
