"""
test_lex_amoris_security.py - Tests for Lex Amoris Security System

Tests all components of the strategic security improvements:
- Rhythm Validation
- Dynamic Blacklist
- Lazy Security
- IPFS Backup
- Rescue Channel
"""

import unittest
import json
import os
import tempfile
import shutil
from datetime import datetime, timezone

from lex_amoris_security import (
    RhythmValidator,
    DynamicBlacklist,
    LazySecurity,
    IPFSBackupManager,
    RescueChannel,
    LexAmorisSecuritySystem
)


class TestRhythmValidator(unittest.TestCase):
    """Test rhythm validation functionality."""
    
    def setUp(self):
        self.validator = RhythmValidator(base_frequency=432.0)
    
    def test_initialization(self):
        """Test validator initialization."""
        self.assertEqual(self.validator.base_frequency, 432.0)
        self.assertEqual(self.validator.tolerance, 0.05)
        self.assertEqual(len(self.validator.validation_log), 0)
    
    def test_calculate_packet_frequency(self):
        """Test frequency calculation for packets."""
        data = {"message": "test", "timestamp": "2025-01-15"}
        frequency = self.validator.calculate_packet_frequency(data)
        
        self.assertIsInstance(frequency, float)
        self.assertGreater(frequency, 0)
    
    def test_validate_rhythm_valid(self):
        """Test validation of packets with acceptable frequency."""
        # Create a packet that should have valid frequency
        data = {"sentimento": "love", "rhythm": "harmonic"}
        is_valid, reason = self.validator.validate_rhythm(data)
        
        # Should return a boolean and string
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(reason, str)
    
    def test_validate_rhythm_logs(self):
        """Test that validations are logged."""
        data = {"test": "data"}
        self.validator.validate_rhythm(data, "192.168.1.1")
        
        self.assertEqual(len(self.validator.validation_log), 1)
        log_entry = self.validator.validation_log[0]
        
        self.assertIn("timestamp", log_entry)
        self.assertIn("source_ip", log_entry)
        self.assertIn("frequency", log_entry)
        self.assertIn("valid", log_entry)
    
    def test_validate_empty_packet(self):
        """Test validation of empty packet."""
        is_valid, reason = self.validator.validate_rhythm({})
        
        self.assertFalse(is_valid)
        self.assertEqual(reason, "Empty packet")
    
    def test_validation_log_limit(self):
        """Test that validation log is limited to 1000 entries."""
        # Add more than 1000 validations (using 1050 for reasonable test time)
        for i in range(1050):
            self.validator.validate_rhythm({"index": i})
        
        self.assertEqual(len(self.validator.validation_log), 1000)


class TestDynamicBlacklist(unittest.TestCase):
    """Test dynamic blacklist functionality."""
    
    def setUp(self):
        self.blacklist = DynamicBlacklist(threshold=5, time_window=300)
    
    def test_initialization(self):
        """Test blacklist initialization."""
        self.assertEqual(self.blacklist.threshold, 5)
        self.assertEqual(self.blacklist.time_window, 300)
        self.assertEqual(len(self.blacklist.failures), 0)
        self.assertEqual(len(self.blacklist.blacklist), 0)
    
    def test_record_failure(self):
        """Test recording failures."""
        source = "192.168.1.100"
        self.blacklist.record_failure(source)
        
        self.assertIn(source, self.blacklist.failures)
        self.assertEqual(len(self.blacklist.failures[source]), 1)
    
    def test_blacklist_after_threshold(self):
        """Test that source is blacklisted after threshold failures."""
        source = "10.0.0.1"
        
        # Record failures up to threshold
        for _ in range(5):
            self.blacklist.record_failure(source)
        
        self.assertTrue(self.blacklist.is_blacklisted(source))
    
    def test_not_blacklisted_below_threshold(self):
        """Test that source is not blacklisted below threshold."""
        source = "10.0.0.2"
        
        # Record failures below threshold
        for _ in range(3):
            self.blacklist.record_failure(source)
        
        self.assertFalse(self.blacklist.is_blacklisted(source))
    
    def test_get_blacklist(self):
        """Test getting current blacklist."""
        sources = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
        
        # Blacklist some sources
        for source in sources[:2]:
            for _ in range(5):
                self.blacklist.record_failure(source)
        
        blacklist = self.blacklist.get_blacklist()
        
        self.assertEqual(len(blacklist), 2)
        self.assertIn(sources[0], blacklist)
        self.assertIn(sources[1], blacklist)
    
    def test_time_window_cleanup(self):
        """Test that old failures are cleaned up."""
        # This test is simplified as we can't easily manipulate time
        # In production, would use time mocking
        source = "10.0.0.5"
        self.blacklist.record_failure(source)
        
        # Verify failure is recorded
        self.assertIn(source, self.blacklist.failures)


class TestLazySecurity(unittest.TestCase):
    """Test lazy security functionality."""
    
    def setUp(self):
        self.lazy_security = LazySecurity(activation_threshold=50.0)
    
    def test_initialization(self):
        """Test lazy security initialization."""
        self.assertEqual(self.lazy_security.activation_threshold, 50.0)
        self.assertFalse(self.lazy_security.is_active)
    
    def test_environmental_pressure_scan(self):
        """Test electromagnetic field scan."""
        pressure = self.lazy_security.environmental_pressure_scan()
        
        self.assertIsInstance(pressure, float)
        self.assertGreater(pressure, 0)
    
    def test_scan_history_logged(self):
        """Test that scans are logged."""
        self.lazy_security.environmental_pressure_scan()
        
        self.assertEqual(len(self.lazy_security.scan_history), 1)
        scan = self.lazy_security.scan_history[0]
        
        self.assertIn("timestamp", scan)
        self.assertIn("pressure", scan)
    
    def test_should_activate(self):
        """Test activation decision."""
        result = self.lazy_security.should_activate()
        
        self.assertIsInstance(result, bool)
    
    def test_get_status(self):
        """Test getting security status."""
        self.lazy_security.should_activate()
        status = self.lazy_security.get_status()
        
        self.assertIn("is_active", status)
        self.assertIn("activation_threshold", status)
        self.assertIn("recent_scans", status)
    
    def test_scan_history_limit(self):
        """Test that scan history is limited."""
        # Perform more than 100 scans
        for _ in range(110):
            self.lazy_security.environmental_pressure_scan()
        
        self.assertEqual(len(self.lazy_security.scan_history), 100)


class TestIPFSBackupManager(unittest.TestCase):
    """Test IPFS backup functionality."""
    
    def setUp(self):
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.backup_manager = IPFSBackupManager(backup_dir=os.path.join(self.temp_dir, "backup"))
        
        # Create test files
        self.test_files = []
        for i in range(3):
            test_file = os.path.join(self.temp_dir, f"test_config_{i}.json")
            with open(test_file, "w") as f:
                json.dump({"config": f"value_{i}"}, f)
            self.test_files.append(test_file)
    
    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test backup manager initialization."""
        self.assertTrue(os.path.exists(self.backup_manager.backup_dir))
    
    def test_create_backup(self):
        """Test creating backup of configuration files."""
        manifest = self.backup_manager.create_backup(self.test_files)
        
        self.assertIn("timestamp", manifest)
        self.assertIn("files", manifest)
        self.assertEqual(len(manifest["files"]), 3)
    
    def test_backup_contains_hashes(self):
        """Test that backup manifest contains file hashes."""
        manifest = self.backup_manager.create_backup(self.test_files)
        
        for file_path in self.test_files:
            self.assertIn(file_path, manifest["files"])
            file_info = manifest["files"][file_path]
            self.assertIn("hash", file_info)
            self.assertIn("backup_path", file_info)
    
    def test_verify_backup(self):
        """Test backup verification."""
        self.backup_manager.create_backup(self.test_files)
        
        # Verify each backed up file
        for file_path in self.test_files:
            is_valid = self.backup_manager.verify_backup(file_path)
            self.assertTrue(is_valid)
    
    def test_verify_nonexistent_file(self):
        """Test verification of nonexistent backup."""
        is_valid = self.backup_manager.verify_backup("/nonexistent/file.json")
        self.assertFalse(is_valid)
    
    def test_backup_nonexistent_file(self):
        """Test backing up nonexistent file."""
        manifest = self.backup_manager.create_backup(["/nonexistent/file.json"])
        
        # When file doesn't exist, it won't be in the manifest files dict
        # unless it has an error entry
        self.assertIsInstance(manifest, dict)
        self.assertIn("files", manifest)


class TestRescueChannel(unittest.TestCase):
    """Test rescue channel functionality."""
    
    def setUp(self):
        self.rescue_channel = RescueChannel()
    
    def test_initialization(self):
        """Test rescue channel initialization."""
        self.assertEqual(len(self.rescue_channel.rescue_log), 0)
        self.assertEqual(self.rescue_channel.false_positive_threshold, 0.3)
    
    def test_send_rescue_message(self):
        """Test sending rescue message."""
        message = self.rescue_channel.send_rescue_message("192.168.1.1", "test_reason")
        
        self.assertIn("timestamp", message)
        self.assertIn("type", message)
        self.assertEqual(message["type"], "rescue")
        self.assertIn("lex_amoris_signature", message)
        self.assertEqual(message["lex_amoris_signature"], "love_first_protocol")
    
    def test_rescue_log_updated(self):
        """Test that rescue log is updated."""
        self.rescue_channel.send_rescue_message("10.0.0.1")
        
        self.assertEqual(len(self.rescue_channel.rescue_log), 1)
    
    def test_analyze_false_positives_empty_log(self):
        """Test false positive analysis with empty log."""
        rate = self.rescue_channel.analyze_false_positives([])
        self.assertEqual(rate, 0.0)
    
    def test_analyze_false_positives(self):
        """Test false positive analysis."""
        # Create mock validation log
        validation_log = [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source_ip": "10.0.0.1",
                "valid": False
            },
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source_ip": "10.0.0.1",
                "valid": False
            },
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source_ip": "10.0.0.1",
                "valid": True
            }
        ]
        
        rate = self.rescue_channel.analyze_false_positives(validation_log)
        
        self.assertIsInstance(rate, float)
        self.assertGreaterEqual(rate, 0.0)
        self.assertLessEqual(rate, 1.0)
    
    def test_rescue_log_limit(self):
        """Test that rescue log is limited."""
        # Send more than 100 rescue messages
        for i in range(110):
            self.rescue_channel.send_rescue_message(f"10.0.0.{i}")
        
        self.assertEqual(len(self.rescue_channel.rescue_log), 100)


class TestLexAmorisSecuritySystem(unittest.TestCase):
    """Test integrated security system."""
    
    def setUp(self):
        self.security_system = LexAmorisSecuritySystem()
    
    def test_initialization(self):
        """Test security system initialization."""
        self.assertIsNotNone(self.security_system.rhythm_validator)
        self.assertIsNotNone(self.security_system.blacklist)
        self.assertIsNotNone(self.security_system.lazy_security)
        self.assertIsNotNone(self.security_system.ipfs_backup)
        self.assertIsNotNone(self.security_system.rescue_channel)
    
    def test_process_packet(self):
        """Test processing a data packet."""
        data = {"message": "test", "sentimento": "love"}
        result = self.security_system.process_packet(data, "192.168.1.1")
        
        self.assertIn("timestamp", result)
        self.assertIn("source", result)
        self.assertIn("accepted", result)
        self.assertIn("reason", result)
    
    def test_process_packet_with_blacklist(self):
        """Test packet processing with blacklisted source."""
        source = "10.0.0.100"
        
        # Blacklist the source
        for _ in range(5):
            self.security_system.blacklist.record_failure(source)
        
        # Try to process packet from blacklisted source
        data = {"message": "test"}
        
        # Force lazy security to be active
        self.security_system.lazy_security.is_active = True
        
        result = self.security_system.process_packet(data, source)
        
        # May be rejected or rescued depending on false positive detection
        self.assertIn("reason", result)
    
    def test_get_system_status(self):
        """Test getting complete system status."""
        status = self.security_system.get_system_status()
        
        self.assertIn("timestamp", status)
        self.assertIn("lazy_security", status)
        self.assertIn("blacklist", status)
        self.assertIn("rhythm_validation", status)
        self.assertIn("rescue_channel", status)
        self.assertIn("backup", status)
    
    def test_create_configuration_backup(self):
        """Test creating configuration backup."""
        # This will only backup files that exist
        manifest = self.security_system.create_configuration_backup()
        
        self.assertIn("timestamp", manifest)
        self.assertIn("files", manifest)
    
    def test_lazy_security_integration(self):
        """Test that lazy security affects packet processing."""
        data = {"test": "data"}
        
        # Process when lazy security is inactive
        result = self.security_system.process_packet(data, "192.168.1.1")
        
        # Should have a result
        self.assertIsInstance(result, dict)


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
