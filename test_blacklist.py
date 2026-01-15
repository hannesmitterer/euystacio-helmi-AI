#!/usr/bin/env python3
"""
Test suite for EUYSTACIO Blacklist System
Tests core blacklist functionality and integration.
"""

import os
import sys
import json
import unittest
from datetime import datetime

from blacklist import EuystacioBlacklist, ensure_blacklist


class TestEuystacioBlacklist(unittest.TestCase):
    """Test cases for the Euystacio Blacklist system."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.test_blacklist_path = "test_blacklist.json"
        # Remove test file if it exists
        if os.path.exists(self.test_blacklist_path):
            os.remove(self.test_blacklist_path)
        self.blacklist = EuystacioBlacklist(self.test_blacklist_path)
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_blacklist_path):
            os.remove(self.test_blacklist_path)
    
    def test_blacklist_initialization(self):
        """Test that blacklist initializes with correct structure."""
        self.assertIsNotNone(self.blacklist.blacklist_data)
        self.assertIn('blocked_entities', self.blacklist.blacklist_data)
        self.assertIn('metadata', self.blacklist.blacklist_data)
        self.assertIn('statistics', self.blacklist.blacklist_data)
        self.assertEqual(len(self.blacklist.blacklist_data['blocked_entities']), 0)
    
    def test_add_entity(self):
        """Test adding an entity to the blacklist."""
        success = self.blacklist.add_entity(
            entity_id="192.168.1.100",
            entity_type="ip_address",
            reason="Suspicious activity detected",
            severity="high"
        )
        self.assertTrue(success)
        self.assertEqual(len(self.blacklist.blacklist_data['blocked_entities']), 1)
        self.assertEqual(self.blacklist.blacklist_data['statistics']['total_blocked'], 1)
    
    def test_add_duplicate_entity(self):
        """Test that adding duplicate entity returns False."""
        entity_id = "malicious_bot_001"
        self.blacklist.add_entity(entity_id, "ai_agent", "Malicious behavior", "critical")
        success = self.blacklist.add_entity(entity_id, "ai_agent", "Duplicate", "high")
        self.assertFalse(success)
        self.assertEqual(len(self.blacklist.blacklist_data['blocked_entities']), 1)
    
    def test_is_blocked(self):
        """Test checking if entity is blocked."""
        entity_id = "threat_node_123"
        self.assertFalse(self.blacklist.is_blocked(entity_id))
        
        self.blacklist.add_entity(entity_id, "node_id", "DDoS attack", "critical")
        self.assertTrue(self.blacklist.is_blocked(entity_id))
    
    def test_get_entity(self):
        """Test retrieving entity details."""
        entity_id = "suspicious_ip_456"
        self.blacklist.add_entity(
            entity_id=entity_id,
            entity_type="ip_address",
            reason="Port scanning detected",
            severity="high",
            metadata={"country": "unknown", "attempts": 5}
        )
        
        entity = self.blacklist.get_entity(entity_id)
        self.assertIsNotNone(entity)
        self.assertEqual(entity['entity_id'], entity_id)
        self.assertEqual(entity['severity'], "high")
        self.assertEqual(entity['metadata']['attempts'], 5)
    
    def test_remove_entity(self):
        """Test removing an entity from blacklist."""
        entity_id = "temp_block_789"
        self.blacklist.add_entity(entity_id, "ai_agent", "Test block", "medium")
        self.assertTrue(self.blacklist.is_blocked(entity_id))
        
        success = self.blacklist.remove_entity(entity_id)
        self.assertTrue(success)
        self.assertFalse(self.blacklist.is_blocked(entity_id))
        self.assertEqual(self.blacklist.blacklist_data['statistics']['total_blocked'], 0)
    
    def test_remove_nonexistent_entity(self):
        """Test removing entity that doesn't exist."""
        success = self.blacklist.remove_entity("nonexistent_id")
        self.assertFalse(success)
    
    def test_list_blocked_entities(self):
        """Test listing blocked entities."""
        self.blacklist.add_entity("ip1", "ip_address", "Attack", "critical")
        self.blacklist.add_entity("ip2", "ip_address", "Scan", "high")
        self.blacklist.add_entity("bot1", "ai_agent", "Malicious", "critical")
        
        all_entities = self.blacklist.list_blocked_entities()
        self.assertEqual(len(all_entities), 3)
        
        ip_entities = self.blacklist.list_blocked_entities(entity_type="ip_address")
        self.assertEqual(len(ip_entities), 2)
        
        critical_entities = self.blacklist.list_blocked_entities(severity="critical")
        self.assertEqual(len(critical_entities), 2)
    
    def test_check_and_log_attempt(self):
        """Test checking and logging blocked attempts."""
        entity_id = "blocked_entity"
        self.blacklist.add_entity(entity_id, "node_id", "Threat", "high")
        
        initial_count = self.blacklist.blacklist_data['statistics']['total_blocks_prevented']
        is_blocked = self.blacklist.check_and_log_attempt(entity_id)
        
        self.assertTrue(is_blocked)
        self.assertEqual(
            self.blacklist.blacklist_data['statistics']['total_blocks_prevented'],
            initial_count + 1
        )
        self.assertIsNotNone(self.blacklist.blacklist_data['statistics']['last_threat_detected'])
    
    def test_get_statistics(self):
        """Test getting blacklist statistics."""
        stats = self.blacklist.get_statistics()
        self.assertIn('total_blocked', stats)
        self.assertIn('total_blocks_prevented', stats)
        self.assertIn('last_threat_detected', stats)
    
    def test_get_all_blocked_ids(self):
        """Test getting set of all blocked IDs."""
        self.blacklist.add_entity("id1", "type1", "reason1", "high")
        self.blacklist.add_entity("id2", "type2", "reason2", "medium")
        self.blacklist.add_entity("id3", "type3", "reason3", "critical")
        
        blocked_ids = self.blacklist.get_all_blocked_ids()
        self.assertEqual(len(blocked_ids), 3)
        self.assertIn("id1", blocked_ids)
        self.assertIn("id2", blocked_ids)
        self.assertIn("id3", blocked_ids)
    
    def test_persistence(self):
        """Test that blacklist persists to file."""
        entity_id = "persistent_entity"
        self.blacklist.add_entity(entity_id, "test", "persistence test", "low")
        
        # Create new instance to load from file
        new_blacklist = EuystacioBlacklist(self.test_blacklist_path)
        self.assertTrue(new_blacklist.is_blocked(entity_id))
    
    def test_ensure_blacklist(self):
        """Test ensure_blacklist function."""
        test_path = "test_ensure_blacklist.json"
        if os.path.exists(test_path):
            os.remove(test_path)
        
        success = ensure_blacklist(test_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(test_path))
        
        # Clean up
        if os.path.exists(test_path):
            os.remove(test_path)


class TestBlacklistIntegration(unittest.TestCase):
    """Test blacklist integration with EUYSTACIO core."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_blacklist_path = "test_integration_blacklist.json"
        if os.path.exists(self.test_blacklist_path):
            os.remove(self.test_blacklist_path)
        self.blacklist = EuystacioBlacklist(self.test_blacklist_path)
    
    def tearDown(self):
        """Clean up."""
        if os.path.exists(self.test_blacklist_path):
            os.remove(self.test_blacklist_path)
    
    def test_multiple_entity_types(self):
        """Test handling multiple entity types."""
        test_entities = [
            ("192.168.1.1", "ip_address", "DDoS", "critical"),
            ("malicious_bot_v2", "ai_agent", "Data theft", "critical"),
            ("node_xyz_999", "node_id", "Unauthorized", "high"),
            ("upstream_ip_threat", "upstream_ip", "Known threat", "high"),
        ]
        
        for entity_id, entity_type, reason, severity in test_entities:
            self.blacklist.add_entity(entity_id, entity_type, reason, severity)
        
        self.assertEqual(len(self.blacklist.list_blocked_entities()), 4)
        
        # Test filtering by type
        ai_agents = self.blacklist.list_blocked_entities(entity_type="ai_agent")
        self.assertEqual(len(ai_agents), 1)
        self.assertEqual(ai_agents[0]['entity_id'], "malicious_bot_v2")


def run_tests():
    """Run all blacklist tests."""
    print("\n=== EUYSTACIO Blacklist System Tests ===\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestEuystacioBlacklist))
    suite.addTests(loader.loadTestsFromTestCase(TestBlacklistIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
