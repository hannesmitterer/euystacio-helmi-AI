/**
 * OV: Open Visual - Registration Module
 * Handles user registration with facial scan validation
 * Integrates with backend server at https://oi-x3xa.onrender.com
 */

import Authentication from './authentication.js';
import FacialRecognition from '../facial-recognition.js';
import BackendAPI from '../backend-api.js';

class Registration {
  constructor() {
    this.auth = new Authentication();
    this.facialRecognition = new FacialRecognition();
    this.api = new BackendAPI();
    this.useBackend = true; // Use backend API by default
  }

  /**
   * Validate user details
   * @private
   */
  validateUserDetails(userDetails) {
    const errors = [];

    if (!userDetails.username || userDetails.username.length < 3) {
      errors.push('Username must be at least 3 characters');
    }

    if (!userDetails.password || userDetails.password.length < 8) {
      errors.push('Password must be at least 8 characters');
    }

    if (!userDetails.email || !this.isValidEmail(userDetails.email)) {
      errors.push('Valid email is required');
    }

    return errors;
  }

  /**
   * Validate email format
   * @private
   */
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Capture facial features from video
   * @param {HTMLVideoElement} videoElement - Video element with camera feed
   * @returns {Promise<Object|null>} Facial features or null if capture failed
   */
  async captureFacialFeatures(videoElement) {
    try {
      await this.facialRecognition.initialize();
      const faces = await this.facialRecognition.detectFaces(videoElement);
      
      if (faces.length === 0) {
        return {
          success: false,
          error: 'No face detected. Please position your face in the camera.'
        };
      }

      if (faces.length > 1) {
        return {
          success: false,
          error: 'Multiple faces detected. Please ensure only one person is in frame.'
        };
      }

      const features = this.facialRecognition.extractFeatures(faces);
      
      if (!features) {
        return {
          success: false,
          error: 'Failed to extract facial features'
        };
      }

      return {
        success: true,
        features
      };
    } catch (error) {
      console.error('Facial capture error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Register new user with optional facial recognition
   * @param {Object} userDetails - User details (username, password, email, etc.)
   * @param {HTMLVideoElement} videoElement - Optional video element for facial scan
   * @param {File} documentFile - Optional document upload for validation
   * @returns {Promise<Object>} Registration result
   */
  async registerUser(userDetails, videoElement = null, documentFile = null) {
    // Validate user details
    const validationErrors = this.validateUserDetails(userDetails);
    if (validationErrors.length > 0) {
      return {
        success: false,
        errors: validationErrors
      };
    }

    let facialFeatures = null;

    // Capture facial features if video element provided
    if (videoElement) {
      const captureResult = await this.captureFacialFeatures(videoElement);
      
      if (captureResult.success) {
        facialFeatures = captureResult.features;
      } else {
        // Facial scan is optional, log warning but continue
        console.warn('Facial scan failed:', captureResult.error);
      }
    }

    // Handle document upload if provided
    let documentUrl = null;
    if (documentFile) {
      if (this.useBackend) {
        try {
          const uploadResult = await this.api.uploadFile(documentFile, 'verification');
          documentUrl = uploadResult.url;
        } catch (error) {
          console.warn('Document upload failed:', error);
        }
      } else {
        const documentValidation = await this.validateDocument(documentFile);
        if (!documentValidation.valid) {
          console.warn('Document validation failed:', documentValidation.error);
        }
      }
    }

    if (this.useBackend) {
      // Use backend API for registration
      try {
        const registrationData = {
          username: userDetails.username,
          email: userDetails.email,
          password: userDetails.password,
          facialFeatures,
          documentUrl
        };

        const result = await this.api.register(registrationData);
        
        return {
          success: true,
          username: result.username || userDetails.username,
          hasFacialRecognition: !!facialFeatures,
          documentValidated: !!documentUrl,
          timestamp: Date.now()
        };
      } catch (error) {
        return {
          success: false,
          errors: [error.message || 'Registration failed']
        };
      }
    } else {
      // Fallback to local storage
      // Check if user already exists
      if (this.auth.userExists(userDetails.username)) {
        return {
          success: false,
          errors: ['Username already exists']
        };
      }

      try {
        this.auth.storeCredentials(
          userDetails.username,
          userDetails.password,
          facialFeatures
        );

        return {
          success: true,
          username: userDetails.username,
          hasFacialRecognition: !!facialFeatures,
          documentValidated: !!documentUrl,
          timestamp: Date.now()
        };
      } catch (error) {
        console.error('Registration error:', error);
        return {
          success: false,
          errors: ['Failed to register user: ' + error.message]
        };
      }
    }
  }
    } catch (error) {
      console.error('Registration error:', error);
      return {
        success: false,
        errors: ['Failed to register user: ' + error.message]
      };
    }
  }

  /**
   * Validate uploaded document
   * @private
   * @param {File} documentFile - Document file to validate
   * @returns {Promise<Object>} Validation result
   */
  async validateDocument(documentFile) {
    // Basic validation - check file type and size
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!allowedTypes.includes(documentFile.type)) {
      return {
        valid: false,
        error: 'Invalid file type. Allowed: JPEG, PNG, PDF'
      };
    }

    if (documentFile.size > maxSize) {
      return {
        valid: false,
        error: 'File size exceeds 5MB limit'
      };
    }

    // In a real implementation, this would:
    // - Extract text from document using OCR
    // - Verify document authenticity
    // - Cross-reference with facial recognition data
    
    return {
      valid: true,
      fileName: documentFile.name,
      fileSize: documentFile.size,
      fileType: documentFile.type
    };
  }

  /**
   * Re-prompt user for additional facial scans for security
   * @param {string} username - Username
   * @param {HTMLVideoElement} videoElement - Video element
   * @returns {Promise<Object>} Result of additional verification
   */
  async addSecurityScan(username, videoElement) {
    if (!this.auth.userExists(username)) {
      return {
        success: false,
        error: 'User not found'
      };
    }

    const profile = this.auth.getUserProfile(username);
    if (!profile.hasFacialRecognition) {
      return {
        success: false,
        error: 'User does not have facial recognition enabled'
      };
    }

    // Capture new facial scan
    const captureResult = await this.captureFacialFeatures(videoElement);
    
    if (!captureResult.success) {
      return captureResult;
    }

    // In a real implementation, this would store multiple facial scans
    // for improved recognition accuracy
    
    return {
      success: true,
      message: 'Additional security scan completed',
      timestamp: Date.now()
    };
  }
}

export default Registration;
