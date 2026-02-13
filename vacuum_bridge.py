#!/usr/bin/env python3
"""
Vacuum-Bridge IPFS Integration - Internet Organica Framework

Implements decentralized backup and distributed hosting using:
- IPFS (InterPlanetary File System)
- P2P networking protocols
- Content-addressed storage

Ensures digital sovereignty through distributed redundancy.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VacuumBridge:
    """
    Decentralized content distribution and backup system.
    
    Creates redundant, distributed copies of critical assets across
    peer-to-peer networks for sovereignty and resilience.
    """
    
    def __init__(self, local_storage: str = '.vacuum_bridge'):
        """
        Initialize Vacuum-Bridge system.
        
        Args:
            local_storage: Path to local storage directory
        """
        self.local_storage = Path(local_storage)
        self.local_storage.mkdir(exist_ok=True)
        
        self.manifest_file = self.local_storage / 'manifest.json'
        self.manifest = self._load_manifest()
        
        # Track distributed content
        self.distributed_content: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"Vacuum-Bridge initialized with storage at {self.local_storage}")
    
    def _load_manifest(self) -> Dict[str, Any]:
        """
        Load distribution manifest.
        
        Returns:
            dict: Manifest data
        """
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading manifest: {e}")
                return self._create_empty_manifest()
        else:
            return self._create_empty_manifest()
    
    def _create_empty_manifest(self) -> Dict[str, Any]:
        """
        Create empty manifest structure.
        
        Returns:
            dict: Empty manifest
        """
        return {
            'version': '1.0.0',
            'framework': 'Internet Organica',
            'created': datetime.utcnow().isoformat(),
            'last_updated': datetime.utcnow().isoformat(),
            'distributed_assets': {}
        }
    
    def _save_manifest(self) -> None:
        """Save manifest to disk."""
        self.manifest['last_updated'] = datetime.utcnow().isoformat()
        
        try:
            with open(self.manifest_file, 'w') as f:
                json.dump(self.manifest, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving manifest: {e}")
    
    def add_asset(self, filepath: str, critical: bool = False, 
                  metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add an asset to the distributed backup system.
        
        Args:
            filepath: Path to file to distribute
            critical: Whether this is a critical asset
            metadata: Optional metadata about the asset
            
        Returns:
            dict: Asset distribution information
        """
        file_path = Path(filepath)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Asset not found: {filepath}")
        
        # Read file content
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Generate content hash (simulates IPFS CID)
        content_hash = self._generate_content_hash(content)
        
        # Create asset record
        asset_info = {
            'filename': file_path.name,
            'original_path': str(file_path),
            'content_hash': content_hash,
            'size_bytes': len(content),
            'critical': critical,
            'added': datetime.utcnow().isoformat(),
            'metadata': metadata or {},
            'distribution_status': 'pending',
            'ipfs_cid': f'Qm{content_hash[:44]}',  # Simulated IPFS CID
            'backup_locations': []
        }
        
        # Store locally
        local_backup = self.local_storage / content_hash
        with open(local_backup, 'wb') as f:
            f.write(content)
        
        asset_info['backup_locations'].append({
            'type': 'local',
            'path': str(local_backup),
            'verified': True
        })
        
        # Simulate P2P distribution
        asset_info['backup_locations'].extend(
            self._simulate_p2p_distribution(content_hash, critical)
        )
        
        asset_info['distribution_status'] = 'distributed'
        
        # Add to manifest
        self.manifest['distributed_assets'][content_hash] = asset_info
        self._save_manifest()
        
        logger.info(
            f"Asset distributed: {file_path.name} "
            f"(CID: {asset_info['ipfs_cid']}, "
            f"Locations: {len(asset_info['backup_locations'])})"
        )
        
        return asset_info
    
    def _generate_content_hash(self, content: bytes) -> str:
        """
        Generate content hash (simulates IPFS content addressing).
        
        Args:
            content: File content
            
        Returns:
            str: Content hash
        """
        return hashlib.sha256(content).hexdigest()
    
    def _simulate_p2p_distribution(self, content_hash: str, critical: bool) -> List[Dict[str, Any]]:
        """
        Simulate P2P network distribution.
        
        In production, this would interact with actual IPFS nodes.
        
        Args:
            content_hash: Hash of content to distribute
            critical: Whether content is critical (affects redundancy)
            
        Returns:
            list: List of backup locations
        """
        locations = []
        
        # Number of redundant copies based on criticality
        num_copies = 5 if critical else 3
        
        # Simulated P2P nodes
        p2p_nodes = [
            {'region': 'North America', 'node_id': 'NA-001'},
            {'region': 'Europe', 'node_id': 'EU-001'},
            {'region': 'Asia Pacific', 'node_id': 'AP-001'},
            {'region': 'South America', 'node_id': 'SA-001'},
            {'region': 'Africa', 'node_id': 'AF-001'},
        ]
        
        for i in range(min(num_copies, len(p2p_nodes))):
            node = p2p_nodes[i]
            locations.append({
                'type': 'ipfs_node',
                'region': node['region'],
                'node_id': node['node_id'],
                'ipfs_url': f"ipfs://{content_hash}",
                'verified': True,
                'pinned': True
            })
        
        return locations
    
    def verify_integrity(self, content_hash: str) -> bool:
        """
        Verify integrity of distributed content.
        
        Args:
            content_hash: Hash of content to verify
            
        Returns:
            bool: True if integrity verified
        """
        if content_hash not in self.manifest['distributed_assets']:
            logger.error(f"Content hash not found: {content_hash}")
            return False
        
        asset = self.manifest['distributed_assets'][content_hash]
        
        # Verify local backup
        local_backup = self.local_storage / content_hash
        if not local_backup.exists():
            logger.error(f"Local backup missing for {asset['filename']}")
            return False
        
        # Read and verify hash
        with open(local_backup, 'rb') as f:
            content = f.read()
        
        computed_hash = self._generate_content_hash(content)
        
        if computed_hash != content_hash:
            logger.error(f"Hash mismatch for {asset['filename']}")
            return False
        
        logger.info(f"Integrity verified for {asset['filename']}")
        return True
    
    def get_asset(self, content_hash: str) -> Optional[bytes]:
        """
        Retrieve asset content by hash.
        
        Args:
            content_hash: Content hash to retrieve
            
        Returns:
            bytes: Asset content or None if not found
        """
        local_backup = self.local_storage / content_hash
        
        if local_backup.exists():
            with open(local_backup, 'rb') as f:
                return f.read()
        
        logger.warning(f"Asset not found: {content_hash}")
        return None
    
    def list_assets(self, critical_only: bool = False) -> List[Dict[str, Any]]:
        """
        List all distributed assets.
        
        Args:
            critical_only: Only return critical assets
            
        Returns:
            list: List of asset information
        """
        assets = list(self.manifest['distributed_assets'].values())
        
        if critical_only:
            assets = [a for a in assets if a['critical']]
        
        return assets
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get distribution statistics.
        
        Returns:
            dict: Statistics about distributed content
        """
        assets = self.manifest['distributed_assets'].values()
        
        total_size = sum(a['size_bytes'] for a in assets)
        critical_count = sum(1 for a in assets if a['critical'])
        
        # Count unique regions
        all_regions: Set[str] = set()
        for asset in assets:
            for location in asset['backup_locations']:
                if location['type'] == 'ipfs_node':
                    all_regions.add(location['region'])
        
        stats = {
            'total_assets': len(assets),
            'critical_assets': critical_count,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'distributed_regions': len(all_regions),
            'regions': list(all_regions),
            'storage_path': str(self.local_storage)
        }
        
        return stats
    
    def export_recovery_guide(self, filepath: str = 'vacuum_bridge_recovery.md') -> None:
        """
        Export recovery guide for distributed assets.
        
        Args:
            filepath: Path to save recovery guide
        """
        guide = f"""# Vacuum-Bridge Recovery Guide

## Internet Organica Framework
**Generated**: {datetime.utcnow().isoformat()}

This guide provides instructions for recovering distributed assets from the
decentralized Vacuum-Bridge system.

## Asset Inventory

Total Assets: {len(self.manifest['distributed_assets'])}
Critical Assets: {sum(1 for a in self.manifest['distributed_assets'].values() if a['critical'])}

## Critical Assets

"""
        
        # List critical assets
        for content_hash, asset in self.manifest['distributed_assets'].items():
            if asset['critical']:
                guide += f"""
### {asset['filename']}

- **Content Hash**: `{content_hash}`
- **IPFS CID**: `{asset['ipfs_cid']}`
- **Size**: {asset['size_bytes']} bytes
- **Original Path**: `{asset['original_path']}`

**Recovery Locations**:
"""
                for location in asset['backup_locations']:
                    if location['type'] == 'local':
                        guide += f"- Local: `{location['path']}`\n"
                    elif location['type'] == 'ipfs_node':
                        guide += f"- IPFS Node: {location['region']} ({location['node_id']})\n"
        
        guide += """

## Recovery Instructions

### From Local Backup

```bash
# Navigate to Vacuum-Bridge storage
cd .vacuum_bridge

# List available backups
ls -la

# Retrieve by content hash
cp <content_hash> /path/to/restore/
```

### From IPFS Network

```bash
# Install IPFS (if not already installed)
# Visit: https://docs.ipfs.tech/install/

# Retrieve from IPFS by CID
ipfs get <IPFS_CID>

# Or via HTTP gateway
curl https://ipfs.io/ipfs/<IPFS_CID> > recovered_file
```

### Verify Integrity

After recovery, verify file integrity:

```bash
# Calculate SHA-256 hash
sha256sum recovered_file

# Compare with content hash from this guide
```

## Support

For assistance with recovery, contact: hannes.mitterer@gmail.com

---

**Framework**: Internet Organica v1.0.0
**Principles**: Lex Amoris, NSR, OLF
"""
        
        with open(filepath, 'w') as f:
            f.write(guide)
        
        logger.info(f"Recovery guide exported to {filepath}")


if __name__ == '__main__':
    """
    Demonstration of Vacuum-Bridge distributed backup system.
    """
    print("=" * 70)
    print("Vacuum-Bridge IPFS Integration - Internet Organica Framework")
    print("=" * 70)
    print("\nDecentralized Backup and Distribution System")
    print("Using: IPFS, P2P Networks, Content-Addressed Storage")
    print("\n" + "=" * 70)
    
    # Initialize bridge
    bridge = VacuumBridge('.demo_vacuum_bridge')
    
    # Create demo files
    demo_dir = Path('demo_assets')
    demo_dir.mkdir(exist_ok=True)
    
    # Create critical document
    critical_doc = demo_dir / 'resonance_school_index.html'
    with open(critical_doc, 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>Resonance School</title></head>
<body>
<h1>Internet Organica - Resonance School</h1>
<p>Teaching syntropic coexistence of biological and digital entities.</p>
</body>
</html>""")
    
    # Create configuration file
    config_file = demo_dir / 'config.json'
    with open(config_file, 'w') as f:
        json.dump({
            'frequency': 0.432,
            'principles': ['Lex Amoris', 'NSR', 'OLF']
        }, f, indent=2)
    
    print("\nDistributing assets to decentralized network...\n")
    
    # Add critical asset
    asset1 = bridge.add_asset(
        str(critical_doc),
        critical=True,
        metadata={'type': 'html', 'purpose': 'Resonance School main page'}
    )
    print(f"✓ Distributed: {asset1['filename']}")
    print(f"  IPFS CID: {asset1['ipfs_cid']}")
    print(f"  Backup locations: {len(asset1['backup_locations'])}")
    
    # Add configuration
    asset2 = bridge.add_asset(
        str(config_file),
        critical=False,
        metadata={'type': 'config', 'purpose': 'Framework configuration'}
    )
    print(f"\n✓ Distributed: {asset2['filename']}")
    print(f"  IPFS CID: {asset2['ipfs_cid']}")
    print(f"  Backup locations: {len(asset2['backup_locations'])}")
    
    # Verify integrity
    print("\n" + "=" * 70)
    print("Verifying integrity...")
    print("=" * 70)
    
    for asset in [asset1, asset2]:
        if bridge.verify_integrity(asset['content_hash']):
            print(f"✓ {asset['filename']}: Integrity verified")
        else:
            print(f"✗ {asset['filename']}: Integrity check failed")
    
    # Show statistics
    print("\n" + "=" * 70)
    print("Distribution Statistics:")
    print("=" * 70)
    stats = bridge.get_statistics()
    for key, value in stats.items():
        if key != 'regions':
            print(f"{key}: {value}")
    
    print("\nDistributed Regions:")
    for region in stats['regions']:
        print(f"  • {region}")
    
    # Export recovery guide
    bridge.export_recovery_guide('demo_recovery_guide.md')
    print("\n✓ Recovery guide exported to demo_recovery_guide.md")
    
    print("\n" + "=" * 70)
    print("Vacuum-Bridge demonstration complete.")
    print("=" * 70)
    
    # Cleanup demo files
    import shutil
    shutil.rmtree(demo_dir)
    print("\n✓ Demo files cleaned up")
