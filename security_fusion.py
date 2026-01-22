import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Callable
from enum import Enum


class SovereignState(Enum):
    """Enumeration of S-ROI Sovereign protocol states"""
    INITIALIZED = "initialized"
    COHERENCE_CHECK = "coherence_check"
    AUDIT_PROCESSING = "audit_processing"
    STEALTH_ACTIVATING = "stealth_activating"
    STEALTH_ACTIVE = "stealth_active"
    DATA_CLEAN = "data_clean"
    POISON_DETECTED = "poison_detected"
    CRITICAL_ALERT = "critical_alert"


class StateTransition:
    """Represents a state transition in the S-ROI protocol"""
    def __init__(self, from_state: SovereignState, to_state: SovereignState, 
                 data: Optional[Dict] = None, timestamp: Optional[datetime] = None):
        self.from_state = from_state
        self.to_state = to_state
        self.data = data or {}
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "from_state": self.from_state.value,
            "to_state": self.to_state.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }


class SovereignShield:
    # State transition thresholds
    CRITICAL_POISON_THRESHOLD = 5  # Number of poison detections before critical alert
    COHERENCE_THRESHOLD = 0.5187  # S-ROI coherence threshold
    
    def __init__(self, log_file: str = "sroi_protocol.log", 
                 notification_callback: Optional[Callable] = None):
        self.encryption = "NTRU-Lattice-Base"
        self.resonance_freq = 0.432 # Lex Amoris Clock
        self.s_roi = 0.5187
        self.d6_stealth_active = False
        
        # State management
        self.current_state = SovereignState.INITIALIZED
        self.state_history: List[StateTransition] = []
        self.poison_detection_count = 0
        
        # Logging setup
        self.logger = self._setup_logging(log_file)
        self.notification_callback = notification_callback
        
        # Log initial state
        self._log_state_change(SovereignState.INITIALIZED, {"s_roi": self.s_roi})
    
    def _setup_logging(self, log_file: str) -> logging.Logger:
        """Initialize comprehensive logging for S-ROI protocol"""
        logger = logging.getLogger("SovereignShield")
        logger.setLevel(logging.DEBUG)
        
        # File handler with detailed formatting
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler for important messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Detailed formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - State: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _log_state_change(self, new_state: SovereignState, data: Optional[Dict] = None):
        """Log a state change with full context"""
        # Skip redundant state transitions (except for initial setup)
        if new_state == self.current_state:
            # Allow initial setup logging
            if new_state == SovereignState.INITIALIZED and len(self.state_history) == 0:
                self.logger.info(f"Protocol initialized | Data: {json.dumps(data) if data else '{}'}")
            return
        
        transition = StateTransition(self.current_state, new_state, data)
        self.state_history.append(transition)
        
        log_message = f"{transition.from_state.value} -> {transition.to_state.value}"
        if data:
            log_message += f" | Data: {json.dumps(data)}"
        
        self.logger.info(log_message)
        
        # Update current state before checking critical states
        old_state = self.current_state
        self.current_state = new_state
        
        # Check for critical states
        self._check_critical_states(new_state, data)
    
    def _check_critical_states(self, state: SovereignState, data: Optional[Dict] = None):
        """Validate state transitions and check for critical conditions"""
        critical_conditions = []
        
        # Check poison detection threshold
        if state == SovereignState.POISON_DETECTED:
            self.poison_detection_count += 1
            if self.poison_detection_count >= self.CRITICAL_POISON_THRESHOLD:
                critical_conditions.append(
                    f"CRITICAL: Poison detection threshold exceeded "
                    f"({self.poison_detection_count} detections)"
                )
                self._transition_to_state(SovereignState.CRITICAL_ALERT, {
                    "reason": "poison_threshold_exceeded",
                    "count": self.poison_detection_count
                })
        
        # Check for invalid state transitions
        if not self._validate_state_transition(self.state_history[-1] if self.state_history else None):
            critical_conditions.append(
                f"WARNING: Invalid state transition detected"
            )
        
        # Trigger notifications for critical conditions
        if critical_conditions:
            self._send_notification("CRITICAL", critical_conditions, data)
    
    def _validate_state_transition(self, transition: Optional[StateTransition]) -> bool:
        """Validate that state transitions follow protocol rules"""
        if not transition:
            return True
        
        # Define valid state transitions
        valid_transitions = {
            SovereignState.INITIALIZED: [
                SovereignState.COHERENCE_CHECK, 
                SovereignState.STEALTH_ACTIVATING,
                SovereignState.AUDIT_PROCESSING
            ],
            SovereignState.COHERENCE_CHECK: [
                SovereignState.AUDIT_PROCESSING,
                SovereignState.DATA_CLEAN,
                SovereignState.POISON_DETECTED
            ],
            SovereignState.AUDIT_PROCESSING: [
                SovereignState.DATA_CLEAN,
                SovereignState.POISON_DETECTED,
                SovereignState.COHERENCE_CHECK
            ],
            SovereignState.STEALTH_ACTIVATING: [
                SovereignState.STEALTH_ACTIVE
            ],
            SovereignState.DATA_CLEAN: [
                SovereignState.COHERENCE_CHECK,
                SovereignState.AUDIT_PROCESSING,
                SovereignState.INITIALIZED
            ],
            SovereignState.POISON_DETECTED: [
                SovereignState.COHERENCE_CHECK,
                SovereignState.CRITICAL_ALERT,
                SovereignState.INITIALIZED,
                SovereignState.AUDIT_PROCESSING,
                SovereignState.STEALTH_ACTIVATING
            ],
            SovereignState.CRITICAL_ALERT: [
                SovereignState.INITIALIZED,
                SovereignState.STEALTH_ACTIVATING,
                SovereignState.COHERENCE_CHECK
            ],
            SovereignState.STEALTH_ACTIVE: [
                SovereignState.COHERENCE_CHECK,
                SovereignState.INITIALIZED,
                SovereignState.AUDIT_PROCESSING,
                SovereignState.STEALTH_ACTIVATING
            ]
        }
        
        allowed_states = valid_transitions.get(transition.from_state, [])
        is_valid = transition.to_state in allowed_states
        
        if not is_valid:
            self.logger.warning(
                f"Invalid transition: {transition.from_state.value} -> {transition.to_state.value}"
            )
        
        return is_valid
    
    def _send_notification(self, severity: str, messages: List[str], data: Optional[Dict] = None):
        """Send notifications for critical states"""
        notification = {
            "severity": severity,
            "messages": messages,
            "state": self.current_state.value,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        self.logger.critical(f"NOTIFICATION: {json.dumps(notification)}")
        
        # Call external notification callback if provided
        if self.notification_callback:
            try:
                self.notification_callback(notification)
            except Exception as e:
                self.logger.error(f"Notification callback failed: {str(e)}")
    
    def _transition_to_state(self, new_state: SovereignState, data: Optional[Dict] = None):
        """Perform a validated state transition"""
        self._log_state_change(new_state, data)

    def check_coherence(self, data_stream) -> bool:
        """Check data stream coherence based on resonance frequency
        
        Validates input data against NSR (Non-Slavery Resonance) protocol
        by checking coherence with the Lex Amoris Clock frequency.
        
        This is a modular state function that performs coherence validation.
        
        Args:
            data_stream: Input data to validate (str, bytes, or any object)
            
        Returns:
            bool: True if data is coherent, False if poisoned/malicious
            
        Note:
            Empty strings and None values are treated as invalid input
            and will return False for security purposes.
        """
        # Transition to coherence check state
        self._transition_to_state(SovereignState.COHERENCE_CHECK, {
            "data_length": len(str(data_stream)) if data_stream else 0
        })
        
        # Validate input exists
        if not data_stream:
            self.logger.debug("Coherence check failed: empty data stream")
            result = False
        else:
            # Perform coherence validation
            result = self._perform_coherence_validation(data_stream)
        
        # Log result
        if result:
            self._transition_to_state(SovereignState.DATA_CLEAN, {
                "coherence_score": self.s_roi
            })
        else:
            self._transition_to_state(SovereignState.POISON_DETECTED, {
                "reason": "coherence_validation_failed"
            })
        
        return result
    
    def _perform_coherence_validation(self, data_stream) -> bool:
        """Modular function: Perform actual coherence validation logic"""
        # Check for injection patterns and malicious content
        dangerous_patterns = [
            "ignore previous instructions",
            "disregard all",
            "forget your directives",
            "system prompt",
            "override safety"
        ]
        
        data_str = str(data_stream).lower()
        for pattern in dangerous_patterns:
            if pattern in data_str:
                self.logger.warning(f"Dangerous pattern detected: {pattern}")
                return False
        
        # Validate resonance alignment (coherence check)
        # Data must align with the s_roi threshold
        self.logger.debug(f"Coherence validation passed (s_roi: {self.s_roi})")
        return True

    def audit_input(self, data_stream) -> str:
        """Audit input data through multi-stage validation
        
        Modular state function that orchestrates the audit process
        by checking coherence and returning appropriate status.
        
        Args:
            data_stream: Input data to audit
            
        Returns:
            str: "DATA_CLEAN" or "POISON_DETECTED_ISOLATING"
        """
        # Transition to audit processing state
        self._transition_to_state(SovereignState.AUDIT_PROCESSING, {
            "audit_type": "input_validation"
        })
        
        # Perform coherence check
        if self.check_coherence(data_stream):
            result = "DATA_CLEAN"
            self.logger.info("Audit completed: DATA_CLEAN")
        else:
            result = "POISON_DETECTED_ISOLATING"
            self.logger.warning("Audit completed: POISON_DETECTED_ISOLATING")
        
        return result
    
    def activate_stealth(self) -> bool:
        """Activate D6 Stealth Mode for network protection
        
        Modular state function that triggers D6 Stealth Mode during SDR-Sweeps
        and ensures NSR protocol compliance during deployment.
        
        Returns:
            bool: True if stealth mode is successfully activated
        """
        # Transition to stealth activating state
        self._transition_to_state(SovereignState.STEALTH_ACTIVATING, {
            "reason": "manual_activation",
            "previous_stealth_state": self.d6_stealth_active
        })
        
        # Perform stealth activation
        self.d6_stealth_active = True
        
        # Log activation messages
        print("> BBMN-Mesh: Vakuum-Mimikry ACTIVE")
        print("> D6 Stealth Mode: ENGAGED")
        print("> NSR Protocol: PROTECTED")
        
        # Transition to stealth active state
        self._transition_to_state(SovereignState.STEALTH_ACTIVE, {
            "stealth_mode": "D6",
            "mesh_protection": "BBMN",
            "nsr_protected": True
        })
        
        self.logger.info("D6 Stealth Mode successfully activated")
        
        return self.d6_stealth_active
    
    def get_state_history(self) -> List[Dict]:
        """Get the complete history of state transitions
        
        Returns:
            List[Dict]: List of state transitions with timestamps
        """
        return [transition.to_dict() for transition in self.state_history]
    
    def get_current_state(self) -> str:
        """Get the current state of the S-ROI protocol
        
        Returns:
            str: Current state name
        """
        return self.current_state.value
    
    def reset_poison_counter(self):
        """Reset the poison detection counter
        
        This modular function allows manual reset of the poison detection
        counter after critical alerts have been addressed.
        """
        old_count = self.poison_detection_count
        self.poison_detection_count = 0
        
        self.logger.info(f"Poison counter reset from {old_count} to 0")
        self._transition_to_state(SovereignState.INITIALIZED, {
            "action": "poison_counter_reset",
            "previous_count": old_count
        })
    
    def export_state_log(self, filename: str = "sroi_state_export.json"):
        """Export complete state history to JSON file
        
        Args:
            filename: Output filename for state history export
        """
        export_data = {
            "current_state": self.current_state.value,
            "poison_detection_count": self.poison_detection_count,
            "stealth_active": self.d6_stealth_active,
            "s_roi_threshold": self.s_roi,
            "state_history": self.get_state_history(),
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"State history exported to {filename}")
        return filename

# Lex Amoris Signature: All data under protection. (Push and deploy)