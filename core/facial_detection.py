"""
Facial Detection Integration for Euystacio
Wrapper for the AIML Human Attributes Detection submodule.
"""

import os
import sys
import cv2
import json
import logging
import tempfile
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from config import config

class FacialDetectionIntegration:
    """Integration wrapper for AIML Human Attributes Detection"""
    
    def __init__(self):
        self.enabled = config.is_facial_detection_enabled()
        self.submodule_path = config.get_submodule_path()
        self.logger = logging.getLogger(__name__)
        
        # Initialize models if enabled and available
        self._models_loaded = False
        if self.enabled and config.is_submodule_available():
            self._load_models()
    
    def _load_models(self):
        """Load the facial detection models"""
        try:
            # Add submodule to path for imports
            if str(self.submodule_path) not in sys.path:
                sys.path.insert(0, str(self.submodule_path))
            
            # Set up environment paths for the submodule
            os.chdir(self.submodule_path)
            
            # Load models (adapted from predict.py)
            env_file = self.submodule_path / '.env'
            if env_file.exists():
                from dotenv import load_dotenv
                load_dotenv(dotenv_path=env_file)
            
            # Load face detection model
            face_proto = os.getenv("FACEDETECTOR")
            face_model = os.getenv("FACEMODEL")
            
            if face_proto and face_model and Path(face_proto).exists() and Path(face_model).exists():
                self.face_net = cv2.dnn.readNet(face_model, face_proto)
                self._models_loaded = True
                self.logger.info("Facial detection models loaded successfully")
            else:
                self.logger.warning("Facial detection model files not found")
                
        except Exception as e:
            self.logger.error(f"Failed to load facial detection models: {e}")
            self._models_loaded = False
    
    def is_available(self):
        """Check if facial detection is available"""
        return (self.enabled and 
                config.is_submodule_available() and 
                self._models_loaded)
    
    def get_face_boxes(self, image: np.ndarray, conf_threshold: float = 0.7) -> Tuple[np.ndarray, List]:
        """Detect faces in image and return face boxes"""
        if not self.is_available():
            return image, []
        
        try:
            image = image.copy()
            image_height = image.shape[0]
            image_width = image.shape[1]
            
            blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], True, False)
            self.face_net.setInput(blob)
            detections = self.face_net.forward()
            
            face_boxes = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > conf_threshold:
                    x1 = int(detections[0, 0, i, 3] * image_width)
                    y1 = int(detections[0, 0, i, 4] * image_height)
                    x2 = int(detections[0, 0, i, 5] * image_width)
                    y2 = int(detections[0, 0, i, 6] * image_height)
                    face_boxes.append([x1, y1, x2, y2])
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), int(round(image_height/150)), 8)
            
            return image, face_boxes
            
        except Exception as e:
            self.logger.error(f"Error in face detection: {e}")
            return image, []
    
    def analyze_image(self, image_path: str) -> Dict:
        """Analyze image for facial attributes, emotions, age, and gender"""
        if not self.is_available():
            return {
                'error': 'Facial detection not available',
                'enabled': self.enabled,
                'submodule_available': config.is_submodule_available()
            }
        
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {'error': 'Could not read image'}
            
            # Detect faces
            result_img, face_boxes = self.get_face_boxes(image)
            
            if not face_boxes:
                return {
                    'faces_detected': 0,
                    'message': 'No faces detected in image'
                }
            
            results = {
                'faces_detected': len(face_boxes),
                'timestamp': datetime.utcnow().isoformat(),
                'faces': []
            }
            
            # Process each detected face
            for idx, face_box in enumerate(face_boxes):
                face_result = {
                    'face_id': idx,
                    'bounding_box': face_box,
                    'confidence': 'high'  # Could extract actual confidence
                }
                
                config_facial = config.get_facial_detection_config()
                
                # Add basic detection info
                if config_facial.get('detect_emotions', True):
                    face_result['emotions'] = self._detect_emotions_placeholder(face_box)
                
                if config_facial.get('detect_age_gender', True):
                    face_result['age'] = self._detect_age_placeholder(face_box)
                    face_result['gender'] = self._detect_gender_placeholder(face_box)
                
                if config_facial.get('detect_attributes', True):
                    face_result['attributes'] = self._detect_attributes_placeholder(face_box)
                
                results['faces'].append(face_result)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error analyzing image: {e}")
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _detect_emotions_placeholder(self, face_box):
        """Placeholder for emotion detection"""
        # In a full implementation, this would use the emotion detection from the submodule
        emotions = ['happy', 'neutral', 'surprise', 'angry', 'fear', 'sad', 'disgust']
        # Return a mock emotion for demonstration
        return {
            'primary_emotion': 'neutral',
            'confidence': 0.85,
            'all_emotions': {emotion: 0.1 for emotion in emotions}
        }
    
    def _detect_age_placeholder(self, face_box):
        """Placeholder for age detection"""
        age_ranges = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        return {
            'age_range': '(25-32)',
            'confidence': 0.75
        }
    
    def _detect_gender_placeholder(self, face_box):
        """Placeholder for gender detection"""
        return {
            'gender': 'Female',
            'confidence': 0.82
        }
    
    def _detect_attributes_placeholder(self, face_box):
        """Placeholder for facial attributes detection"""
        sample_attributes = ['Smiling', 'Young', 'Attractive', 'No_Beard']
        return {
            'detected_attributes': sample_attributes,
            'total_attributes_checked': 40
        }
    
    def process_pulse_image(self, image_data: bytes) -> Dict:
        """Process image data for pulse submission"""
        if not self.is_available():
            return {'facial_detection_available': False}
        
        try:
            # Save image data to temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                tmp_file.write(image_data)
                tmp_path = tmp_file.name
            
            # Analyze the image
            result = self.analyze_image(tmp_path)
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            # Add integration metadata
            result['integration_info'] = {
                'feature_name': 'AIML Human Attributes Detection',
                'ai_signature': 'Euystacio-Helmi AI with weblineindia submodule',
                'processing_timestamp': datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing pulse image: {e}")
            return {'error': f'Image processing failed: {str(e)}'}

# Global facial detection instance
facial_detection = FacialDetectionIntegration()