from pydantic import BaseModel, Field
from typing import List, Dict, Any

# Data Model for an Individual Agent's Report
class AgentOutput(BaseModel):
    agent_id: str = Field(..., description="Unique ID of the Collective agent.")
    trust_index: float = Field(..., description="Calculated fidelity/trust score (0.0 to 1.0).")
    status: str = Field(..., description="The agent's operational status ('VALID', 'INVALID', 'ERROR').")
    resolution: str = Field(..., description="The agent's proposed action or path/answer.")
    raw_data: Dict[str, Any] = Field(default_factory=dict, description="Optional raw data for diagnostics.")

# Data Model for Human/Control Panel Input
class InputEnvelope(BaseModel):
    request_id: str = Field(..., description="Unique ID for the human-initiated request.")
    user_intent: str = Field(..., description="The natural language command from the operator.")
    sentimento_score: float = Field(default=0.0, description="The operator's emotional/alignment score (if applicable).")
    
    def is_valid_user_intent(self) -> bool:
        """Placeholder for initial validation logic (e.g., Red Code/Consent check)."""
        # For this integration, we will assume a simple check.
        return True 

# Data Model for the Final Output from Euystacio Gateway
class OutputEnvelope(BaseModel):
    status: str = Field(..., description="The overall system status ('REJECTED', 'CRITICAL_HALT', 'CONSUS_ACHIEVED', 'LOW_CONFIDENCE_WARNING').")
    message: str = Field(..., description="A short summary message for the operator.")
    data: Dict[str, Any] = Field(default_factory=dict, description="The aggregated metrics and final resolution.")
    
    # New Fields for the Control Panel Dashboard (Contained within 'data' dictionary in the final commit)
    # The integration code directly places the output fields into the 'data' dictionary:
    # 'collective_resolution', 'collective_trust_level', 'axiomatic_alignment', 'initial_request_id'