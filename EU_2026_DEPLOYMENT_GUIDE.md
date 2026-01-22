# EU 2026 Compliance - Deployment and Configuration Guide

## Quick Reference

This guide provides step-by-step instructions for deploying and configuring the EU 2026 compliance modules.

---

## Prerequisites

### For Python Modules

```bash
# Python 3.8 or higher
python --version

# No additional dependencies required for bio-clock and IPFS modules
# (Uses only Python standard library)
```

### For Solidity Smart Contract

```bash
# Node.js and npm
node --version  # v18+ recommended
npm --version

# Install dependencies
npm install
```

---

## Module 1: Bio-Clock Signal Isolation

### Installation

The bio-clock module is ready to use immediately:

```bash
# Test the module
python test_bioclock_signal_isolation.py

# Expected output: 18 tests passing
```

### Basic Usage

```python
from bioclock_signal_isolation import BioClock, DecentralizedTimeReference

# Initialize bio-clock
clock = BioClock()

# Get status
status = clock.get_status()
print(f"Operating at {status['frequency_hz']} Hz")

# Generate cryptographic timestamp
timestamp, signature = clock.get_cryptographic_timestamp()

# Verify timestamp
is_valid = clock.verify_timestamp(timestamp, signature)
```

### Configuration Options

```python
# Custom seed for deterministic behavior
clock = BioClock(seed="your_custom_seed_here")

# Export state for backup
state_json = clock.export_state()
with open('bioclock_backup.json', 'w') as f:
    f.write(state_json)

# Import state for recovery
new_clock = BioClock()
with open('bioclock_backup.json', 'r') as f:
    new_clock.import_state(f.read())
```

---

## Module 2: IPFS Triple-Shard Identity

### Installation

The IPFS module is ready to use immediately:

```bash
# Test the module
python test_ipfs_triple_shard_identity.py

# Expected output: 19 tests passing
```

### Basic Usage

```python
from ipfs_triple_shard_identity import (
    SeedbringerIdentity,
    TripleShardAnchor,
    GeographicRegion
)

# Create identity
identity = SeedbringerIdentity({
    "name": "Seedbringer",
    "identifier": "hannesmitterer",
    "email": "hannes.mitterer@gmail.com"
})

# Initialize anchor
anchor = TripleShardAnchor(identity)

# Add IPFS shards across regions
anchor.add_shard(
    ipfs_cid="QmYourIPFSCID",
    ipfs_gateway="https://ipfs.gateway.io",
    region=GeographicRegion.EUROPE_WEST
)

# Verify distribution
is_valid, message = anchor.verify_geographic_distribution()
print(f"Distribution valid: {is_valid}")

# Sync all shards
results = anchor.sync_all_shards()
print(f"Synced {results['synced']}/{results['total_shards']} shards")
```

### IPFS Gateway Configuration

You'll need to configure IPFS gateways for each region:

```python
# Example gateways (replace with your actual IPFS nodes)
GATEWAYS = {
    "EUROPE_WEST": "https://ipfs.eu-west.example.io",
    "AMERICAS": "https://ipfs.americas.example.io",
    "ASIA_PACIFIC": "https://ipfs.asia.example.io",
}
```

---

## Module 3: Peacebond Treasury Forensic

### Installation

```bash
# Navigate to project directory
cd /home/runner/work/euystacio-helmi-AI/euystacio-helmi-AI

# Install dependencies (if not already installed)
npm install

# Compile contract
npx hardhat compile
```

### Configuration

Create or update `.env` file:

```bash
# Resonance Credits Token Address
RESONANCE_CREDITS_TOKEN=0xYourTokenAddress

# Detection threshold (number of failed transactions)
BLOCK_DETECTION_THRESHOLD=5

# Number of guardian approvals required
REQUIRED_GUARDIAN_APPROVALS=2

# Backup addresses (minimum 3 required)
BACKUP_ADDRESS_1=0xBackupAddress1
BACKUP_ADDRESS_2=0xBackupAddress2
BACKUP_ADDRESS_3=0xBackupAddress3

# Guardian addresses
GUARDIAN_1=0xGuardianAddress1
GUARDIAN_2=0xGuardianAddress2
GUARDIAN_3=0xGuardianAddress3

# Network configuration (example for Polygon)
POLYGON_RPC_URL=https://polygon-rpc.com
PRIVATE_KEY=your_private_key_here
```

### Deployment

```bash
# Test the contract
npx hardhat test test/PeacebondTreasuryForensic.test.js

# Deploy to local network (for testing)
npx hardhat run scripts/deploy_peacebond_forensic.js --network localhost

# Deploy to testnet
npx hardhat run scripts/deploy_peacebond_forensic.js --network mumbai

# Deploy to mainnet (CAREFUL!)
npx hardhat run scripts/deploy_peacebond_forensic.js --network polygon
```

### Post-Deployment Configuration

After deployment, configure the contract:

```javascript
// Using ethers.js
const contract = await ethers.getContractAt(
    "PeacebondTreasuryForensic",
    "0xDeployedContractAddress"
);

// Add backup addresses
await contract.addBackupAddress("0xBackupAddress1");
await contract.addBackupAddress("0xBackupAddress2");
await contract.addBackupAddress("0xBackupAddress3");

// Add guardians
await contract.addGuardian("0xGuardianAddress1");
await contract.addGuardian("0xGuardianAddress2");

// Verify configuration
const status = await contract.getStatus();
console.log("Configuration:", status);
```

---

## Integration Example

### Full System Integration

```python
#!/usr/bin/env python3
"""
EU 2026 Compliance - Full System Integration Example
"""

from bioclock_signal_isolation import BioClock, DecentralizedTimeReference
from ipfs_triple_shard_identity import SeedbringerIdentity, TripleShardAnchor, GeographicRegion
import json
import time

def main():
    print("EU 2026 Compliance System - Integration Test")
    print("=" * 60)
    
    # 1. Initialize Bio-Clock
    print("\n1. Initializing Bio-Clock Signal Isolation...")
    clock = BioClock()
    print(f"   ✓ Bio-clock operational at {clock.FREQUENCY_HZ} Hz")
    
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
    
    # Add shards (replace with real IPFS CIDs and gateways)
    regions = [
        (GeographicRegion.EUROPE_WEST, "https://ipfs.eu-west.gateway.io"),
        (GeographicRegion.AMERICAS, "https://ipfs.americas.gateway.io"),
        (GeographicRegion.ASIA_PACIFIC, "https://ipfs.asia.gateway.io"),
    ]
    
    for i, (region, gateway) in enumerate(regions):
        shard = anchor.add_shard(
            ipfs_cid=f"QmExample{i}",  # Replace with real CID
            ipfs_gateway=gateway,
            region=region
        )
        print(f"   ✓ Shard {i+1} added: {region.value}")
    
    # 4. Verify Geographic Distribution
    print("\n4. Verifying Geographic Distribution...")
    is_valid, message = anchor.verify_geographic_distribution()
    print(f"   {'✓' if is_valid else '✗'} {message}")
    
    # 5. Verify Integrity
    print("\n5. Verifying Integrity...")
    integrity = anchor.verify_integrity()
    print(f"   ✓ Health: {integrity['health_percentage']:.1f}%")
    
    # 6. Export System State
    print("\n6. Exporting System State...")
    
    system_state = {
        "protocol": "EUYSTACIO/NSR - EU 2026 Compliance",
        "timestamp": time.time(),
        "bio_clock": clock.get_status(),
        "identity": json.loads(identity.to_json()),
        "ipfs_shards": json.loads(anchor.export_manifest())
    }
    
    with open('eu2026_system_state.json', 'w') as f:
        json.dump(system_state, f, indent=2)
    
    print("   ✓ System state exported to eu2026_system_state.json")
    
    # 7. Summary
    print("\n" + "=" * 60)
    print("✅ EU 2026 Compliance System Fully Operational")
    print(f"   - Bio-Clock: {clock.FREQUENCY_HZ} Hz")
    print(f"   - Identity Hash: {identity.get_content_hash()[:16]}...")
    print(f"   - IPFS Shards: {len(anchor.shards)} across {len(set(s.region for s in anchor.shards))} regions")
    print(f"   - Health: {integrity['health_percentage']:.1f}%")

if __name__ == "__main__":
    main()
```

Save this as `eu2026_integration_test.py` and run:

```bash
python eu2026_integration_test.py
```

---

## Monitoring and Maintenance

### Daily Health Check Script

```python
#!/usr/bin/env python3
"""Daily health check for EU 2026 compliance systems"""

from bioclock_signal_isolation import BioClock
from ipfs_triple_shard_identity import TripleShardAnchor
import json

def check_health():
    # Load state
    with open('eu2026_system_state.json', 'r') as f:
        state = json.load(f)
    
    # Check bio-clock
    clock = BioClock()
    clock.import_state(json.dumps(state['bio_clock']))
    
    print("Bio-Clock Status:")
    print(f"  Uptime: {clock.get_status()['uptime_seconds']/3600:.1f} hours")
    print(f"  Drift: {clock.drift_compensation:.3f}s")
    
    # Check IPFS shards (requires recreation)
    # Add implementation to check shard health
    
    print("\n✅ Daily health check complete")

if __name__ == "__main__":
    check_health()
```

---

## Troubleshooting

### Bio-Clock Issues

**Problem:** Clock drift detected

**Solution:**
```python
# Add multiple time sources
time_ref = DecentralizedTimeReference()
time_ref.add_time_source("local", time.time())
time_ref.add_time_source("crypto", crypto_timestamp)

# Get consensus and compensate
consensus = time_ref.get_consensus_time()
clock.compensate_drift(consensus)
```

### IPFS Shard Issues

**Problem:** Shard sync failures

**Solution:**
```python
# Check integrity
integrity = anchor.verify_integrity()

# Auto-sync outdated shards
synced = anchor.auto_sync_outdated()
print(f"Synced {synced} outdated shards")

# If still failing, add new shard
anchor.add_shard(new_cid, new_gateway, new_region)
```

### Smart Contract Issues

**Problem:** Forensic switch won't activate

**Solution:**
```javascript
// Check status
const status = await contract.getStatus();
console.log("Current Approvals:", status.approvalCount);
console.log("Required:", await contract.requiredGuardianApprovals());

// Grant additional approvals
await contract.connect(guardian).grantForensicApproval();
```

---

## Security Best Practices

1. **Bio-Clock Seed Protection**
   - Store seed securely (encrypted)
   - Never commit seed to version control
   - Use hardware security module (HSM) if available

2. **IPFS Gateway Security**
   - Use HTTPS for all gateways
   - Verify TLS certificates
   - Monitor gateway availability

3. **Smart Contract Security**
   - Use multi-signature for guardian accounts
   - Regularly audit guardian access
   - Test forensic switch activation in testnet first

4. **Backup Strategy**
   - Daily state exports
   - Geographic distribution of backups
   - Encrypted storage

---

## Support and Resources

- **Documentation:** [EU_2026_COMPLIANCE_GUIDE.md](EU_2026_COMPLIANCE_GUIDE.md)
- **Emergency Contact:** hannes.mitterer@gmail.com
- **Telegram Channel:** @euystacio_nsr_alerts
- **Protocol Version:** 1.0.0

---

**Last Updated:** 2026-01-20  
**Status:** ACTIVE - Monitoraggio Attivo
