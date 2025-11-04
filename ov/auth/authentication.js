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
   * Hash password using PBKDF2 (more secure than SHA-256)
   * @private
   */
  hashPassword(password) {
    // Use PBKDF2 with a salt for password hashing
    // In production, each user should have a unique salt
    const salt = CryptoJS.lib.WordArray.random(128/8);
    const iterations = 10000; // Number of iterations
    const keySize = 256/32; // 256 bits
    
    const hash = CryptoJS.PBKDF2(password, salt, {
      keySize: keySize,
      iterations: iterations
    });
    
    return {
      hash: hash.toString(),
      salt: salt.toString(),
      iterations: iterations
    };
  }

  /**
   * Verify password against stored hash
   * @private
   */
  verifyPassword(password, storedHash, storedSalt, iterations = 10000) {
    const keySize = 256/32;
    const hash = CryptoJS.PBKDF2(password, CryptoJS.enc.Hex.parse(storedSalt), {
      keySize: keySize,
      iterations: iterations
    });
    
    return hash.toString() === storedHash;
  }

  /**
   * Store user credentials securely
   * @param {string} username - Username
   * @param {string} password - Password (will be hashed using PBKDF2)
   * @param {Object} facialFeatures - Facial recognition features
   */
  storeCredentials(username, password, facialFeatures = null) {
    const credentials = this.getCredentials() || {};
    
    // Hash password using PBKDF2
    const passwordData = this.hashPassword(password);
    
    credentials[username] = {
      passwordHash: passwordData.hash,
      passwordSalt: passwordData.salt,
      iterations: passwordData.iterations,
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

    const userData = credentials[username];
    const isValid = this.verifyPassword(
      password, 
      userData.passwordHash, 
      userData.passwordSalt,
      userData.iterations || 10000
    );
    
    if (isValid) {
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
