"""
Euystacio Configuration System
Configuration management for optional features and integrations.
"""

import os
from pathlib import Path

class EuystacioConfig:
    """Configuration management for Euystacio features"""
    
    def __init__(self):
        # Default configuration
        self._config = {
            'facial_detection_enabled': False,
            'facial_detection_confidence_threshold': 0.7,
            'facial_detection_auto_mode': True,
            'facial_detection_attributes': True,
            'facial_detection_emotions': True,
            'facial_detection_age_gender': True
        }
        
        # Load from environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'EUYSTACIO_FACIAL_DETECTION_ENABLED': ('facial_detection_enabled', bool),
            'EUYSTACIO_FACIAL_DETECTION_CONFIDENCE': ('facial_detection_confidence_threshold', float),
            'EUYSTACIO_FACIAL_DETECTION_AUTO': ('facial_detection_auto_mode', bool),
            'EUYSTACIO_FACIAL_DETECTION_ATTRIBUTES': ('facial_detection_attributes', bool),
            'EUYSTACIO_FACIAL_DETECTION_EMOTIONS': ('facial_detection_emotions', bool),
            'EUYSTACIO_FACIAL_DETECTION_AGE_GENDER': ('facial_detection_age_gender', bool),
        }
        
        for env_var, (config_key, type_func) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    if type_func == bool:
                        self._config[config_key] = value.lower() in ('true', '1', 'yes', 'on')
                    else:
                        self._config[config_key] = type_func(value)
                except (ValueError, TypeError):
                    pass  # Keep default value if conversion fails
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self._config.get(key, default)
    
    def is_facial_detection_enabled(self):
        """Check if facial detection feature is enabled"""
        return self.get('facial_detection_enabled', False)
    
    def get_facial_detection_config(self):
        """Get facial detection configuration"""
        return {
            'enabled': self.get('facial_detection_enabled', False),
            'confidence_threshold': self.get('facial_detection_confidence_threshold', 0.7),
            'auto_mode': self.get('facial_detection_auto_mode', True),
            'detect_attributes': self.get('facial_detection_attributes', True),
            'detect_emotions': self.get('facial_detection_emotions', True),
            'detect_age_gender': self.get('facial_detection_age_gender', True),
        }
    
    def get_submodule_path(self):
        """Get path to facial detection submodule"""
        return Path(__file__).parent / 'external' / 'facial-detection'
    
    def is_submodule_available(self):
        """Check if facial detection submodule is available"""
        submodule_path = self.get_submodule_path()
        return (submodule_path.exists() and 
                (submodule_path / 'predict.py').exists() and
                (submodule_path / 'model').exists())

# Global configuration instance
config = EuystacioConfig()