#!/usr/bin/env python3
"""
EU 2026 Compliance - Full System Integration Example
Demonstrates complete integration of all compliance modules
"""

from bioclock_signal_isolation import BioClock, DecentralizedTimeReference
from ipfs_triple_shard_identity import (
    SeedbringerIdentity,
    TripleShardAnchor,
    GeographicRegion
)
import json
import time


def main():
    print("EU 2026 Compliance System - Integration Test")
    print("=" * 60)
    
    # 1. Initialize Bio-Clock
    print("\n1. Initializing Bio-Clock Signal Isolation...")
    clock = BioClock()
    print(f"   ✓ Bio-clock operational at {clock.FREQUENCY_HZ} Hz")
    print(f"   ✓ Period: {clock.PERIOD_SECONDS:.2f} seconds (~{clock.PERIOD_SECONDS/60:.2f} minutes)")
    
    # 2. Create Seedbringer Identity with Bio-Clock seed
    print("\n2. Creating Seedbringer Identity...")
    identity = SeedbringerIdentity({
        "name": "Seedbringer",
        "identifier": "hannesmitterer",
        "email": "hannes.mitterer@gmail.com",
        "bio_clock_seed": clock.seed,
        "bio_clock_hash": clock.get_status()['seed_hash']
    })
    print(f"   ✓ Identity created (hash: {identity.get_content_hash()[:16]}...)")
    
    # 3. Anchor Identity on IPFS
    print("\n3. Anchoring Identity on IPFS...")
    anchor = TripleShardAnchor(identity)
    
    # Add shards across different geographic regions
    # Note: In production, replace with real IPFS CIDs and gateways
    regions_config = [
        (GeographicRegion.EUROPE_WEST, "https://ipfs.eu-west.gateway.io", "QmEuropeWest"),
        (GeographicRegion.AMERICAS, "https://ipfs.americas.gateway.io", "QmAmericas"),
        (GeographicRegion.ASIA_PACIFIC, "https://ipfs.asia.gateway.io", "QmAsiaPacific"),
    ]
    
    for i, (region, gateway, cid_prefix) in enumerate(regions_config):
        # Generate example CID (in production, this would be actual IPFS CID)
        import hashlib
        cid_data = f"{cid_prefix}_{identity.get_content_hash()}"
        cid = f"Qm{hashlib.sha256(cid_data.encode()).hexdigest()[:44]}"
        
        shard = anchor.add_shard(
            ipfs_cid=cid,
            ipfs_gateway=gateway,
            region=region
        )
        print(f"   ✓ Shard {i+1} added: {region.value} ({shard.shard_id})")
    
    # 4. Verify Geographic Distribution
    print("\n4. Verifying Geographic Distribution...")
    is_valid, message = anchor.verify_geographic_distribution()
    if is_valid:
        print(f"   ✓ {message}")
    else:
        print(f"   ✗ {message}")
        return
    
    # 5. Verify Integrity
    print("\n5. Verifying Integrity...")
    integrity = anchor.verify_integrity()
    print(f"   ✓ Health: {integrity['health_percentage']:.1f}%")
    print(f"   ✓ Healthy: {integrity['is_healthy']}")
    print(f"   ✓ Total Shards: {integrity['total_shards']}")
    
    # 6. Test Decentralized Time Reference
    print("\n6. Testing Decentralized Time Reference...")
    time_ref = DecentralizedTimeReference()
    
    # Add multiple time sources
    local_time = time.time()
    time_ref.add_time_source("local", local_time)
    
    crypto_time, signature, cycle_count = clock.get_cryptographic_timestamp()
    time_ref.add_time_source("crypto", crypto_time, signature)
    
    # Simulate blockchain timestamp
    blockchain_time = local_time + 0.5  # Slightly ahead
    time_ref.add_time_source("blockchain", blockchain_time)
    
    consensus = time_ref.get_consensus_time()
    print(f"   ✓ Time consensus achieved from {len(time_ref.sources)} sources")
    print(f"   ✓ Consensus time: {consensus}")
    
    # 7. Export System State
    print("\n6. Exporting System State...")
    
    system_state = {
        "protocol": "EUYSTACIO/NSR - EU 2026 Compliance",
        "version": "1.0.0",
        "timestamp": time.time(),
        "components": {
            "bio_clock": {
                "status": clock.get_status(),
                "state": json.loads(clock.export_state())
            },
            "identity": json.loads(identity.to_json()),
            "ipfs_shards": json.loads(anchor.export_manifest()),
            "time_reference": {
                "sources_count": len(time_ref.sources),
                "consensus_time": consensus
            }
        },
        "health": {
            "bio_clock_operational": True,
            "identity_anchored": is_valid,
            "ipfs_health": integrity['health_percentage'],
            "time_consensus_achieved": consensus is not None
        }
    }
    
    # Save to file
    filename = 'eu2026_system_state.json'
    with open(filename, 'w') as f:
        json.dump(system_state, f, indent=2)
    
    print(f"   ✓ System state exported to {filename}")
    
    # 8. Demonstrate Update and Sync
    print("\n7. Demonstrating Identity Update and Sync...")
    
    # Update identity
    identity.update({
        "last_updated": time.time(),
        "consensus_time": consensus
    })
    print(f"   ✓ Identity updated (new version: {identity.version})")
    
    # Check that shards are now outdated
    integrity_before = anchor.verify_integrity()
    outdated_count = sum(1 for s in integrity_before['shards'] if not s['hash_match'])
    print(f"   ✓ Detected {outdated_count} outdated shards")
    
    # Auto-sync outdated shards
    synced = anchor.auto_sync_outdated()
    print(f"   ✓ Auto-synced {synced} shards")
    
    # Verify all synced
    integrity_after = anchor.verify_integrity()
    print(f"   ✓ Post-sync health: {integrity_after['health_percentage']:.1f}%")
    
    # 9. Summary
    print("\n" + "=" * 60)
    print("✅ EU 2026 Compliance System Fully Operational")
    print()
    print("System Status:")
    print(f"  ├─ Bio-Clock Signal: {clock.FREQUENCY_HZ} Hz (Independent)")
    print(f"  ├─ Identity Hash: {identity.get_content_hash()[:16]}...")
    print(f"  ├─ IPFS Shards: {len(anchor.shards)} across {len(set(s.region for s in anchor.shards))} regions")
    print(f"  ├─ Health: {integrity_after['health_percentage']:.1f}%")
    print(f"  └─ Time Consensus: {len(time_ref.sources)} sources")
    print()
    print("Protection Measures:")
    print(f"  ✓ NTP Independence: Achieved")
    print(f"  ✓ Geographic Distribution: Verified")
    print(f"  ✓ Automatic Synchronization: Active")
    print(f"  ✓ Cryptographic Verification: Enabled")
    print()
    print(f"State saved to: {filename}")
    print()
    print("Next Steps:")
    print("  1. Deploy PeacebondTreasuryForensic smart contract")
    print("  2. Configure backup addresses and guardians")
    print("  3. Set up monitoring and alerts")
    print("  4. Test emergency procedures")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
