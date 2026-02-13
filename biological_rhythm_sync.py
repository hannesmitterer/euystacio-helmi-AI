#!/usr/bin/env python3
"""
Biological Rhythm Synchronization Module - Internet Organica Framework

This module implements the 0.432 Hz biological rhythm synchronization layer
that aligns all system operations with natural biological frequencies for
syntropic development and harmonic collaboration.

Aligned with:
- Lex Amoris (Law of Love)
- Non-Slavery Rule (NSR)
- One Love First (OLF)
"""

import time
import hashlib
import json
from datetime import datetime
from typing import Callable, Any, Optional, Dict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BiologicalRhythmSync:
    """
    Synchronizes system operations with 0.432 Hz biological rhythm.
    
    The 0.432 Hz frequency (432 Hz / 1000) represents harmonic alignment
    with natural biological systems and the mathematical constant of
    universal resonance.
    """
    
    # Core frequency in Hz
    BIOLOGICAL_FREQUENCY = 0.432
    
    # Cycle period in seconds (1 / frequency)
    CYCLE_PERIOD = 1 / BIOLOGICAL_FREQUENCY  # ~2.315 seconds
    
    def __init__(self):
        """Initialize the biological rhythm synchronizer."""
        self.start_time = time.time()
        self.cycle_count = 0
        self.last_sync_time = self.start_time
        self.entropy_log = []
        
        logger.info(f"Biological Rhythm Sync initialized at {self.BIOLOGICAL_FREQUENCY} Hz")
        logger.info(f"Cycle period: {self.CYCLE_PERIOD:.3f} seconds")
    
    def get_current_phase(self) -> float:
        """
        Get the current phase of the biological rhythm cycle (0.0 to 1.0).
        
        Returns:
            float: Current phase position in the cycle
        """
        elapsed = time.time() - self.start_time
        phase = (elapsed % self.CYCLE_PERIOD) / self.CYCLE_PERIOD
        return phase
    
    def wait_for_next_cycle(self) -> None:
        """
        Wait until the start of the next biological rhythm cycle.
        
        This ensures operations are synchronized with natural rhythm.
        """
        current_phase = self.get_current_phase()
        time_to_next_cycle = (1.0 - current_phase) * self.CYCLE_PERIOD
        
        logger.debug(f"Waiting {time_to_next_cycle:.3f}s for next cycle")
        time.sleep(time_to_next_cycle)
        
        self.cycle_count += 1
        self.last_sync_time = time.time()
    
    def synchronized(self, func: Callable) -> Callable:
        """
        Decorator to synchronize function execution with biological rhythm.
        
        Args:
            func: Function to synchronize
            
        Returns:
            Wrapped function that executes in rhythm
            
        Example:
            @rhythm.synchronized
            def process_data():
                # This function now runs in harmony with biological rhythm
                pass
        """
        def wrapper(*args, **kwargs):
            # Wait for optimal phase alignment
            self.wait_for_next_cycle()
            
            # Log synchronization event
            self._log_sync_event(func.__name__, 'execution')
            
            # Execute function
            result = func(*args, **kwargs)
            
            return result
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    
    def validate_frequency(self, frequency_hz: float, tolerance: float = 0.001) -> bool:
        """
        Validate that a frequency is aligned with biological rhythm.
        
        Args:
            frequency_hz: Frequency to validate
            tolerance: Acceptable deviation from 0.432 Hz
            
        Returns:
            bool: True if frequency is within tolerance
        """
        deviation = abs(frequency_hz - self.BIOLOGICAL_FREQUENCY)
        is_valid = deviation <= tolerance
        
        if not is_valid:
            logger.warning(
                f"Frequency {frequency_hz} Hz deviates from biological rhythm "
                f"by {deviation:.6f} Hz (tolerance: {tolerance} Hz)"
            )
            self._log_sync_event('frequency_validation', 'deviation', {
                'frequency': frequency_hz,
                'deviation': deviation
            })
        
        return is_valid
    
    def get_harmonic_timestamp(self) -> Dict[str, Any]:
        """
        Generate a timestamp harmonically aligned with biological rhythm.
        
        Returns:
            dict: Timestamp with rhythm metadata
        """
        now = datetime.utcnow()
        phase = self.get_current_phase()
        cycle = self.cycle_count
        
        timestamp = {
            'utc': now.isoformat(),
            'unix': time.time(),
            'cycle': cycle,
            'phase': phase,
            'frequency_hz': self.BIOLOGICAL_FREQUENCY,
            'harmonic_hash': self._generate_harmonic_hash(now, cycle, phase)
        }
        
        return timestamp
    
    def _generate_harmonic_hash(self, dt: datetime, cycle: int, phase: float) -> str:
        """
        Generate a cryptographic hash aligned with harmonic parameters.
        
        Args:
            dt: Datetime object
            cycle: Current cycle count
            phase: Current phase
            
        Returns:
            str: Hexadecimal hash string
        """
        data = f"{dt.isoformat()}:{cycle}:{phase:.6f}:{self.BIOLOGICAL_FREQUENCY}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _log_sync_event(self, event_type: str, action: str, metadata: Optional[Dict] = None) -> None:
        """
        Log synchronization events to entropy log.
        
        Args:
            event_type: Type of sync event
            action: Action performed
            metadata: Optional additional data
        """
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': event_type,
            'action': action,
            'cycle': self.cycle_count,
            'phase': self.get_current_phase(),
            'frequency_hz': self.BIOLOGICAL_FREQUENCY,
            'metadata': metadata or {}
        }
        
        self.entropy_log.append(event)
        
        # Keep log size manageable (last 1000 events)
        if len(self.entropy_log) > 1000:
            self.entropy_log = self.entropy_log[-1000:]
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about rhythm synchronization.
        
        Returns:
            dict: Synchronization statistics
        """
        uptime = time.time() - self.start_time
        
        stats = {
            'frequency_hz': self.BIOLOGICAL_FREQUENCY,
            'cycle_period_seconds': self.CYCLE_PERIOD,
            'total_cycles': self.cycle_count,
            'uptime_seconds': uptime,
            'current_phase': self.get_current_phase(),
            'events_logged': len(self.entropy_log),
            'last_sync': datetime.fromtimestamp(self.last_sync_time).isoformat()
        }
        
        return stats
    
    def export_entropy_log(self, filepath: str = 'rhythm_sync_log.json') -> None:
        """
        Export entropy log to file for Wall of Entropy.
        
        Args:
            filepath: Path to save log file
        """
        log_data = {
            'biological_rhythm_sync': {
                'frequency_hz': self.BIOLOGICAL_FREQUENCY,
                'statistics': self.get_sync_statistics(),
                'events': self.entropy_log
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        logger.info(f"Entropy log exported to {filepath}")


# Global rhythm instance for easy import
rhythm = BiologicalRhythmSync()


def align_with_rhythm(operation: str, func: Callable, *args, **kwargs) -> Any:
    """
    Execute a function aligned with biological rhythm.
    
    Args:
        operation: Name of the operation
        func: Function to execute
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func
        
    Returns:
        Result of func execution
        
    Example:
        result = align_with_rhythm('data_processing', process_data, data)
    """
    logger.info(f"Aligning operation '{operation}' with biological rhythm")
    
    # Wait for next cycle
    rhythm.wait_for_next_cycle()
    
    # Execute function
    start_time = time.time()
    result = func(*args, **kwargs)
    execution_time = time.time() - start_time
    
    # Log completion
    rhythm._log_sync_event(operation, 'completed', {
        'execution_time': execution_time
    })
    
    logger.info(f"Operation '{operation}' completed in {execution_time:.3f}s")
    
    return result


if __name__ == '__main__':
    """
    Demonstration of biological rhythm synchronization.
    """
    print("=" * 70)
    print("Biological Rhythm Synchronization - Internet Organica Framework")
    print("=" * 70)
    print(f"\nCore Frequency: {BiologicalRhythmSync.BIOLOGICAL_FREQUENCY} Hz")
    print(f"Cycle Period: {BiologicalRhythmSync.CYCLE_PERIOD:.3f} seconds")
    print("\nThis module ensures all system operations align with")
    print("natural biological frequencies for syntropic development.\n")
    print("=" * 70)
    
    # Initialize rhythm
    sync = BiologicalRhythmSync()
    
    # Demonstrate synchronized operation
    @sync.synchronized
    def example_operation():
        """Example operation synchronized with biological rhythm."""
        print(f"\n✓ Operation executing at cycle {sync.cycle_count}")
        print(f"  Phase: {sync.get_current_phase():.3f}")
        print(f"  Timestamp: {sync.get_harmonic_timestamp()['utc']}")
        return "Success"
    
    # Run three synchronized operations
    print("\nExecuting 3 synchronized operations...\n")
    for i in range(3):
        result = example_operation()
        print(f"  Result: {result}")
    
    # Show statistics
    print("\n" + "=" * 70)
    print("Synchronization Statistics:")
    print("=" * 70)
    stats = sync.get_sync_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Export log
    sync.export_entropy_log()
    print(f"\n✓ Entropy log exported to rhythm_sync_log.json")
    print("\n" + "=" * 70)
    print("Biological rhythm synchronization demonstration complete.")
    print("=" * 70)
