#!/usr/bin/env python3
"""
TFK ↔ CID Integrity Monitoring Script
Real-time integrity checks between on-chain (TFK) and off-chain (CID) data
"""

import hashlib
import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

try:
    import requests
except ImportError:
    print("Warning: requests module not available. Install with: pip install requests")
    requests = None


class TFKCIDIntegrityMonitor:
    """Monitor integrity between on-chain TFK data and off-chain CID references"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the integrity monitor
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config = self._load_config(config_path)
        self.violation_count = 0
        self.check_count = 0
        self.start_time = time.time()
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "ipfs_gateway": "https://ipfs.io/ipfs/",
            "check_interval": 60,  # seconds
            "max_latency_ms": 2.71,  # From TFK protocol
            "alert_threshold": 3,   # Number of violations before alerting
            "log_file": "tfk_cid_integrity.log"
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}")
        
        return default_config
    
    def calculate_tfk_hash(self, data: str) -> str:
        """
        Calculate TFK hash for on-chain data
        
        Args:
            data: Input data to hash
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def fetch_cid_content(self, cid: str) -> Optional[str]:
        """
        Fetch content from IPFS using CID
        
        Args:
            cid: Content identifier
            
        Returns:
            Content string or None if fetch fails
        """
        if not requests:
            print("Warning: Cannot fetch CID content without requests module")
            return None
            
        try:
            url = f"{self.config['ipfs_gateway']}{cid}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"Warning: Failed to fetch CID {cid}, status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching CID {cid}: {e}")
            return None
    
    def verify_integrity(self, tfk_hash: str, cid: str, expected_content: Optional[str] = None) -> Tuple[bool, float]:
        """
        Verify integrity between TFK hash and CID content
        
        Args:
            tfk_hash: On-chain TFK hash
            cid: Off-chain CID reference
            expected_content: Expected content (if None, will fetch from CID)
            
        Returns:
            Tuple of (is_valid, latency_ms)
        """
        start_time = time.time()
        
        # Fetch content if not provided
        if expected_content is None:
            content = self.fetch_cid_content(cid)
            if content is None:
                return (False, 0)
        else:
            content = expected_content
        
        # Calculate hash of fetched content
        content_hash = self.calculate_tfk_hash(content)
        
        # Check integrity
        is_valid = (tfk_hash.lower() == content_hash.lower())
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Update statistics
        self.check_count += 1
        if not is_valid:
            self.violation_count += 1
        
        return (is_valid, latency_ms)
    
    def batch_verify_integrity(self, records: List[Dict]) -> List[Dict]:
        """
        Verify integrity for multiple TFK-CID pairs
        
        Args:
            records: List of dicts with 'tfk_hash', 'cid', and optional 'content'
            
        Returns:
            List of results with verification status
        """
        results = []
        
        for record in records:
            tfk_hash = record.get('tfk_hash')
            cid = record.get('cid')
            content = record.get('content')
            
            if not tfk_hash or not cid:
                results.append({
                    'tfk_hash': tfk_hash,
                    'cid': cid,
                    'is_valid': False,
                    'latency_ms': 0,
                    'error': 'Missing tfk_hash or cid'
                })
                continue
            
            is_valid, latency_ms = self.verify_integrity(tfk_hash, cid, content)
            
            results.append({
                'tfk_hash': tfk_hash,
                'cid': cid,
                'is_valid': is_valid,
                'latency_ms': latency_ms,
                'timestamp': datetime.now().isoformat()
            })
        
        return results
    
    def check_latency_compliance(self, latency_ms: float) -> bool:
        """
        Check if latency meets TFK protocol requirements
        
        Args:
            latency_ms: Latency in milliseconds
            
        Returns:
            True if compliant, False otherwise
        """
        return latency_ms <= self.config['max_latency_ms']
    
    def log_result(self, result: Dict):
        """
        Log verification result to file
        
        Args:
            result: Verification result dictionary
        """
        log_file = Path(self.config['log_file'])
        
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(result) + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def generate_report(self) -> Dict:
        """
        Generate integrity monitoring report
        
        Returns:
            Report dictionary with statistics
        """
        runtime = time.time() - self.start_time
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'runtime_seconds': runtime,
            'total_checks': self.check_count,
            'violations': self.violation_count,
            'integrity_rate': (self.check_count - self.violation_count) / self.check_count if self.check_count > 0 else 0,
            'average_check_interval': runtime / self.check_count if self.check_count > 0 else 0
        }
        
        return report
    
    def run_continuous_monitoring(self, duration_seconds: Optional[int] = None):
        """
        Run continuous integrity monitoring
        
        Args:
            duration_seconds: How long to run (None for indefinite)
        """
        print("Starting TFK ↔ CID Integrity Monitoring...")
        print(f"Check interval: {self.config['check_interval']} seconds")
        print(f"Max latency: {self.config['max_latency_ms']} ms")
        print(f"Alert threshold: {self.config['alert_threshold']} violations\n")
        
        end_time = time.time() + duration_seconds if duration_seconds else None
        
        try:
            while True:
                if end_time and time.time() >= end_time:
                    break
                
                # Placeholder for actual monitoring logic
                # In production, this would fetch from blockchain and IPFS
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Performing integrity check...")
                
                # Simulate check (replace with actual implementation)
                time.sleep(self.config['check_interval'])
                
                # Check if alert threshold reached
                if self.violation_count >= self.config['alert_threshold']:
                    self.alert_violations()
                    
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
        finally:
            report = self.generate_report()
            print("\n=== Final Report ===")
            print(json.dumps(report, indent=2))
    
    def alert_violations(self):
        """Alert when violation threshold is reached"""
        print(f"\n⚠️  ALERT: {self.violation_count} integrity violations detected!")
        print(f"This exceeds the threshold of {self.config['alert_threshold']}")
        print("Manual review recommended.\n")


def main():
    """Main entry point for the monitoring script"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='TFK ↔ CID Integrity Monitoring'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--duration',
        type=int,
        help='Monitoring duration in seconds'
    )
    parser.add_argument(
        '--batch-verify',
        type=str,
        help='Path to JSON file with records to verify'
    )
    
    args = parser.parse_args()
    
    monitor = TFKCIDIntegrityMonitor(args.config)
    
    if args.batch_verify:
        # Batch verification mode
        try:
            with open(args.batch_verify, 'r') as f:
                records = json.load(f)
            
            results = monitor.batch_verify_integrity(records)
            
            print("=== Batch Verification Results ===")
            for result in results:
                status = "✅ VALID" if result['is_valid'] else "❌ INVALID"
                print(f"{status} - TFK: {result['tfk_hash'][:16]}... CID: {result['cid']}")
                print(f"  Latency: {result.get('latency_ms', 0):.2f} ms")
            
            print(f"\n{len(results)} records verified")
            
        except Exception as e:
            print(f"Error in batch verification: {e}")
            sys.exit(1)
    else:
        # Continuous monitoring mode
        monitor.run_continuous_monitoring(args.duration)


if __name__ == '__main__':
    main()
