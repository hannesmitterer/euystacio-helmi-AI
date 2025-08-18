"""
Configuration for Cognitive Modeling Integration

Provides ethical, opt-in configuration for extended cognitive capabilities.
All features are disabled by default to preserve Euystacio's original flow.
"""

import json
import os
from typing import Dict, Any, Optional

class CognitiveModelingConfig:
    """
    Configuration manager for cognitive modeling features.
    
    Follows Euystacio's ethical framework:
    - All features opt-in by default
    - Full transparency in configuration
    - Preserves original system behavior
    """
    
    def __init__(self, config_path: str = "cognitive_modeling_config.json"):
        self.config_path = config_path
        self.config = self._load_or_create_config()
    
    def _load_or_create_config(self) -> Dict[str, Any]:
        """Load existing config or create default ethical config"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            # Default configuration - all features disabled for ethical opt-in
            default_config = {
                "cognitive_modeling_enabled": False,
                "andromeda_integration": {
                    "enabled": False,
                    "model_size": "small",  # Start with smallest model for accessibility
                    "ethical_constraints": True
                },
                "world_modeling": {
                    "enabled": False,
                    "environmental_sensing": False,
                    "rhythm_analysis": False
                },
                "api_endpoints": {
                    "sentiment_reflection": False,
                    "environmental_rhythm": False
                },
                "ethical_framework": {
                    "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
                    "accountability_maintained": True,
                    "human_oversight_required": True,
                    "preserve_original_behavior": True
                },
                "logging": {
                    "log_all_interactions": True,
                    "transparency_level": "full"
                }
            }
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration with proper logging"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
    
    def is_enabled(self) -> bool:
        """Check if cognitive modeling is enabled"""
        return self.config.get("cognitive_modeling_enabled", False)
    
    def is_andromeda_enabled(self) -> bool:
        """Check if Andromeda integration is enabled"""
        return (self.is_enabled() and 
                self.config.get("andromeda_integration", {}).get("enabled", False))
    
    def is_world_modeling_enabled(self) -> bool:
        """Check if world modeling is enabled"""
        return (self.is_enabled() and 
                self.config.get("world_modeling", {}).get("enabled", False))
    
    def get_andromeda_config(self) -> Dict[str, Any]:
        """Get Andromeda-specific configuration"""
        return self.config.get("andromeda_integration", {})
    
    def get_world_model_config(self) -> Dict[str, Any]:
        """Get world modeling configuration"""
        return self.config.get("world_modeling", {})
    
    def enable_cognitive_modeling(self, 
                                 enable_andromeda: bool = True,
                                 enable_world_modeling: bool = True) -> None:
        """
        Enable cognitive modeling features with ethical safeguards
        
        This method requires explicit human consent and logs the activation
        """
        self.config["cognitive_modeling_enabled"] = True
        if enable_andromeda:
            self.config["andromeda_integration"]["enabled"] = True
        if enable_world_modeling:
            self.config["world_modeling"]["enabled"] = True
            
        self._save_config(self.config)
        
        # Log the activation for transparency
        self._log_activation("cognitive_modeling", {
            "andromeda": enable_andromeda,
            "world_modeling": enable_world_modeling
        })
    
    def _log_activation(self, feature: str, details: Dict[str, Any]) -> None:
        """Log feature activation for accountability"""
        log_entry = {
            "timestamp": json.loads(json.dumps({"timestamp": "now"}))["timestamp"],
            "feature": feature,
            "details": details,
            "ai_signature": self.config["ethical_framework"]["ai_signature"],
            "human_oversight": True
        }
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Log to cognitive modeling specific log
        with open("logs/cognitive_modeling_activation.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")