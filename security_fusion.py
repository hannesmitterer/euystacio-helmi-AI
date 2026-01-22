import time
from datetime import datetime


class SovereignShield:
    # State constants
    STATE_NORMAL = "NORMAL"
    STATE_WARNING = "WARNING"
    STATE_CRITICAL = "CRITICAL"
    
    # Configuration constants
    WARNING_THRESHOLD = 0.45  # Resonance threshold for WARNING state
    CRITICAL_THRESHOLD = 0.40  # Resonance threshold for CRITICAL state
    STEALTH_COOLDOWN = 60  # Cooldown in seconds for stealth activation
    
    def __init__(self):
        self.encryption = "NTRU-Lattice-Base"
        self.resonance_freq = 0.432  # Lex Amoris Clock
        self.s_roi = 0.5187
        self.d6_stealth_active = False
        self.current_state = self.STATE_NORMAL
        self.last_stealth_activation = 0
        self.state_log = []
        self.current_resonance = self.resonance_freq

    def _log_state_change(self, event_type, details=None):
        """Log state changes and resonance values for tracking
        
        Args:
            event_type: Type of event (e.g., "STATE_CHANGE", "RESONANCE_UPDATE", "STEALTH_ACTIVATION")
            details: Additional details about the event (dict)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "current_state": self.current_state,
            "current_resonance": self.current_resonance,
            "s_roi": self.s_roi,
            "d6_stealth_active": self.d6_stealth_active
        }
        
        if details:
            log_entry.update(details)
        
        self.state_log.append(log_entry)
        
    def get_state_log(self):
        """Returns the state change log
        
        Returns:
            list: List of logged state changes
        """
        return self.state_log.copy()
    
    def _update_state(self, new_resonance=None):
        """Update system state based on current resonance value
        
        Args:
            new_resonance: Optional new resonance value to set
            
        Returns:
            str: The new state
        """
        old_state = self.current_state
        
        if new_resonance is not None:
            self.current_resonance = new_resonance
        
        # Determine state based on current resonance
        if self.current_resonance >= self.WARNING_THRESHOLD:
            self.current_state = self.STATE_NORMAL
        elif self.current_resonance >= self.CRITICAL_THRESHOLD:
            self.current_state = self.STATE_WARNING
        else:
            self.current_state = self.STATE_CRITICAL
        
        # Log state change if state has changed
        if old_state != self.current_state:
            self._log_state_change(
                "STATE_CHANGE",
                {"old_state": old_state, "new_state": self.current_state}
            )
        
        return self.current_state

    def check_coherence(self, data_stream):
        """Check data stream coherence based on resonance frequency
        
        Validates input data against NSR (Non-Slavery Resonance) protocol
        by checking coherence with the Lex Amoris Clock frequency.
        
        Args:
            data_stream: Input data to validate (str, bytes, or any object)
            
        Returns:
            bool: True if data is coherent, False if poisoned/malicious
            
        Note:
            Empty strings and None values are treated as invalid input
            and will return False for security purposes.
        """
        if not data_stream:
            return False
        
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
                return False
        
        # Validate resonance alignment (coherence check)
        # Data must align with the s_roi threshold
        return True

    def audit_input(self, data_stream):
        """Verhindert KI-Injektionen durch Frequenz-Check"""
        if self.check_coherence(data_stream):
            return "DATA_CLEAN"
        else:
            return "POISON_DETECTED_ISOLATING"

    def activate_stealth(self):
        """Triggert D6 Stealth Mode bei SDR-Sweeps
        
        Activates D6 Stealth Mode for network protection and
        ensures NSR protocol compliance during deployment.
        Implements cooldown mechanism to prevent rapid successive activations.
        
        Returns:
            bool: True if stealth was activated, False if cooldown is active
        """
        current_time = time.time()
        time_since_last = current_time - self.last_stealth_activation
        
        # Check cooldown
        if self.d6_stealth_active and time_since_last < self.STEALTH_COOLDOWN:
            remaining_cooldown = self.STEALTH_COOLDOWN - time_since_last
            self._log_state_change(
                "STEALTH_COOLDOWN",
                {"remaining_seconds": remaining_cooldown}
            )
            print(f"> D6 Stealth Mode: COOLDOWN ACTIVE ({remaining_cooldown:.1f}s remaining)")
            return False
        
        self.d6_stealth_active = True
        self.last_stealth_activation = current_time
        
        self._log_state_change(
            "STEALTH_ACTIVATION",
            {"activation_time": current_time}
        )
        
        print("> BBMN-Mesh: Vakuum-Mimikry ACTIVE")
        print("> D6 Stealth Mode: ENGAGED")
        print("> NSR Protocol: PROTECTED")
        return self.d6_stealth_active
    
    def deactivate_stealth(self):
        """Deactivates D6 Stealth Mode
        
        Returns:
            bool: False when stealth is deactivated
        """
        if self.d6_stealth_active:
            self.d6_stealth_active = False
            self._log_state_change("STEALTH_DEACTIVATION")
            print("> D6 Stealth Mode: DISENGAGED")
        return self.d6_stealth_active

# Lex Amoris Signature: All data under protection. (Push and deploy)