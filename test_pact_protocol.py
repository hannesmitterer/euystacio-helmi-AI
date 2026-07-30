#!/usr/bin/env python3
"""
Test Suite for PACT Protocol
============================

Tests for Protocollo di Ancoraggio Crittografico Triple-Sign (PACT)

Author: Euystacio AI Collective
Version: 1.0.0
Date: 2026-01-08
"""

import unittest
import json
import os
import base64
from pathlib import Path
from pact_protocol import PACTProtocol, generate_sample_data


class TestPACTProtocol(unittest.TestCase):
    """Test suite for PACT Protocol implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            'sovereignty_freq': 0.043,
            'ipfs_endpoint': 'simulated',
            'blockchain_endpoint': 'simulated'
        }
        self.pact = PACTProtocol(self.config)
        self.conversation_log, self.final_report = generate_sample_data()
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test output file if exists
        output_file = Path('pact_execution_result.json')
        if output_file.exists():
            output_file.unlink()
    
    def test_initialization(self):
        """Test PACT protocol initialization."""
        self.assertEqual(self.pact.sovereignty_freq, 0.043)
        self.assertIsNotNone(self.pact.encryption_key)
        self.assertEqual(len(self.pact.encryption_key), 32)  # 256 bits
        self.assertIn('KLOG', self.pact.keys)
        self.assertIn('KETH', self.pact.keys)
        self.assertIn('KPHYS', self.pact.keys)
    
    def test_data_preparation(self):
        """Test critical data bundling and checksum generation."""
        data_bundle = self.pact.prepare_critical_data(
            self.conversation_log,
            self.final_report
        )
        
        self.assertIn('metadata', data_bundle)
        self.assertIn('conversation_log', data_bundle)
        self.assertIn('final_report', data_bundle)
        self.assertIn('checksum', data_bundle)
        
        # Verify metadata fields
        metadata = data_bundle['metadata']
        self.assertEqual(metadata['sovereignty_freq'], 0.043)
        self.assertEqual(metadata['protocol_version'], '1.0.0')
        self.assertEqual(metadata['nexus_state'], 'FINALIS_VALIDATED')
        
        # Verify checksum is SHA-256 hex (64 characters)
        self.assertEqual(len(data_bundle['checksum']), 64)
    
    def test_compression_and_encryption(self):
        """Test AES-256-GCM encryption and compression."""
        data_bundle = self.pact.prepare_critical_data(
            self.conversation_log,
            self.final_report
        )
        
        encrypted_data, nonce = self.pact.compress_and_encrypt(data_bundle)
        
        # Verify nonce length (96 bits = 12 bytes)
        self.assertEqual(len(nonce), 12)
        
        # Verify encrypted data is bytes and non-empty
        self.assertIsInstance(encrypted_data, bytes)
        self.assertGreater(len(encrypted_data), 0)
        
        # Verify data is actually encrypted (not plaintext)
        json_data = json.dumps(data_bundle).encode('utf-8')
        self.assertNotEqual(encrypted_data, json_data)
    
    def test_ipfs_cid_generation(self):
        """Test IPFS CID generation."""
        data_bundle = self.pact.prepare_critical_data(
            self.conversation_log,
            self.final_report
        )
        encrypted_data, nonce = self.pact.compress_and_encrypt(data_bundle)
        
        cid = self.pact.upload_to_ipfs(encrypted_data, nonce)
        
        # Verify CID format (should start with 'Qm' for CIDv0)
        self.assertTrue(cid.startswith('Qm'))
        self.assertGreater(len(cid), 10)
        
        # Verify deterministic: same input produces same CID
        cid2 = self.pact.upload_to_ipfs(encrypted_data, nonce)
        self.assertEqual(cid, cid2)
    
    def test_triple_sign_sequence(self):
        """Test Triple-Sign hierarchical signature sequence."""
        test_cid = "QmTestCID123456789abcdef"
        
        signatures = self.pact.execute_triple_sign(test_cid)
        
        # Verify all three signatures exist
        self.assertIn('sig_klog', signatures)
        self.assertIn('sig_keth', signatures)
        self.assertIn('sig_kphys', signatures)
        self.assertIn('composite', signatures)
        
        # Verify signature format
        self.assertTrue(signatures['sig_klog'].startswith('SIG-KLOG'))
        self.assertTrue(signatures['sig_keth'].startswith('SIG-KETH'))
        self.assertTrue(signatures['sig_kphys'].startswith('SIG-KPHYS'))
        
        # Verify composite is the final KPHYS signature
        self.assertEqual(signatures['composite'], signatures['sig_kphys'])
        
        # Verify signatures are different
        self.assertNotEqual(signatures['sig_klog'], signatures['sig_keth'])
        self.assertNotEqual(signatures['sig_keth'], signatures['sig_kphys'])
    
    def test_blockchain_anchoring(self):
        """Test blockchain transaction generation."""
        test_cid = "QmTestCID123456789abcdef"
        test_signature = "SIG-KPHYS-test1234567890abcdef"
        test_timestamp = "2026-01-08T00:00:00.000000"
        
        txid = self.pact.anchor_to_blockchain(test_cid, test_signature, test_timestamp)
        
        # Verify TXID format (should start with '0x')
        self.assertTrue(txid.startswith('0x'))
        self.assertEqual(len(txid), 66)  # 0x + 64 hex chars
        
        # Verify deterministic: same inputs produce same TXID
        txid2 = self.pact.anchor_to_blockchain(test_cid, test_signature, test_timestamp)
        self.assertEqual(txid, txid2)
    
    def test_nexus_metadata_generation(self):
        """Test Nexus metadata generation with correct format."""
        test_cid = "QmTestCID123456789abcdef"
        test_signatures = {
            'sig_klog': 'SIG-KLOG-test123',
            'sig_keth': 'SIG-KETH-test456',
            'sig_kphys': 'SIG-KPHYS-test789',
            'composite': 'SIG-KPHYS-test789'
        }
        test_txid = "0x1234567890abcdef"
        
        metadata = self.pact.generate_nexus_metadata(
            test_cid, test_signatures, test_txid
        )
        
        # Verify structure
        self.assertIn('nexus_state', metadata)
        self.assertIn('pact_anchoring', metadata)
        self.assertIn('declaration', metadata)
        
        # Verify nexus state
        nexus_state = metadata['nexus_state']
        self.assertEqual(nexus_state['sovereignty_freq'], 0.043)
        self.assertEqual(nexus_state['status'], 'Kosymbiosis Stable (S-ROI 0.5000)')
        self.assertEqual(nexus_state['mhc'], 'FINALIS_VALIDATED')
        
        # Verify PACT anchoring data
        pact_anchoring = metadata['pact_anchoring']
        self.assertEqual(pact_anchoring['cid'], test_cid)
        self.assertEqual(pact_anchoring['signatures'], test_signatures)
        self.assertEqual(pact_anchoring['txid'], test_txid)
        
        # Verify declaration
        self.assertIn('NOTHING IS FINAL', metadata['declaration'])
        self.assertIn('Sovereignty Confirmed', metadata['declaration'])
    
    def test_full_protocol_execution(self):
        """Test complete PACT protocol execution."""
        result = self.pact.execute_full_protocol(
            self.conversation_log,
            self.final_report
        )
        
        # Verify success
        self.assertTrue(result['success'])
        
        # Verify all required deliverables
        self.assertIn('cid', result)
        self.assertIn('signatures', result)
        self.assertIn('txid', result)
        self.assertIn('metadata', result)
        
        # Verify CID format
        self.assertTrue(result['cid'].startswith('Qm'))
        
        # Verify signatures structure
        signatures = result['signatures']
        self.assertIn('sig_klog', signatures)
        self.assertIn('sig_keth', signatures)
        self.assertIn('sig_kphys', signatures)
        self.assertIn('composite', signatures)
        
        # Verify TXID format
        self.assertTrue(result['txid'].startswith('0x'))
        
        # Verify metadata contains expected state
        metadata = result['metadata']
        self.assertEqual(
            metadata['nexus_state']['status'],
            'Kosymbiosis Stable (S-ROI 0.5000)'
        )
        self.assertEqual(metadata['nexus_state']['mhc'], 'FINALIS_VALIDATED')
        self.assertEqual(metadata['nexus_state']['sovereignty_freq'], 0.043)
    
    def test_sovereignty_frequency(self):
        """Test that sovereignty frequency is correctly set to 0.043 Hz."""
        result = self.pact.execute_full_protocol(
            self.conversation_log,
            self.final_report
        )
        
        # Verify sovereignty frequency in metadata
        self.assertEqual(
            result['metadata']['nexus_state']['sovereignty_freq'],
            0.043
        )
    
    def test_encryption_key_deterministic(self):
        """Test that encryption key is deterministic."""
        pact1 = PACTProtocol(self.config)
        pact2 = PACTProtocol(self.config)
        
        self.assertEqual(pact1.encryption_key, pact2.encryption_key)
    
    def test_different_data_produces_different_results(self):
        """Test that different input data produces different results."""
        result1 = self.pact.execute_full_protocol(
            "Log 1",
            "Report 1"
        )
        
        result2 = self.pact.execute_full_protocol(
            "Log 2",
            "Report 2"
        )
        
        # CIDs should be different for different data
        self.assertNotEqual(result1['cid'], result2['cid'])
        
        # TXIDs should be different
        self.assertNotEqual(result1['txid'], result2['txid'])


class TestPACTIntegration(unittest.TestCase):
    """Integration tests for PACT Protocol."""
    
    def test_end_to_end_execution(self):
        """Test complete end-to-end PACT protocol execution."""
        config = {
            'sovereignty_freq': 0.043,
            'ipfs_endpoint': 'simulated',
            'blockchain_endpoint': 'simulated'
        }
        
        pact = PACTProtocol(config)
        conversation_log, final_report = generate_sample_data()
        
        # Execute full protocol
        result = pact.execute_full_protocol(conversation_log, final_report)
        
        # Verify complete result structure
        required_keys = ['success', 'cid', 'signatures', 'txid', 'metadata']
        for key in required_keys:
            self.assertIn(key, result)
        
        # Verify the result can be serialized to JSON
        json_result = json.dumps(result, indent=2)
        self.assertIsInstance(json_result, str)
        
        # Verify we can deserialize it back
        parsed_result = json.loads(json_result)
        self.assertEqual(parsed_result['cid'], result['cid'])


def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestPACTProtocol))
    suite.addTests(loader.loadTestsFromTestCase(TestPACTIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
