"""
Tests for IPFS Triple-Shard Identity Anchoring Module
EU 2026 Compliance Testing
"""

import unittest
import time
import json
from ipfs_triple_shard_identity import (
    SeedbringerIdentity,
    TripleShardAnchor,
    IPFSShard,
    ShardStatus,
    GeographicRegion
)


class TestSeedbringerIdentity(unittest.TestCase):
    """Test cases for SeedbringerIdentity class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.identity = SeedbringerIdentity()
    
    def test_initialization(self):
        """Test identity initialization"""
        self.assertEqual(self.identity.version, 1)
        self.assertIn('name', self.identity.identity_data)
        self.assertEqual(self.identity.identity_data['name'], 'Seedbringer')
    
    def test_custom_identity_data(self):
        """Test initialization with custom data"""
        custom_data = {
            "name": "Test User",
            "identifier": "test123"
        }
        identity = SeedbringerIdentity(custom_data)
        
        self.assertEqual(identity.identity_data['name'], 'Test User')
        self.assertEqual(identity.identity_data['identifier'], 'test123')
    
    def test_update(self):
        """Test identity updates"""
        initial_version = self.identity.version
        
        self.identity.update({'email': 'new@example.com'})
        
        self.assertEqual(self.identity.identity_data['email'], 'new@example.com')
        self.assertEqual(self.identity.version, initial_version + 1)
    
    def test_to_json(self):
        """Test JSON export"""
        json_str = self.identity.to_json()
        
        self.assertIsInstance(json_str, str)
        data = json.loads(json_str)
        
        self.assertIn('version', data)
        self.assertIn('identity', data)
    
    def test_content_hash(self):
        """Test content hash generation"""
        hash1 = self.identity.get_content_hash()
        
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 64)  # SHA256 hex
        
        # Hash should be consistent
        hash2 = self.identity.get_content_hash()
        self.assertEqual(hash1, hash2)
        
        # Hash should change after update
        self.identity.update({'test': 'value'})
        hash3 = self.identity.get_content_hash()
        self.assertNotEqual(hash1, hash3)


class TestTripleShardAnchor(unittest.TestCase):
    """Test cases for TripleShardAnchor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.identity = SeedbringerIdentity()
        self.anchor = TripleShardAnchor(self.identity)
    
    def test_initialization(self):
        """Test anchor initialization"""
        self.assertEqual(len(self.anchor.shards), 0)
        self.assertEqual(self.anchor.MIN_SHARDS, 3)
        self.assertEqual(self.anchor.MIN_REGIONS, 2)
    
    def test_add_shard(self):
        """Test adding a shard"""
        shard = self.anchor.add_shard(
            ipfs_cid="QmTest123",
            ipfs_gateway="https://ipfs.io",
            region=GeographicRegion.EUROPE_WEST
        )
        
        self.assertEqual(len(self.anchor.shards), 1)
        self.assertEqual(shard.ipfs_cid, "QmTest123")
        self.assertEqual(shard.region, GeographicRegion.EUROPE_WEST)
        self.assertEqual(shard.status, ShardStatus.ACTIVE)
    
    def test_remove_shard(self):
        """Test removing a shard"""
        shard = self.anchor.add_shard(
            ipfs_cid="QmTest123",
            ipfs_gateway="https://ipfs.io",
            region=GeographicRegion.EUROPE_WEST
        )
        
        self.assertTrue(self.anchor.remove_shard(shard.shard_id))
        self.assertEqual(len(self.anchor.shards), 0)
        
        # Removing non-existent shard should return False
        self.assertFalse(self.anchor.remove_shard("nonexistent"))
    
    def test_geographic_distribution_insufficient_shards(self):
        """Test geographic distribution with insufficient shards"""
        # Add only 1 shard
        self.anchor.add_shard(
            ipfs_cid="QmTest1",
            ipfs_gateway="https://ipfs1.io",
            region=GeographicRegion.EUROPE_WEST
        )
        
        is_valid, message = self.anchor.verify_geographic_distribution()
        self.assertFalse(is_valid)
        self.assertIn("Insufficient shards", message)
    
    def test_geographic_distribution_insufficient_regions(self):
        """Test geographic distribution with insufficient regions"""
        # Add 3 shards in same region
        for i in range(3):
            self.anchor.add_shard(
                ipfs_cid=f"QmTest{i}",
                ipfs_gateway=f"https://ipfs{i}.io",
                region=GeographicRegion.EUROPE_WEST
            )
        
        is_valid, message = self.anchor.verify_geographic_distribution()
        self.assertFalse(is_valid)
        self.assertIn("regional distribution", message)
    
    def test_geographic_distribution_valid(self):
        """Test valid geographic distribution"""
        # Add 3 shards in different regions
        regions = [
            GeographicRegion.EUROPE_WEST,
            GeographicRegion.AMERICAS,
            GeographicRegion.ASIA_PACIFIC
        ]
        
        for i, region in enumerate(regions):
            self.anchor.add_shard(
                ipfs_cid=f"QmTest{i}",
                ipfs_gateway=f"https://ipfs{i}.io",
                region=region
            )
        
        is_valid, message = self.anchor.verify_geographic_distribution()
        self.assertTrue(is_valid)
        self.assertIn("verified", message)
    
    def test_verify_integrity(self):
        """Test integrity verification"""
        # Add shards
        for i in range(3):
            self.anchor.add_shard(
                ipfs_cid=f"QmTest{i}",
                ipfs_gateway=f"https://ipfs{i}.io",
                region=GeographicRegion.EUROPE_WEST
            )
        
        results = self.anchor.verify_integrity()
        
        self.assertIn('timestamp', results)
        self.assertIn('current_hash', results)
        self.assertIn('shards', results)
        self.assertEqual(len(results['shards']), 3)
        self.assertTrue(results['is_healthy'])
    
    def test_sync_shard(self):
        """Test shard synchronization"""
        shard = self.anchor.add_shard(
            ipfs_cid="QmTest123",
            ipfs_gateway="https://ipfs.io",
            region=GeographicRegion.EUROPE_WEST
        )
        
        # Mark shard as outdated
        shard.status = ShardStatus.OUTDATED
        
        # Sync shard
        success = self.anchor.sync_shard(shard.shard_id)
        
        self.assertTrue(success)
        self.assertEqual(shard.status, ShardStatus.ACTIVE)
    
    def test_sync_all_shards(self):
        """Test synchronizing all shards"""
        # Add 3 shards
        for i in range(3):
            self.anchor.add_shard(
                ipfs_cid=f"QmTest{i}",
                ipfs_gateway=f"https://ipfs{i}.io",
                region=GeographicRegion.EUROPE_WEST
            )
        
        results = self.anchor.sync_all_shards()
        
        self.assertEqual(results['total_shards'], 3)
        self.assertEqual(results['synced'], 3)
        self.assertEqual(results['failed'], 0)
    
    def test_auto_sync_outdated(self):
        """Test automatic sync of outdated shards"""
        # Add shards
        shard1 = self.anchor.add_shard(
            ipfs_cid="QmTest1",
            ipfs_gateway="https://ipfs1.io",
            region=GeographicRegion.EUROPE_WEST
        )
        
        shard2 = self.anchor.add_shard(
            ipfs_cid="QmTest2",
            ipfs_gateway="https://ipfs2.io",
            region=GeographicRegion.AMERICAS
        )
        
        # Mark one as outdated
        shard1.status = ShardStatus.OUTDATED
        
        synced_count = self.anchor.auto_sync_outdated()
        
        self.assertEqual(synced_count, 1)
        self.assertEqual(shard1.status, ShardStatus.ACTIVE)
        self.assertEqual(shard2.status, ShardStatus.ACTIVE)
    
    def test_get_status(self):
        """Test status retrieval"""
        # Add shards in different regions
        regions = [
            GeographicRegion.EUROPE_WEST,
            GeographicRegion.AMERICAS,
            GeographicRegion.ASIA_PACIFIC
        ]
        
        for i, region in enumerate(regions):
            self.anchor.add_shard(
                ipfs_cid=f"QmTest{i}",
                ipfs_gateway=f"https://ipfs{i}.io",
                region=region
            )
        
        status = self.anchor.get_status()
        
        self.assertIn('identity_version', status)
        self.assertIn('identity_hash', status)
        self.assertIn('total_shards', status)
        self.assertIn('geographic_distribution', status)
        self.assertEqual(status['total_shards'], 3)
        self.assertTrue(status['geographic_distribution']['is_valid'])
    
    def test_export_manifest(self):
        """Test manifest export"""
        # Add shards
        for i in range(3):
            self.anchor.add_shard(
                ipfs_cid=f"QmTest{i}",
                ipfs_gateway=f"https://ipfs{i}.io",
                region=GeographicRegion.EUROPE_WEST
            )
        
        manifest_json = self.anchor.export_manifest()
        
        self.assertIsInstance(manifest_json, str)
        manifest = json.loads(manifest_json)
        
        self.assertIn('protocol', manifest)
        self.assertIn('identity', manifest)
        self.assertIn('shards', manifest)
        self.assertEqual(len(manifest['shards']), 3)


class TestIntegration(unittest.TestCase):
    """Integration tests for identity anchoring"""
    
    def test_full_workflow(self):
        """Test complete workflow from creation to verification"""
        # Create identity
        identity = SeedbringerIdentity({
            "name": "Seedbringer",
            "identifier": "hannesmitterer",
            "email": "hannes.mitterer@gmail.com"
        })
        
        # Create anchor
        anchor = TripleShardAnchor(identity)
        
        # Add shards across regions
        anchor.add_shard(
            "QmEuropeWest",
            "https://eu-west.ipfs.io",
            GeographicRegion.EUROPE_WEST
        )
        anchor.add_shard(
            "QmAmericas",
            "https://americas.ipfs.io",
            GeographicRegion.AMERICAS
        )
        anchor.add_shard(
            "QmAsiaPacific",
            "https://asia.ipfs.io",
            GeographicRegion.ASIA_PACIFIC
        )
        
        # Verify distribution
        is_valid, message = anchor.verify_geographic_distribution()
        self.assertTrue(is_valid)
        
        # Verify integrity
        integrity = anchor.verify_integrity()
        self.assertTrue(integrity['is_healthy'])
        
        # Update identity
        identity.update({"pgp_fingerprint": "ABC123"})
        
        # Verify that shards are now outdated
        integrity = anchor.verify_integrity()
        outdated_count = sum(1 for s in integrity['shards'] if not s['hash_match'])
        self.assertEqual(outdated_count, 3)
        
        # Auto-sync
        synced = anchor.auto_sync_outdated()
        self.assertEqual(synced, 3)
        
        # Verify all synced
        integrity = anchor.verify_integrity()
        self.assertTrue(integrity['is_healthy'])
    
    def test_disaster_recovery(self):
        """Test disaster recovery scenario"""
        identity = SeedbringerIdentity()
        anchor = TripleShardAnchor(identity)
        
        # Add 5 shards for redundancy
        regions = [
            GeographicRegion.EUROPE_WEST,
            GeographicRegion.EUROPE_EAST,
            GeographicRegion.AMERICAS,
            GeographicRegion.ASIA_PACIFIC,
            GeographicRegion.AFRICA
        ]
        
        for i, region in enumerate(regions):
            anchor.add_shard(
                f"QmShard{i}",
                f"https://ipfs{i}.io",
                region
            )
        
        # Simulate 2 shards failing
        anchor.shards[0].status = ShardStatus.FAILED
        anchor.shards[1].status = ShardStatus.FAILED
        
        # Should still have enough active shards
        is_valid, _ = anchor.verify_geographic_distribution()
        self.assertTrue(is_valid)
        
        # Export manifest for recovery
        manifest = anchor.export_manifest()
        self.assertIsNotNone(manifest)


if __name__ == '__main__':
    print("Running IPFS Triple-Shard Identity Anchoring Tests")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)
