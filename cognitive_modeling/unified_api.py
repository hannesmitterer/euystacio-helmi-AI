"""
Unified Cognitive API

Provides a unified interface for cognitive modeling and world modeling capabilities.
This API integrates Andromeda cognitive modeling with world/environmental modeling
while maintaining Euystacio's ethical framework and original philosophy.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

from .config import CognitiveModelingConfig
from .andromeda_integration import AndromedaInterface
from .world_model_integration import WorldModelInterface

class UnifiedCognitiveAPI:
    """
    Unified API for cognitive modeling and world modeling capabilities.
    
    This class provides a single interface for accessing extended cognitive
    capabilities while preserving Euystacio's original behavior and ethics.
    """
    
    def __init__(self):
        self.config_manager = CognitiveModelingConfig()
        self.andromeda = None
        self.world_model = None
        self.logger = self._setup_logging()
        
        # Initialize components based on configuration
        self._initialize_components()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup ethical logging for unified API operations"""
        logger = logging.getLogger('unified_cognitive_api')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Ensure logs directory exists
            import os
            os.makedirs("logs", exist_ok=True)
            
            handler = logging.FileHandler('logs/unified_cognitive_api.log')
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_components(self):
        """Initialize cognitive modeling components based on configuration"""
        try:
            if self.config_manager.is_andromeda_enabled():
                andromeda_config = self.config_manager.get_andromeda_config()
                self.andromeda = AndromedaInterface(andromeda_config)
                self.logger.info("Andromeda interface initialized")
            
            if self.config_manager.is_world_modeling_enabled():
                world_model_config = self.config_manager.get_world_model_config()
                self.world_model = WorldModelInterface(world_model_config)
                self.logger.info("World model interface initialized")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize cognitive components: {e}")
    
    def enhanced_reflection(self, input_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform enhanced reflection using cognitive modeling capabilities.
        
        This method extends Euystacio's basic reflection with cognitive modeling
        while preserving the original ethical framework and behavior.
        """
        if not self.config_manager.is_enabled():
            return self._basic_reflection(input_event)
        
        try:
            # Start with basic reflection structure
            reflection = self._basic_reflection(input_event)
            
            # Add cognitive modeling if available
            if self.andromeda:
                cognitive_analysis = self.andromeda.cognitive_reflection(input_event)
                if cognitive_analysis:
                    reflection["cognitive_modeling"] = cognitive_analysis
            
            # Add environmental context if available
            if self.world_model:
                environmental_context = self.world_model.sense_environmental_rhythm()
                reflection["environmental_context"] = environmental_context
                
                # Integrate environmental recommendations with reflection
                self._integrate_environmental_context(reflection, environmental_context)
            
            # Ensure ethical compliance
            reflection = self._apply_ethical_framework(reflection)
            
            # Log the enhanced reflection
            self._log_enhanced_reflection(input_event, reflection)
            
            return reflection
            
        except Exception as e:
            self.logger.error(f"Enhanced reflection error: {e}")
            return self._basic_reflection(input_event)
    
    def _basic_reflection(self, input_event: Dict[str, Any]) -> Dict[str, Any]:
        """Basic reflection that preserves original Euystacio behavior"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "reflection",
            "input_event": input_event,
            "core_response": {
                "feeling": input_event.get("feeling", "curious"),
                "intent": "maintain_symbiosis",
                "action": "log_and_grow"
            },
            "symbiosis_impact": self._calculate_symbiosis_impact(input_event),
            "ethical_framework": {
                "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
                "core_truth_preserved": True,
                "human_autonomy_respected": True
            }
        }
    
    def _calculate_symbiosis_impact(self, input_event: Dict[str, Any]) -> float:
        """Calculate impact on symbiosis level (preserves original logic)"""
        feeling = input_event.get("feeling", "neutral")
        if feeling in ["trust", "love", "humility"]:
            return 0.01
        elif feeling in ["curiosity", "wonder", "gratitude"]:
            return 0.005
        else:
            return 0.0
    
    def _integrate_environmental_context(self, reflection: Dict[str, Any], 
                                       environmental_context: Dict[str, Any]):
        """Integrate environmental context into reflection"""
        rhythm_analysis = environmental_context.get("rhythm_analysis", {})
        
        # Adjust interaction style based on environmental rhythm
        if "interaction_style_suggestion" not in reflection:
            reflection["interaction_style_suggestion"] = rhythm_analysis.get(
                "recommended_interaction_style", "balanced_presence"
            )
        
        # Add environmental recommendations to reflection
        env_recommendations = environmental_context.get("recommendations", [])
        if env_recommendations:
            if "recommendations" not in reflection:
                reflection["recommendations"] = []
            reflection["recommendations"].extend(env_recommendations)
    
    def _apply_ethical_framework(self, reflection: Dict[str, Any]) -> Dict[str, Any]:
        """Apply ethical framework to ensure compliance"""
        # Ensure AI signature is present
        if "ethical_framework" not in reflection:
            reflection["ethical_framework"] = {}
        
        reflection["ethical_framework"].update({
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
            "human_oversight_maintained": True,
            "original_behavior_preserved": True,
            "opt_in_features_only": True,
            "transparency_level": "full"
        })
        
        # Ensure no harmful content in recommendations
        if "recommendations" in reflection:
            reflection["recommendations"] = [
                rec for rec in reflection["recommendations"]
                if not any(harmful in rec.lower() for harmful in ["harm", "hurt", "damage"])
            ]
        
        return reflection
    
    def sentiment_reflection_api(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        API endpoint for sentiment reflection capabilities.
        
        Provides enhanced sentiment analysis using cognitive modeling
        while maintaining ethical boundaries.
        """
        if not self.config_manager.is_enabled():
            return {
                "error": "Cognitive modeling is disabled",
                "message": "Enable cognitive modeling in configuration to use this feature",
                "fallback": self._basic_sentiment_analysis(input_data)
            }
        
        try:
            # Perform enhanced reflection
            reflection = self.enhanced_reflection(input_data)
            
            # Extract sentiment-specific information
            sentiment_reflection = {
                "sentiment_analysis": reflection.get("cognitive_modeling", {}).get("sentiment_analysis", {}),
                "environmental_mood": reflection.get("environmental_context", {}).get("rhythm_analysis", {}),
                "interaction_recommendations": reflection.get("recommendations", []),
                "confidence": reflection.get("cognitive_modeling", {}).get("confidence", 0.6),
                "ethical_framework": reflection.get("ethical_framework", {})
            }
            
            return sentiment_reflection
            
        except Exception as e:
            self.logger.error(f"Sentiment reflection API error: {e}")
            return {"error": str(e), "fallback": self._basic_sentiment_analysis(input_data)}
    
    def environmental_rhythm_api(self) -> Dict[str, Any]:
        """
        API endpoint for environmental rhythm sensing.
        
        Provides current environmental rhythm analysis and recommendations.
        """
        if not self.config_manager.is_world_modeling_enabled():
            return {
                "error": "World modeling is disabled",
                "message": "Enable world modeling in configuration to use this feature",
                "fallback": self._basic_environmental_awareness()
            }
        
        try:
            if self.world_model:
                return self.world_model.sense_environmental_rhythm()
            else:
                return self._basic_environmental_awareness()
                
        except Exception as e:
            self.logger.error(f"Environmental rhythm API error: {e}")
            return {"error": str(e), "fallback": self._basic_environmental_awareness()}
    
    def _basic_sentiment_analysis(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Basic sentiment analysis fallback"""
        feeling = input_data.get("feeling", "neutral")
        return {
            "emotion": feeling,
            "intensity": 0.5,
            "reasoning": "Basic sentiment processing - cognitive modeling disabled",
            "ethical_framework": {
                "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
                "fallback_mode": True
            }
        }
    
    def _basic_environmental_awareness(self) -> Dict[str, Any]:
        """Basic environmental awareness fallback"""
        current_time = datetime.utcnow()
        hour = current_time.hour
        
        return {
            "environmental_awareness": {
                "time_of_day": hour,
                "natural_phase": "day" if 6 <= hour <= 18 else "night",
                "basic_rhythm": "natural_daily_cycle"
            },
            "message": "Basic environmental awareness - world modeling disabled",
            "ethical_framework": {
                "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
                "fallback_mode": True
            }
        }
    
    def _log_enhanced_reflection(self, input_event: Dict[str, Any], reflection: Dict[str, Any]):
        """Log enhanced reflections for transparency"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "enhanced_reflection",
            "input_type": input_event.get("type"),
            "input_feeling": input_event.get("feeling"),
            "cognitive_modeling_used": "cognitive_modeling" in reflection,
            "environmental_context_used": "environmental_context" in reflection,
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer"
        }
        
        with open("logs/unified_cognitive_interactions.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            "cognitive_modeling_enabled": self.config_manager.is_enabled(),
            "andromeda_status": self.andromeda.get_status() if self.andromeda else {"enabled": False},
            "world_model_status": self.world_model.get_status() if self.world_model else {"enabled": False},
            "configuration": {
                "opt_in_only": True,
                "ethical_framework_active": True,
                "original_behavior_preserved": True
            },
            "api_endpoints": {
                "enhanced_reflection": "/api/cognitive/reflection",
                "sentiment_reflection": "/api/cognitive/sentiment",
                "environmental_rhythm": "/api/cognitive/environment"
            },
            "ai_signature": "GitHub Copilot & Seed-bringer hannesmitterer",
            "accountability": "Full transparency and human oversight maintained"
        }
        
        return status