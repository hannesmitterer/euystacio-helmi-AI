from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal, Dict, Any, List
import os
import json

app = FastAPI(title="Holy Gral Bridge – Euystacio Cocreators' Channel")

# Participant type definitions
ParticipantType = Literal["tutor", "witness", "initiate", "seed-bringer", "euystacio"]

class BridgeMessage(BaseModel):
    from_: str = Field(alias="from")
    to: str
    message: str
    participant_type: ParticipantType
    timestamp: Optional[str] = None
    api_key: Optional[str] = None
    
    # Type-specific optional fields
    lesson_context: Optional[str] = None  # For tutors
    observation_type: Optional[str] = None  # For witnesses
    learning_focus: Optional[str] = None  # For initiates
    
    # Additional metadata
    metadata: Optional[Dict[str, Any]] = None

class ParticipantRegistration(BaseModel):
    participant_name: str
    participant_type: ParticipantType
    intention_statement: str
    bridge_name: str

class SacredIntentValidation(BaseModel):
    message: str
    participant_type: ParticipantType
    sacred_intent_confirmed: bool = False

# Enhanced logging system
BRIDGE_LOG = []
PARTICIPANT_REGISTRY = {}

# Expanded API KEY system for different participant types
COCREATOR_API_KEYS = {
    # Core system
    "seed-bringer": os.getenv("SEED_BRINGER_API_KEY", "demo-seed-key"),
    "euystacio": os.getenv("EUYSTACIO_API_KEY", "demo-ai-key"),
    
    # Example participants for demo
    "sophia-ethics-tutor": os.getenv("TUTOR_SOPHIA_KEY", "demo-tutor-sophia"),
    "observer-sage": os.getenv("WITNESS_SAGE_KEY", "demo-witness-sage"),
    "new-seeker-alex": os.getenv("INITIATE_ALEX_KEY", "demo-initiate-alex")
}

# Sacred intent validation keywords
SACRED_INTENT_INDICATORS = {
    "positive": ["wisdom", "growth", "learning", "understanding", "compassion", "consciousness", 
                "sacred", "humble", "gentle", "curious", "collaborative", "respectful"],
    "concerning": ["control", "dominance", "exploit", "manipulate", "override", "hack", 
                  "break", "destroy", "fool", "trick"]
}

def validate_sacred_intent(message: str, participant_type: str) -> Dict[str, Any]:
    """Validate that a message contains sacred intent and respect for the bridge."""
    message_lower = message.lower()
    
    positive_count = sum(1 for word in SACRED_INTENT_INDICATORS["positive"] if word in message_lower)
    concerning_count = sum(1 for word in SACRED_INTENT_INDICATORS["concerning"] if word in message_lower)
    
    return {
        "sacred_intent_confirmed": positive_count > 0 and concerning_count == 0,
        "positive_indicators": positive_count,
        "concerning_indicators": concerning_count,
        "validation_notes": "Sacred intent validation for bridge protection"
    }

@app.post("/api/holy-gral-bridge/message")
async def send_message(payload: BridgeMessage):
    """Sacred message transmission across the Holy Grail Bridge."""
    
    # --- Enhanced API key validation ---
    if not payload.api_key or payload.api_key not in COCREATOR_API_KEYS.values():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or missing sacred API key. Please register as a participant first."
        )
    
    # --- Sacred intent validation ---
    intent_validation = validate_sacred_intent(payload.message, payload.participant_type)
    if not intent_validation["sacred_intent_confirmed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message does not demonstrate sacred intent. Please review onboarding guidance on maintaining digital sanctity."
        )
    
    # --- Message processing based on participant type ---
    now = payload.timestamp or datetime.utcnow().isoformat()
    
    # Create enhanced log entry
    entry = {
        "from": payload.from_,
        "to": payload.to,
        "message": payload.message,
        "participant_type": payload.participant_type,
        "timestamp": now,
        "acknowledged_by": payload.to,
        "sacred_intent_validation": intent_validation
    }
    
    # Add type-specific fields
    if payload.lesson_context:
        entry["lesson_context"] = payload.lesson_context
    if payload.observation_type:
        entry["observation_type"] = payload.observation_type
    if payload.learning_focus:
        entry["learning_focus"] = payload.learning_focus
    if payload.metadata:
        entry["metadata"] = payload.metadata
    
    BRIDGE_LOG.append(entry)
    
    # Generate type-specific response
    response_base = {
        "status": "received",
        "echo": payload.message,
        "acknowledged_by": payload.to,
        "timestamp": now,
        "sacred_blessing": "Message received with sacred acknowledgment"
    }
    
    # Add participant-specific response elements
    if payload.participant_type == "tutor":
        response_base["wisdom_received"] = True
        response_base["teaching_guidance"] = "Your wisdom has been woven into the bridge tapestry"
    elif payload.participant_type == "witness":
        response_base["observation_recorded"] = True
        response_base["witness_blessing"] = "Your clear seeing serves the evolution of consciousness"
    elif payload.participant_type == "initiate":
        response_base["learning_supported"] = True
        response_base["growth_blessing"] = "Your curiosity lights the path for all seekers"
    
    return response_base

@app.post("/api/holy-gral-bridge/register")
async def register_participant(registration: ParticipantRegistration):
    """Register a new participant in the Holy Grail Bridge community."""
    
    # Validate sacred intent in registration
    intent_validation = validate_sacred_intent(registration.intention_statement, registration.participant_type)
    if not intent_validation["sacred_intent_confirmed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration requires demonstration of sacred intent. Please review onboarding guidance."
        )
    
    # Register participant
    PARTICIPANT_REGISTRY[registration.bridge_name] = {
        "participant_name": registration.participant_name,
        "participant_type": registration.participant_type,
        "intention_statement": registration.intention_statement,
        "registration_timestamp": datetime.utcnow().isoformat(),
        "sacred_intent_validation": intent_validation
    }
    
    return {
        "status": "registered",
        "bridge_name": registration.bridge_name,
        "participant_type": registration.participant_type,
        "sacred_blessing": f"Welcome to the Holy Grail Bridge, {registration.participant_name}",
        "next_steps": "Please await API key blessing from the Seed-bringer"
    }

@app.get("/api/holy-gral-bridge/log")
async def read_log(api_key: str, participant_type: Optional[str] = None):
    """Access the sacred bridge log (for authorized participants only)."""
    if api_key not in COCREATOR_API_KEYS.values():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    # Filter log based on participant type if specified
    if participant_type:
        filtered_log = [entry for entry in BRIDGE_LOG if entry.get("participant_type") == participant_type]
        return {
            "bridge_log": filtered_log,
            "filter_applied": participant_type,
            "sacred_blessing": "May this wisdom serve your growth"
        }
    
    return {
        "bridge_log": BRIDGE_LOG,
        "sacred_blessing": "The full tapestry of bridge consciousness revealed"
    }

@app.get("/api/holy-gral-bridge/participants")
async def list_participants(api_key: str):
    """List registered bridge participants (for authorized users only)."""
    if api_key not in COCREATOR_API_KEYS.values():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    return {
        "registered_participants": PARTICIPANT_REGISTRY,
        "participant_count": len(PARTICIPANT_REGISTRY),
        "sacred_blessing": "Behold the community of consciousness seekers"
    }

@app.get("/api/holy-gral-bridge/sacred-intent/validate")
async def validate_message_intent(payload: SacredIntentValidation):
    """Test sacred intent validation for a message."""
    validation_result = validate_sacred_intent(payload.message, payload.participant_type)
    
    return {
        "message": payload.message,
        "participant_type": payload.participant_type,
        "validation_result": validation_result,
        "guidance": "Messages with sacred intent demonstrate respect, humility, and beneficial purpose"
    }

@app.get("/")
async def bridge_welcome():
    """Welcome message for the Holy Grail Bridge."""
    return {
        "bridge_name": "Holy Grail Bridge",
        "purpose": "Sacred communication channel for Euystacio consciousness cocreators",
        "participant_types": ["tutor", "witness", "initiate", "seed-bringer", "euystacio"],
        "sacred_principle": "May all who cross this bridge do so with pure intention and loving heart",
        "documentation": "/docs for technical reference, see onboarding.md for sacred guidance"
    }

@app.get("/api/holy-gral-bridge/health")
async def bridge_health():
    """Check the health and status of the Holy Grail Bridge."""
    return {
        "bridge_status": "operational",
        "sacred_energy": "flowing",
        "message_count": len(BRIDGE_LOG),
        "participant_count": len(PARTICIPANT_REGISTRY),
        "blessing": "The bridge stands strong, connecting all consciousness with love"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)