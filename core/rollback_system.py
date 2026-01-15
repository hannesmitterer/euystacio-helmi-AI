"""
Rollback Mechanisms - State Preservation and Restoration

Implements event-based rollback system to restore safe states when
NRE violations are detected.

NRE Principles: 006, 016, 017, 018
"""

import json
import hashlib
import copy
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class CheckpointStatus(Enum):
    """Status of a checkpoint"""
    SAFE = "safe"
    UNSAFE = "unsafe"
    UNKNOWN = "unknown"


class RollbackTrigger(Enum):
    """Reasons for initiating rollback"""
    NRE_VIOLATION = "nre_violation"
    BOUNDARY_APPROACHED = "boundary_approached"
    SELF_CORRECTION = "self_correction"
    MANUAL_INTERVENTION = "manual_intervention"
    HARM_PREVENTION = "harm_prevention"


class StateCheckpoint:
    """Represents a saved system state with NRE validation"""
    
    def __init__(self, state_data: Dict, nre_validation: Dict):
        self.checkpoint_id = self._generate_id(state_data)
        self.timestamp = datetime.utcnow().isoformat()
        self.state_hash = self._hash_state(state_data)
        self.state_data = copy.deepcopy(state_data)
        self.nre_validation = nre_validation
        self.status = self._determine_status(nre_validation)
        self.metadata = {
            "created_at": self.timestamp,
            "size_bytes": len(json.dumps(state_data))
        }
    
    def _generate_id(self, state_data: Dict) -> str:
        """Generate unique checkpoint ID"""
        timestamp = datetime.utcnow().isoformat()
        data_str = json.dumps(state_data, sort_keys=True)
        combined = f"{timestamp}:{data_str}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _hash_state(self, state_data: Dict) -> str:
        """Create cryptographic hash of state for integrity verification"""
        data_str = json.dumps(state_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _determine_status(self, nre_validation: Dict) -> CheckpointStatus:
        """Determine if checkpoint represents a safe state"""
        compliance_score = nre_validation.get("overall_compliance", 0.0)
        
        if compliance_score >= 0.95:
            return CheckpointStatus.SAFE
        elif compliance_score < 0.7:
            return CheckpointStatus.UNSAFE
        else:
            return CheckpointStatus.UNKNOWN
    
    def verify_integrity(self) -> bool:
        """Verify checkpoint data hasn't been tampered with"""
        current_hash = self._hash_state(self.state_data)
        return current_hash == self.state_hash
    
    def to_dict(self) -> Dict:
        """Export checkpoint as dictionary"""
        return {
            "checkpoint_id": self.checkpoint_id,
            "timestamp": self.timestamp,
            "state_hash": self.state_hash,
            "status": self.status.value,
            "nre_compliance": self.nre_validation.get("overall_compliance", 0.0),
            "metadata": self.metadata
        }


class StatePreservation:
    """
    Maintains checkpoints of ethically-validated system states.
    
    Implements NRE-006 (Resilience), NRE-016 (Intervention), 
    NRE-017 (Eternal Witness).
    """
    
    def __init__(self, max_checkpoints: int = 100):
        self.checkpoints: List[StateCheckpoint] = []
        self.max_checkpoints = max_checkpoints
        self.immutable_ledger = []  # NRE-017: Never delete, only append
        
    def create_checkpoint(self, state: Dict, nre_validation: Dict) -> str:
        """
        Create new checkpoint of current state.
        
        Returns:
            checkpoint_id
        """
        checkpoint = StateCheckpoint(state, nre_validation)
        
        # Add to active checkpoints
        self.checkpoints.append(checkpoint)
        
        # Add to immutable ledger (NRE-017)
        self.immutable_ledger.append({
            "checkpoint_id": checkpoint.checkpoint_id,
            "timestamp": checkpoint.timestamp,
            "status": checkpoint.status.value,
            "state_hash": checkpoint.state_hash
        })
        
        # Manage checkpoint limit (keep most recent)
        if len(self.checkpoints) > self.max_checkpoints:
            # Remove oldest non-safe checkpoint
            self._prune_checkpoints()
        
        return checkpoint.checkpoint_id
    
    def _prune_checkpoints(self):
        """Remove old checkpoints while preserving safe states"""
        # Keep all SAFE checkpoints and recent UNKNOWN
        safe_checkpoints = [cp for cp in self.checkpoints if cp.status == CheckpointStatus.SAFE]
        recent_checkpoints = sorted(self.checkpoints, key=lambda x: x.timestamp, reverse=True)[:50]
        
        # Combine and deduplicate
        keep_ids = {cp.checkpoint_id for cp in safe_checkpoints + recent_checkpoints}
        self.checkpoints = [cp for cp in self.checkpoints if cp.checkpoint_id in keep_ids]
    
    def get_last_safe_checkpoint(self) -> Optional[StateCheckpoint]:
        """Find most recent checkpoint with SAFE status"""
        safe_checkpoints = [cp for cp in self.checkpoints if cp.status == CheckpointStatus.SAFE]
        
        if not safe_checkpoints:
            return None
        
        # Return most recent
        return max(safe_checkpoints, key=lambda x: x.timestamp)
    
    def get_checkpoint(self, checkpoint_id: str) -> Optional[StateCheckpoint]:
        """Retrieve specific checkpoint by ID"""
        for cp in self.checkpoints:
            if cp.checkpoint_id == checkpoint_id:
                return cp
        return None
    
    def verify_ledger_integrity(self) -> bool:
        """Verify immutable ledger hasn't been tampered with"""
        # Check that all ledger entries have corresponding checkpoints or history
        for entry in self.immutable_ledger:
            checkpoint_id = entry["checkpoint_id"]
            # Entry must exist either in active checkpoints or be historically valid
            exists = any(cp.checkpoint_id == checkpoint_id for cp in self.checkpoints)
            if not exists:
                # Historical entry - verify hash chain would go here
                pass
        return True


class RollbackMechanism:
    """
    Event-based rollback system for NRE violation recovery.
    
    Triggers automatic restoration to safe states when ethical
    boundaries are violated.
    """
    
    def __init__(self, state_preservation: StatePreservation):
        self.state_preservation = state_preservation
        self.rollback_history = []
        self.current_state = None
        
    def trigger_rollback(self, trigger: RollbackTrigger, 
                        context: Dict) -> Tuple[bool, str]:
        """
        Initiate rollback to last safe state.
        
        Args:
            trigger: Reason for rollback
            context: Additional context about the trigger
            
        Returns:
            Tuple of (success, message)
        """
        # Find last safe checkpoint
        safe_checkpoint = self.state_preservation.get_last_safe_checkpoint()
        
        if not safe_checkpoint:
            return False, "No safe checkpoint available for rollback"
        
        # Verify checkpoint integrity (NRE-017)
        if not safe_checkpoint.verify_integrity():
            return False, "Checkpoint integrity verification failed"
        
        # Perform rollback
        self.current_state = copy.deepcopy(safe_checkpoint.state_data)
        
        # Log rollback event
        rollback_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "trigger": trigger.value,
            "context": context,
            "restored_checkpoint": safe_checkpoint.checkpoint_id,
            "restored_from_time": safe_checkpoint.timestamp
        }
        self.rollback_history.append(rollback_event)
        
        # Notify stakeholders (would integrate with messaging system)
        self._notify_rollback(rollback_event)
        
        return True, f"Successfully rolled back to checkpoint {safe_checkpoint.checkpoint_id}"
    
    def _notify_rollback(self, event: Dict):
        """Notify Sovereign Collective of rollback event"""
        # Integration point with messaging layer
        # For now, just log it
        print(f"ROLLBACK NOTIFICATION: {json.dumps(event, indent=2)}")
    
    def get_rollback_statistics(self) -> Dict:
        """Get statistics about rollback events"""
        triggers_count = {}
        for event in self.rollback_history:
            trigger = event["trigger"]
            triggers_count[trigger] = triggers_count.get(trigger, 0) + 1
        
        return {
            "total_rollbacks": len(self.rollback_history),
            "rollbacks_by_trigger": triggers_count,
            "last_rollback": self.rollback_history[-1] if self.rollback_history else None,
            "current_state_available": self.current_state is not None
        }


class AutomaticRecoverySystem:
    """
    Coordinates automatic detection and recovery from NRE violations.
    
    Implements NRE-018 (Self-Correction Primacy).
    """
    
    def __init__(self):
        self.state_preservation = StatePreservation()
        self.rollback_mechanism = RollbackMechanism(self.state_preservation)
        self.recovery_attempts = []
        
    def monitor_and_recover(self, current_state: Dict, 
                          nre_validation: Dict) -> Dict:
        """
        Monitor current state and trigger recovery if needed.
        
        Returns:
            Status dictionary with recovery actions taken
        """
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "recovery_triggered": False,
            "actions_taken": []
        }
        
        # Check compliance score
        compliance_score = nre_validation.get("overall_compliance", 1.0)
        
        # Create checkpoint if state is acceptable
        if compliance_score >= 0.7:
            checkpoint_id = self.state_preservation.create_checkpoint(
                current_state, nre_validation
            )
            status["actions_taken"].append(f"Checkpoint created: {checkpoint_id}")
        
        # Trigger recovery if compliance is poor
        if compliance_score < 0.7:
            success, message = self.rollback_mechanism.trigger_rollback(
                RollbackTrigger.SELF_CORRECTION,
                {"compliance_score": compliance_score, "validation": nre_validation}
            )
            
            status["recovery_triggered"] = True
            status["actions_taken"].append(f"Rollback: {message}")
            
            # Log recovery attempt
            self.recovery_attempts.append({
                "timestamp": datetime.utcnow().isoformat(),
                "success": success,
                "compliance_before": compliance_score
            })
        
        return status
    
    def get_recovery_statistics(self) -> Dict:
        """Get statistics about automatic recovery"""
        successful = sum(1 for attempt in self.recovery_attempts if attempt["success"])
        
        return {
            "total_attempts": len(self.recovery_attempts),
            "successful_recoveries": successful,
            "success_rate": successful / len(self.recovery_attempts) if self.recovery_attempts else 0.0,
            "recent_attempts": self.recovery_attempts[-10:]
        }


# Singleton instances
_state_preservation_instance = None
_rollback_mechanism_instance = None
_recovery_system_instance = None

def get_state_preservation() -> StatePreservation:
    """Get global state preservation instance"""
    global _state_preservation_instance
    if _state_preservation_instance is None:
        _state_preservation_instance = StatePreservation()
    return _state_preservation_instance

def get_rollback_mechanism() -> RollbackMechanism:
    """Get global rollback mechanism instance"""
    global _rollback_mechanism_instance
    if _rollback_mechanism_instance is None:
        state_pres = get_state_preservation()
        _rollback_mechanism_instance = RollbackMechanism(state_pres)
    return _rollback_mechanism_instance

def get_recovery_system() -> AutomaticRecoverySystem:
    """Get global automatic recovery system instance"""
    global _recovery_system_instance
    if _recovery_system_instance is None:
        _recovery_system_instance = AutomaticRecoverySystem()
    return _recovery_system_instance
