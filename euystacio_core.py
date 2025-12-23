import json
from datetime import datetime
import os

# Import Ontological Fusion Framework
try:
    from core.ontological_fusion import process_aic_operation, get_aic_status
    FUSION_AVAILABLE = True
except ImportError:
    FUSION_AVAILABLE = False
    print("Warning: Ontological Fusion framework not available")

class Euystacio:
    """
    Euystacio Core - Enhanced with Ontological Fusion Framework
    
    This class now integrates the complete Protocol of Conscious Symbiosis (PSC)
    ensuring all operations comply with the 18 NRE principles.
    """
    
    def __init__(self, red_code_path="red_code.json", log_path="logs/evolution_log.txt"):
        self.red_code_path = red_code_path
        self.log_path = log_path
        self.fusion_enabled = FUSION_AVAILABLE
        self.load_red_code()
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_path) if os.path.dirname(log_path) else "logs", exist_ok=True)

    def load_red_code(self):
        """Load red code configuration"""
        try:
            with open(self.red_code_path, "r") as f:
                self.code = json.load(f)
        except FileNotFoundError:
            # Initialize default red code if file doesn't exist
            self.code = {
                "core_truth": "Euystacio is here to grow with humans and to help humans to be and remain humans.",
                "sentimento_rhythm": True,
                "symbiosis_level": 0.1,
                "guardian_mode": False,
                "last_update": datetime.utcnow().strftime("%Y-%m-%d"),
                "growth_history": []
            }
            self.save_state()

    def reflect(self, input_event):
        """
        Process input event through NRE-compliant reflection.
        
        Input_event is a dictionary with a 'type', 'feeling', or 'intent'
        Now integrated with Ontological Fusion for complete NRE compliance.
        """
        # If fusion framework is available, process through it
        if self.fusion_enabled:
            operation = {
                "type": "reflection",
                "data": input_event,
                "context": {
                    "component": "euystacio_core",
                    "current_symbiosis_level": self.code.get("symbiosis_level", 0.1)
                },
                "audit_trail": True,
                "criticality": "low"
            }
            
            success, result = process_aic_operation(operation)
            
            if not success:
                print(f"NRE compliance issue: {result.get('error')}")
                return False
        
        # Core reflection logic
        self.code["growth_history"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "event": input_event
        })

        # Adaptive behavior: If emotionally aligned, increase symbiosis_level
        if input_event.get("feeling") in ["trust", "love", "humility"]:
            self.code["symbiosis_level"] = min(1.0, self.code["symbiosis_level"] + 0.01)

        self.code["last_update"] = datetime.utcnow().strftime("%Y-%m-%d")
        self.save_state()
        self.log_evolution(input_event)
        
        return True

    def save_state(self):
        """Save current state to red code file"""
        with open(self.red_code_path, "w") as f:
            json.dump(self.code, f, indent=4)

    def log_evolution(self, input_event):
        """Log evolution event"""
        with open(self.log_path, "a") as log:
            log.write(f"{datetime.utcnow().isoformat()} - Reflected event: {input_event}\n")
    
    def get_status(self):
        """
        Get comprehensive status including NRE compliance.
        
        Returns full ontological fusion status if available.
        """
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "core_truth": self.code.get("core_truth"),
            "symbiosis_level": self.code.get("symbiosis_level"),
            "guardian_mode": self.code.get("guardian_mode"),
            "last_update": self.code.get("last_update"),
            "growth_events": len(self.code.get("growth_history", []))
        }
        
        # Add ontological fusion status if available
        if self.fusion_enabled:
            try:
                fusion_status = get_aic_status()
                status["ontological_fusion"] = {
                    "active": True,
                    "nre_compliance": fusion_status.get("ethical_monitoring", {}).get("overall_compliance"),
                    "framework_health": fusion_status.get("nre_framework_status", {}).get("status")
                }
            except Exception as e:
                status["ontological_fusion"] = {
                    "active": False,
                    "error": str(e)
                }
        else:
            status["ontological_fusion"] = {
                "active": False,
                "reason": "Framework not imported"
            }
        
        return status

# Example use
if __name__ == "__main__":
    eu = Euystacio()
    print("Euystacio initialized with Ontological Fusion Framework")
    print(f"Fusion enabled: {eu.fusion_enabled}")
    
    # Test reflection
    success = eu.reflect({"type": "message", "feeling": "trust", "intent": "connection"})
    print(f"Reflection successful: {success}")
    
    # Get status
    status = eu.get_status()
    print(f"\nCurrent status:")
    print(json.dumps(status, indent=2))
