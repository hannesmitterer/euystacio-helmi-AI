"""
Tests for Bio-Clock Signal Isolation Module
EU 2026 Compliance Testing
"""

import unittest
import time
import json
from bioclock_signal_isolation import BioClock, DecentralizedTimeReference


class TestBioClock(unittest.TestCase):
    """Test cases for BioClock class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.clock = BioClock(seed="test_seed_12345")
    
    def test_initialization(self):
        """Test bio-clock initialization"""
        self.assertEqual(self.clock.FREQUENCY_HZ, 0.0043)
        self.assertAlmostEqual(self.clock.PERIOD_SECONDS, 232.56, places=1)
        self.assertEqual(self.clock.cycle_count, 0)
        self.assertEqual(self.clock.seed, "test_seed_12345")
    
    def test_phase_calculation(self):
        """Test current phase calculation"""
        phase = self.clock.get_current_phase()
        self.assertIsInstance(phase, float)
        self.assertGreaterEqual(phase, 0.0)
        self.assertLess(phase, 1.0)
    
    def test_cryptographic_timestamp(self):
        """Test cryptographic timestamp generation"""
        timestamp, signature = self.clock.get_cryptographic_timestamp()
        
        self.assertIsInstance(timestamp, float)
        self.assertIsInstance(signature, str)
        self.assertEqual(len(signature), 64)  # SHA256 hex digest
    
    def test_timestamp_verification(self):
        """Test timestamp verification"""
        timestamp, signature = self.clock.get_cryptographic_timestamp()
        
        # Should verify correctly
        self.assertTrue(self.clock.verify_timestamp(timestamp, signature))
        
        # Should fail with wrong signature
        wrong_signature = "0" * 64
        self.assertFalse(self.clock.verify_timestamp(timestamp, wrong_signature))
    
    def test_drift_compensation(self):
        """Test clock drift compensation"""
        reference_time = time.time() + 10.0  # 10 seconds ahead
        drift = self.clock.compensate_drift(reference_time)
        
        self.assertGreater(drift, 0)
        self.assertGreater(self.clock.drift_compensation, 0)
    
    def test_status_retrieval(self):
        """Test status retrieval"""
        status = self.clock.get_status()
        
        self.assertIn('frequency_hz', status)
        self.assertIn('cycle_count', status)
        self.assertIn('current_phase', status)
        self.assertEqual(status['frequency_hz'], 0.0043)
    
    def test_state_export_import(self):
        """Test state export and import"""
        # Run a few cycles
        self.clock.cycle_count = 5
        self.clock.drift_compensation = 1.5
        
        # Export state
        state_json = self.clock.export_state()
        self.assertIsInstance(state_json, str)
        
        # Create new clock and import state
        new_clock = BioClock()
        new_clock.import_state(state_json)
        
        self.assertEqual(new_clock.cycle_count, 5)
        self.assertEqual(new_clock.drift_compensation, 1.5)
        self.assertEqual(new_clock.seed, self.clock.seed)
    
    def test_seed_generation(self):
        """Test automatic seed generation"""
        clock1 = BioClock()
        clock2 = BioClock()
        
        # Seeds should be different
        self.assertNotEqual(clock1.seed, clock2.seed)
    
    def test_oscillator_initialization(self):
        """Test oscillator state initialization"""
        osc_state = self.clock._oscillator_state
        
        self.assertIn('phase', osc_state)
        self.assertIn('frequency', osc_state)
        self.assertEqual(osc_state['frequency'], 0.0043)


class TestDecentralizedTimeReference(unittest.TestCase):
    """Test cases for DecentralizedTimeReference class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.time_ref = DecentralizedTimeReference()
    
    def test_initialization(self):
        """Test time reference initialization"""
        self.assertEqual(len(self.time_ref.sources), 0)
        self.assertEqual(self.time_ref.consensus_threshold, 0.5)
    
    def test_add_time_source(self):
        """Test adding time sources"""
        timestamp = time.time()
        self.time_ref.add_time_source("test_source", timestamp, "signature123")
        
        self.assertEqual(len(self.time_ref.sources), 1)
        self.assertEqual(self.time_ref.sources[0]['name'], "test_source")
        self.assertEqual(self.time_ref.sources[0]['timestamp'], timestamp)
    
    def test_consensus_time_single_source(self):
        """Test consensus with single source"""
        timestamp = time.time()
        self.time_ref.add_time_source("source1", timestamp)
        
        consensus = self.time_ref.get_consensus_time()
        self.assertEqual(consensus, timestamp)
    
    def test_consensus_time_multiple_sources(self):
        """Test consensus with multiple sources"""
        base_time = time.time()
        
        self.time_ref.add_time_source("source1", base_time)
        self.time_ref.add_time_source("source2", base_time + 1)
        self.time_ref.add_time_source("source3", base_time + 2)
        
        consensus = self.time_ref.get_consensus_time()
        
        # Should return median (base_time + 1)
        self.assertEqual(consensus, base_time + 1)
    
    def test_consensus_time_even_sources(self):
        """Test consensus with even number of sources"""
        base_time = time.time()
        
        self.time_ref.add_time_source("source1", base_time)
        self.time_ref.add_time_source("source2", base_time + 2)
        
        consensus = self.time_ref.get_consensus_time()
        
        # Should return average of middle two (base_time + 1)
        self.assertEqual(consensus, base_time + 1)
    
    def test_clear_old_sources(self):
        """Test clearing old time sources"""
        current_time = time.time()
        
        # Add a current source
        self.time_ref.add_time_source("current", current_time)
        
        # Manually add an old source
        old_source = {
            'name': 'old_source',
            'timestamp': current_time - 600,
            'signature': None,
            'added_at': current_time - 600
        }
        self.time_ref.sources.append(old_source)
        
        self.assertEqual(len(self.time_ref.sources), 2)
        
        # Clear sources older than 300 seconds
        self.time_ref.clear_old_sources(max_age_seconds=300)
        
        # Only current source should remain
        self.assertEqual(len(self.time_ref.sources), 1)
        self.assertEqual(self.time_ref.sources[0]['name'], 'current')
    
    def test_consensus_with_no_sources(self):
        """Test consensus time with no sources"""
        consensus = self.time_ref.get_consensus_time()
        self.assertIsNone(consensus)


class TestIntegration(unittest.TestCase):
    """Integration tests for bio-clock and time reference"""
    
    def test_bio_clock_with_time_reference(self):
        """Test bio-clock integrated with decentralized time reference"""
        clock = BioClock()
        time_ref = DecentralizedTimeReference()
        
        # Add local time
        local_time = time.time()
        time_ref.add_time_source("local", local_time)
        
        # Add cryptographic timestamp from bio-clock
        crypto_time, signature = clock.get_cryptographic_timestamp()
        time_ref.add_time_source("crypto", crypto_time, signature)
        
        # Get consensus
        consensus = time_ref.get_consensus_time()
        
        self.assertIsNotNone(consensus)
        self.assertAlmostEqual(consensus, local_time, delta=1.0)
    
    def test_drift_compensation_with_consensus(self):
        """Test drift compensation using consensus time"""
        clock = BioClock()
        time_ref = DecentralizedTimeReference()
        
        # Simulate drift by adding time sources
        base_time = time.time()
        time_ref.add_time_source("source1", base_time + 5)
        time_ref.add_time_source("source2", base_time + 5)
        time_ref.add_time_source("source3", base_time + 5)
        
        consensus = time_ref.get_consensus_time()
        drift = clock.compensate_drift(consensus)
        
        # Drift should be detected
        self.assertGreater(abs(drift), 0)


if __name__ == '__main__':
    print("Running Bio-Clock Signal Isolation Tests")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)
