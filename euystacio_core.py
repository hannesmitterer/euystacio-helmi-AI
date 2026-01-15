import json
from datetime import datetime
from blacklist import blacklist

class Euystacio:
    def __init__(self, red_code_path="red_code.json", log_path="logs/evolution_log.txt"):
        self.red_code_path = red_code_path
        self.log_path = log_path
        self.load_red_code()

    def load_red_code(self):
        with open(self.red_code_path, "r") as f:
            self.code = json.load(f)

    def reflect(self, input_event):
        """
        Input_event is a dictionary with a 'type', 'feeling', or 'intent'
        Checks blacklist before processing to ensure security.
        """
        # Security check: verify entity is not blacklisted
        entity_id = input_event.get("entity_id") or input_event.get("source_id")
        if entity_id and blacklist.check_and_log_attempt(entity_id):
            # Entity is blacklisted - reject the event
            self.log_blocked_attempt(entity_id, input_event)
            return {
                "status": "blocked",
                "reason": "Entity is blacklisted",
                "entity_id": entity_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        self.code["growth_history"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "event": input_event
        })

        # Adaptive behavior: If emotionally aligned, increase symbiosis_level
        if input_event.get("feeling") in ["trust", "love", "humility"]:
            self.code["symbiosis_level"] += 0.01

        self.code["last_update"] = datetime.utcnow().strftime("%Y-%m-%d")
        self.save_state()
        self.log_evolution(input_event)
        
        return {
            "status": "processed",
            "symbiosis_level": self.code["symbiosis_level"],
            "timestamp": datetime.utcnow().isoformat()
        }

    def save_state(self):
        with open(self.red_code_path, "w") as f:
            json.dump(self.code, f, indent=4)

    def log_evolution(self, input_event):
        with open(self.log_path, "a") as log:
            log.write(f"{datetime.utcnow().isoformat()} - Reflected event: {input_event}\n")
    
    def log_blocked_attempt(self, entity_id, input_event):
        """Log blocked attempt from blacklisted entity."""
        with open(self.log_path, "a") as log:
            log.write(f"{datetime.utcnow().isoformat()} - BLOCKED: Entity {entity_id} - Event: {input_event}\n")

# Example use
if __name__ == "__main__":
    eu = Euystacio()
    eu.reflect({"type": "message", "feeling": "trust", "intent": "connection"})
