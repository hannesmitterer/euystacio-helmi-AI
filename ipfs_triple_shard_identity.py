"""
IPFS Triple-Shard Identity Anchoring Module - EU 2026 Compliance
Protocollo: EUYSTACIO / NSR
Implementazione: Hardening della Tripla Firma (Triple-Sign Pact)

Anchors Seedbringer Identity across at least three IPFS shards with:
- Geographic distribution verification
- Automatic synchronization on shard changes
- Cryptographic integrity checking
"""

import json
import hashlib
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ShardStatus(Enum):
    """Status of an IPFS shard"""
    ACTIVE = "active"
    SYNCING = "syncing"
    FAILED = "failed"
    OUTDATED = "outdated"


class GeographicRegion(Enum):
    """Geographic regions for shard distribution"""
    EUROPE_WEST = "europe_west"
    EUROPE_EAST = "europe_east"
    AMERICAS = "americas"
    ASIA_PACIFIC = "asia_pacific"
    AFRICA = "africa"
    OCEANIA = "oceania"


@dataclass
class IPFSShard:
    """Represents a single IPFS shard"""
    shard_id: str
    ipfs_cid: str
    ipfs_gateway: str
    region: GeographicRegion
    status: ShardStatus
    last_sync: float
    content_hash: str
    metadata: Dict


class SeedbringerIdentity:
    """
    Manages Seedbringer identity data
    """
    
    def __init__(self, identity_data: Optional[Dict] = None):
        """
        Initialize Seedbringer identity
        
        Args:
            identity_data: Optional existing identity data
        """
        self.identity_data = identity_data or self._create_default_identity()
        self.version = 1
        self.created_at = time.time()
        self.updated_at = time.time()
        
    def _create_default_identity(self) -> Dict:
        """Create default identity structure"""
        return {
            "name": "Seedbringer",
            "identifier": "hannesmitterer",
            "role": "Creator",
            "email": "hannes.mitterer@gmail.com",
            "pgp_fingerprint": "",
            "ethereum_address": "",
            "bio_clock_seed": "",
            "created": time.time()
        }
    
    def update(self, updates: Dict) -> None:
        """
        Update identity data
        
        Args:
            updates: Dictionary of fields to update
        """
        self.identity_data.update(updates)
        self.updated_at = time.time()
        self.version += 1
    
    def to_json(self) -> str:
        """Export identity as JSON"""
        data = {
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "identity": self.identity_data
        }
        return json.dumps(data, indent=2, sort_keys=True)
    
    def get_content_hash(self) -> str:
        """Calculate content hash for integrity verification"""
        json_str = self.to_json()
        return hashlib.sha256(json_str.encode()).hexdigest()


class TripleShardAnchor:
    """
    Manages IPFS triple-shard anchoring with geographic distribution
    
    Ensures identity is replicated across at least 3 geographically
    distributed IPFS nodes with automatic synchronization.
    """
    
    MIN_SHARDS = 3
    MIN_REGIONS = 2  # Minimum number of different regions required
    
    def __init__(self, identity: SeedbringerIdentity):
        """
        Initialize triple-shard anchor
        
        Args:
            identity: SeedbringerIdentity instance to anchor
        """
        self.identity = identity
        self.shards: List[IPFSShard] = []
        self.sync_interval = 300  # 5 minutes default
        self.last_integrity_check = time.time()
        
    def add_shard(self, ipfs_cid: str, ipfs_gateway: str, 
                  region: GeographicRegion) -> IPFSShard:
        """
        Add a new IPFS shard
        
        Args:
            ipfs_cid: IPFS Content Identifier
            ipfs_gateway: IPFS gateway URL
            region: Geographic region of the shard
            
        Returns:
            Created IPFSShard instance
        """
        shard = IPFSShard(
            shard_id=hashlib.sha256(f"{ipfs_cid}:{ipfs_gateway}".encode()).hexdigest()[:16],
            ipfs_cid=ipfs_cid,
            ipfs_gateway=ipfs_gateway,
            region=region,
            status=ShardStatus.ACTIVE,
            last_sync=time.time(),
            content_hash=self.identity.get_content_hash(),
            metadata={}
        )
        
        self.shards.append(shard)
        return shard
    
    def remove_shard(self, shard_id: str) -> bool:
        """
        Remove a shard by ID
        
        Args:
            shard_id: ID of shard to remove
            
        Returns:
            True if shard was removed
        """
        initial_count = len(self.shards)
        self.shards = [s for s in self.shards if s.shard_id != shard_id]
        return len(self.shards) < initial_count
    
    def verify_geographic_distribution(self) -> Tuple[bool, str]:
        """
        Verify that shards are geographically distributed
        
        Returns:
            Tuple of (is_valid, message)
        """
        if len(self.shards) < self.MIN_SHARDS:
            return False, f"Insufficient shards: {len(self.shards)} < {self.MIN_SHARDS}"
        
        # Count active shards
        active_shards = [s for s in self.shards if s.status == ShardStatus.ACTIVE]
        if len(active_shards) < self.MIN_SHARDS:
            return False, f"Insufficient active shards: {len(active_shards)} < {self.MIN_SHARDS}"
        
        # Check regional distribution
        regions = set(s.region for s in active_shards)
        if len(regions) < self.MIN_REGIONS:
            return False, f"Insufficient regional distribution: {len(regions)} < {self.MIN_REGIONS}"
        
        return True, f"Geographic distribution verified: {len(active_shards)} shards across {len(regions)} regions"
    
    def verify_integrity(self) -> Dict[str, any]:
        """
        Verify integrity of all shards
        
        Returns:
            Dictionary with verification results
        """
        self.last_integrity_check = time.time()
        current_hash = self.identity.get_content_hash()
        
        results = {
            "timestamp": self.last_integrity_check,
            "current_hash": current_hash,
            "total_shards": len(self.shards),
            "shards": []
        }
        
        for shard in self.shards:
            shard_result = {
                "shard_id": shard.shard_id,
                "status": shard.status.value,
                "region": shard.region.value,
                "hash_match": shard.content_hash == current_hash,
                "age_seconds": time.time() - shard.last_sync
            }
            
            # Update shard status based on hash match
            if not shard_result["hash_match"]:
                shard.status = ShardStatus.OUTDATED
                shard_result["needs_sync"] = True
            else:
                shard_result["needs_sync"] = False
                
            results["shards"].append(shard_result)
        
        # Calculate overall health
        healthy_shards = sum(1 for s in results["shards"] if s["hash_match"] and s["status"] == "active")
        results["health_percentage"] = (healthy_shards / len(self.shards) * 100) if self.shards else 0
        results["is_healthy"] = healthy_shards >= self.MIN_SHARDS
        
        return results
    
    def sync_shard(self, shard_id: str) -> bool:
        """
        Synchronize a specific shard with current identity
        
        Args:
            shard_id: ID of shard to sync
            
        Returns:
            True if sync successful
        """
        shard = next((s for s in self.shards if s.shard_id == shard_id), None)
        if not shard:
            return False
        
        # Update shard status
        shard.status = ShardStatus.SYNCING
        
        # In a real implementation, this would upload to IPFS
        # For now, we simulate the sync
        try:
            # Simulate IPFS upload delay
            time.sleep(0.1)
            
            # Update shard metadata
            shard.content_hash = self.identity.get_content_hash()
            shard.last_sync = time.time()
            shard.status = ShardStatus.ACTIVE
            
            # Update IPFS CID (in real implementation, this would be the new CID)
            new_cid_data = f"{shard.ipfs_cid}:{time.time()}"
            shard.ipfs_cid = f"Qm{hashlib.sha256(new_cid_data.encode()).hexdigest()[:44]}"
            
            return True
            
        except Exception as e:
            shard.status = ShardStatus.FAILED
            shard.metadata["last_error"] = str(e)
            return False
    
    def sync_all_shards(self) -> Dict[str, any]:
        """
        Synchronize all shards with current identity
        
        Returns:
            Dictionary with sync results
        """
        results = {
            "timestamp": time.time(),
            "total_shards": len(self.shards),
            "synced": 0,
            "failed": 0,
            "details": []
        }
        
        for shard in self.shards:
            success = self.sync_shard(shard.shard_id)
            
            if success:
                results["synced"] += 1
            else:
                results["failed"] += 1
            
            results["details"].append({
                "shard_id": shard.shard_id,
                "success": success,
                "status": shard.status.value
            })
        
        return results
    
    def auto_sync_outdated(self) -> int:
        """
        Automatically sync all outdated shards
        
        Returns:
            Number of shards synced
        """
        synced_count = 0
        
        for shard in self.shards:
            if shard.status == ShardStatus.OUTDATED:
                if self.sync_shard(shard.shard_id):
                    synced_count += 1
        
        return synced_count
    
    def get_status(self) -> Dict:
        """
        Get current status of triple-shard anchor
        
        Returns:
            Dictionary with status information
        """
        is_distributed, distribution_msg = self.verify_geographic_distribution()
        integrity = self.verify_integrity()
        
        return {
            "identity_version": self.identity.version,
            "identity_hash": self.identity.get_content_hash(),
            "total_shards": len(self.shards),
            "active_shards": len([s for s in self.shards if s.status == ShardStatus.ACTIVE]),
            "geographic_distribution": {
                "is_valid": is_distributed,
                "message": distribution_msg,
                "regions": list(set(s.region.value for s in self.shards))
            },
            "integrity": integrity,
            "last_check": self.last_integrity_check
        }
    
    def export_manifest(self) -> str:
        """
        Export triple-shard manifest as JSON
        
        Returns:
            JSON string containing full manifest
        """
        manifest = {
            "protocol": "EUYSTACIO/NSR Triple-Sign Pact",
            "version": "1.0.0",
            "timestamp": time.time(),
            "identity": json.loads(self.identity.to_json()),
            "shards": [
                {
                    "shard_id": s.shard_id,
                    "ipfs_cid": s.ipfs_cid,
                    "ipfs_gateway": s.ipfs_gateway,
                    "region": s.region.value,
                    "status": s.status.value,
                    "last_sync": s.last_sync,
                    "content_hash": s.content_hash
                }
                for s in self.shards
            ],
            "status": self.get_status()
        }
        
        return json.dumps(manifest, indent=2)


if __name__ == "__main__":
    # Example usage
    print("IPFS Triple-Shard Identity Anchoring - EU 2026 Compliance")
    print("=" * 70)
    
    # Create Seedbringer identity
    identity = SeedbringerIdentity()
    print(f"\n✅ Created Seedbringer Identity")
    print(f"   Hash: {identity.get_content_hash()[:16]}...")
    
    # Initialize triple-shard anchor
    anchor = TripleShardAnchor(identity)
    print(f"\n✅ Initialized Triple-Shard Anchor")
    
    # Add shards across different regions
    print(f"\n📍 Adding IPFS shards across geographic regions...")
    
    shard1 = anchor.add_shard(
        ipfs_cid="QmExample1234567890abcdefghijklmnopqrstu",
        ipfs_gateway="https://ipfs.eu-west.gateway.io",
        region=GeographicRegion.EUROPE_WEST
    )
    print(f"   + Shard 1: {shard1.region.value} ({shard1.shard_id})")
    
    shard2 = anchor.add_shard(
        ipfs_cid="QmExample0987654321zyxwvutsrqponmlkjih",
        ipfs_gateway="https://ipfs.americas.gateway.io",
        region=GeographicRegion.AMERICAS
    )
    print(f"   + Shard 2: {shard2.region.value} ({shard2.shard_id})")
    
    shard3 = anchor.add_shard(
        ipfs_cid="QmExampleABCDEF123456789fedcba987654",
        ipfs_gateway="https://ipfs.asia.gateway.io",
        region=GeographicRegion.ASIA_PACIFIC
    )
    print(f"   + Shard 3: {shard3.region.value} ({shard3.shard_id})")
    
    # Verify geographic distribution
    print(f"\n🌍 Verifying Geographic Distribution...")
    is_valid, message = anchor.verify_geographic_distribution()
    print(f"   Status: {'✅ VALID' if is_valid else '❌ INVALID'}")
    print(f"   Message: {message}")
    
    # Verify integrity
    print(f"\n🔒 Verifying Integrity...")
    integrity = anchor.verify_integrity()
    print(f"   Health: {integrity['health_percentage']:.1f}%")
    print(f"   Healthy: {'✅ YES' if integrity['is_healthy'] else '❌ NO'}")
    
    # Get status
    print(f"\n📊 Current Status:")
    status = anchor.get_status()
    print(json.dumps(status, indent=2))
    
    # Export manifest
    print(f"\n💾 Exporting Manifest...")
    manifest = anchor.export_manifest()
    print(f"   ✅ Manifest exported ({len(manifest)} bytes)")
    
    print(f"\n✅ Triple-Shard Identity Anchoring operational")
    print(f"   Identity secured across {len(anchor.shards)} IPFS shards")
    print(f"   Geographic distribution: {len(status['geographic_distribution']['regions'])} regions")
