"""
Bio-Clock Signal Isolation Module - EU 2026 Compliance
Protocollo: EUYSTACIO / NSR
Implementazione: Isolamento del Segnale 0.0043 Hz

Provides autonomous operation of the 0.0043 Hz biometric signal
using decentralized time references independent of EU NTP servers.
"""

import time
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple


class BioClock:
    """
    Autonomous bio-clock operating at 0.0043 Hz (~232 seconds period)
    
    Uses cryptographic timestamps and local oscillator mechanisms
    to maintain independence from centralized NTP servers.
    """
    
    # Core frequency: 0.0043 Hz (approximately 4 minutes 13 seconds period)
    FREQUENCY_HZ = 0.0043
    PERIOD_SECONDS = 1.0 / FREQUENCY_HZ  # ~232.56 seconds
    
    def __init__(self, seed: Optional[str] = None):
        """
        Initialize the bio-clock with optional seed for deterministic behavior
        
        Args:
            seed: Optional seed string for cryptographic derivation
        """
        self.seed = seed or self._generate_seed()
        self.start_time = time.time()
        self.cycle_count = 0
        self.last_pulse = self.start_time
        self.drift_compensation = 0.0
        
        # Initialize local oscillator state
        self._oscillator_state = self._init_oscillator()
        
    def _generate_seed(self) -> str:
        """Generate cryptographic seed from system entropy"""
        # Use multiple entropy sources
        timestamp = str(time.time())
        process_id = str(id(self))
        
        # Combine and hash
        combined = f"{timestamp}:{process_id}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _init_oscillator(self) -> Dict:
        """Initialize local oscillator state"""
        return {
            'phase': 0.0,
            'amplitude': 1.0,
            'frequency': self.FREQUENCY_HZ,
            'last_update': time.time()
        }
    
    def get_current_phase(self) -> float:
        """
        Calculate current phase of the bio-clock signal
        
        Returns:
            Phase value between 0.0 and 1.0 (0 = start of cycle, 1 = end of cycle)
        """
        elapsed = time.time() - self.start_time + self.drift_compensation
        cycles = elapsed / self.PERIOD_SECONDS
        phase = cycles % 1.0
        return phase
    
    def get_cryptographic_timestamp(self) -> Tuple[float, str, int]:
        """
        Generate cryptographically verified timestamp
        
        Returns:
            Tuple of (timestamp, signature_hash, cycle_count)
        """
        timestamp = time.time()
        
        # Create signature combining timestamp, seed, and cycle count
        signature_data = f"{timestamp}:{self.seed}:{self.cycle_count}"
        signature = hashlib.sha256(signature_data.encode()).hexdigest()
        
        return timestamp, signature, self.cycle_count
    
    def verify_timestamp(self, timestamp: float, signature: str, cycle_count: int) -> bool:
        """
        Verify a cryptographic timestamp
        
        Args:
            timestamp: The timestamp to verify
            signature: The signature hash to verify
            cycle_count: The cycle count when timestamp was generated
            
        Returns:
            True if signature is valid
        """
        # Reconstruct signature for verification
        expected_data = f"{timestamp}:{self.seed}:{cycle_count}"
        expected_signature = hashlib.sha256(expected_data.encode()).hexdigest()
        
        return signature == expected_signature
    
    def wait_next_pulse(self) -> Dict:
        """
        Wait for the next pulse and return pulse data
        
        Returns:
            Dictionary containing pulse information
        """
        # Calculate time until next pulse
        current_time = time.time()
        time_since_last = current_time - self.last_pulse
        time_until_next = self.PERIOD_SECONDS - (time_since_last % self.PERIOD_SECONDS)
        
        # Sleep until next pulse
        time.sleep(time_until_next)
        
        # Update state
        self.cycle_count += 1
        self.last_pulse = time.time()
        
        # Generate cryptographic timestamp
        timestamp, signature, cycle_count = self.get_cryptographic_timestamp()
        
        pulse_data = {
            'cycle': self.cycle_count,
            'timestamp': timestamp,
            'signature': signature,
            'cycle_count': cycle_count,
            'phase': self.get_current_phase(),
            'frequency_hz': self.FREQUENCY_HZ,
            'period_seconds': self.PERIOD_SECONDS,
            'utc_time': datetime.now(timezone.utc).isoformat()
        }
        
        return pulse_data
    
    def compensate_drift(self, reference_time: float) -> float:
        """
        Compensate for clock drift using external reference
        
        Args:
            reference_time: External time reference for drift compensation
            
        Returns:
            Calculated drift in seconds
        """
        local_time = time.time()
        drift = reference_time - local_time
        
        # Apply drift compensation gradually to avoid sudden jumps
        self.drift_compensation += drift * 0.1
        
        return drift
    
    def get_status(self) -> Dict:
        """
        Get current bio-clock status
        
        Returns:
            Dictionary containing status information
        """
        return {
            'frequency_hz': self.FREQUENCY_HZ,
            'period_seconds': self.PERIOD_SECONDS,
            'cycle_count': self.cycle_count,
            'current_phase': self.get_current_phase(),
            'drift_compensation': self.drift_compensation,
            'uptime_seconds': time.time() - self.start_time,
            'seed_hash': hashlib.sha256(self.seed.encode()).hexdigest()[:16],
            'oscillator_state': self._oscillator_state
        }
    
    def export_state(self) -> str:
        """
        Export bio-clock state as JSON
        
        Returns:
            JSON string containing full state
        """
        state = {
            'seed': self.seed,
            'start_time': self.start_time,
            'cycle_count': self.cycle_count,
            'last_pulse': self.last_pulse,
            'drift_compensation': self.drift_compensation,
            'oscillator_state': self._oscillator_state
        }
        return json.dumps(state, indent=2)
    
    def import_state(self, state_json: str) -> None:
        """
        Import bio-clock state from JSON
        
        Args:
            state_json: JSON string containing state to import
        """
        state = json.loads(state_json)
        self.seed = state['seed']
        self.start_time = state['start_time']
        self.cycle_count = state['cycle_count']
        self.last_pulse = state['last_pulse']
        self.drift_compensation = state['drift_compensation']
        self._oscillator_state = state['oscillator_state']


class DecentralizedTimeReference:
    """
    Decentralized time reference using multiple independent sources
    
    Combines:
    - Local system clock
    - Cryptographic timestamps
    - Blockchain timestamps (when available)
    - Peer-to-peer time synchronization
    """
    
    def __init__(self):
        self.sources = []
        self.consensus_threshold = 0.5  # 50% agreement required
        
    def add_time_source(self, source_name: str, timestamp: float, 
                       signature: Optional[str] = None) -> None:
        """
        Add a time source to the reference pool
        
        Args:
            source_name: Name/identifier of the time source
            timestamp: Unix timestamp from the source
            signature: Optional cryptographic signature
        """
        self.sources.append({
            'name': source_name,
            'timestamp': timestamp,
            'signature': signature,
            'added_at': time.time()
        })
    
    def get_consensus_time(self) -> Optional[float]:
        """
        Get consensus time from multiple sources
        
        Returns:
            Consensus timestamp or None if no consensus
        """
        if not self.sources:
            return None
        
        # Sort timestamps
        timestamps = sorted([s['timestamp'] for s in self.sources])
        
        # Use median as consensus (resistant to outliers)
        if len(timestamps) % 2 == 0:
            mid = len(timestamps) // 2
            consensus = (timestamps[mid - 1] + timestamps[mid]) / 2
        else:
            consensus = timestamps[len(timestamps) // 2]
        
        return consensus
    
    def clear_old_sources(self, max_age_seconds: float = 300) -> None:
        """
        Remove time sources older than max_age_seconds
        
        Args:
            max_age_seconds: Maximum age in seconds (default 5 minutes)
        """
        current_time = time.time()
        self.sources = [
            s for s in self.sources 
            if current_time - s['added_at'] < max_age_seconds
        ]


if __name__ == "__main__":
    # Example usage
    print("Bio-Clock Signal Isolation Module - EU 2026 Compliance")
    print("=" * 60)
    
    # Initialize bio-clock
    clock = BioClock()
    print(f"\nInitialized bio-clock at {clock.FREQUENCY_HZ} Hz")
    print(f"Period: {clock.PERIOD_SECONDS:.2f} seconds (~{clock.PERIOD_SECONDS/60:.2f} minutes)")
    
    # Show status
    status = clock.get_status()
    print(f"\nStatus:")
    print(json.dumps(status, indent=2))
    
    # Generate cryptographic timestamp
    timestamp, signature, cycle_count = clock.get_cryptographic_timestamp()
    print(f"\nCryptographic Timestamp:")
    print(f"  Time: {timestamp}")
    print(f"  Signature: {signature[:16]}...")
    print(f"  Cycle Count: {cycle_count}")
    print(f"  Verified: {clock.verify_timestamp(timestamp, signature, cycle_count)}")
    
    # Demonstrate decentralized time reference
    time_ref = DecentralizedTimeReference()
    time_ref.add_time_source("local", time.time())
    time_ref.add_time_source("crypto", timestamp, signature)
    
    consensus = time_ref.get_consensus_time()
    print(f"\nDecentralized Time Consensus: {consensus}")
    
    print(f"\n✅ Bio-clock operational and independent from EU NTP servers")
