/**
 * OV: Open Visual - Facial Recognition Module
 * Implements facial detection and recognition using TensorFlow.js
 */

import * as faceDetection from '@tensorflow-models/face-detection';
import '@tensorflow/tfjs-backend-webgl';

class FacialRecognition {
  constructor() {
    this.detector = null;
    this.model = null;
    this.isInitialized = false;
  }

  /**
   * Initialize the face detection model
   */
  async initialize() {
    if (this.isInitialized) return;

    try {
      // Create detector with MediaPipe FaceDetector
      const model = faceDetection.SupportedModels.MediaPipeFaceDetector;
      const detectorConfig = {
        runtime: 'tfjs',
        maxFaces: 1,
        refineLandmarks: true
      };
      
      this.detector = await faceDetection.createDetector(model, detectorConfig);
      this.isInitialized = true;
      console.log('Facial recognition initialized successfully');
    } catch (error) {
      console.error('Failed to initialize facial recognition:', error);
      throw error;
    }
  }

  /**
   * Detect faces in a video element or image
   * @param {HTMLVideoElement|HTMLImageElement} media - Media element to analyze
   * @returns {Promise<Array>} Array of detected faces
   */
  async detectFaces(media) {
    if (!this.isInitialized) {
      await this.initialize();
    }

    try {
      const faces = await this.detector.estimateFaces(media, {
        flipHorizontal: false
      });
      return faces;
    } catch (error) {
      console.error('Face detection error:', error);
      return [];
    }
  }

  /**
   * Extract facial features for recognition
   * @param {Array} faces - Detected faces from detectFaces
   * @returns {Object} Facial feature descriptor
   */
  extractFeatures(faces) {
    if (!faces || faces.length === 0) {
      return null;
    }

    const face = faces[0];
    const keypoints = face.keypoints;
    
    // Create a simple feature descriptor from keypoints
    const features = {
      boundingBox: face.box,
      keypoints: keypoints.map(kp => ({
        x: kp.x,
        y: kp.y,
        name: kp.name
      })),
      timestamp: Date.now()
    };

    return features;
  }

  /**
   * Compare two facial feature descriptors
   * @param {Object} features1 - First feature descriptor
   * @param {Object} features2 - Second feature descriptor
   * @returns {number} Similarity score (0-1)
   */
  compareFaces(features1, features2) {
    if (!features1 || !features2) {
      return 0;
    }

    // Simple Euclidean distance calculation between keypoints
    const kp1 = features1.keypoints;
    const kp2 = features2.keypoints;

    if (kp1.length !== kp2.length) {
      return 0;
    }

    let totalDistance = 0;
    for (let i = 0; i < kp1.length; i++) {
      const dx = kp1[i].x - kp2[i].x;
      const dy = kp1[i].y - kp2[i].y;
      totalDistance += Math.sqrt(dx * dx + dy * dy);
    }

    // Normalize to 0-1 similarity score (inverse of distance)
    const avgDistance = totalDistance / kp1.length;
    const similarity = Math.max(0, 1 - (avgDistance / 100));
    
    return similarity;
  }

  /**
   * Verify if a face matches the stored features
   * @param {HTMLVideoElement|HTMLImageElement} media - Media element
   * @param {Object} storedFeatures - Previously stored facial features
   * @param {number} threshold - Similarity threshold (default 0.7)
   * @returns {Promise<boolean>} Whether the face matches
   */
  async verifyFace(media, storedFeatures, threshold = 0.7) {
    const faces = await this.detectFaces(media);
    const currentFeatures = this.extractFeatures(faces);
    
    if (!currentFeatures) {
      return false;
    }

    const similarity = this.compareFaces(currentFeatures, storedFeatures);
    return similarity >= threshold;
  }

  /**
   * Cleanup resources
   */
  dispose() {
    if (this.detector) {
      this.detector.dispose();
      this.detector = null;
    }
    this.isInitialized = false;
  }
}

export default FacialRecognition;
