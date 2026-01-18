"""
lex_amoris_security.py - Lex Amoris Security Enhancements

This module implements strategic security improvements based on Lex Amoris principles:
1. Dynamic Blacklist with Rhythm Validation
2. Lazy Security (energy-efficient protection)
3. IPFS Backup System
4. Rescue Channel (Canale di Soccorso)

All security measures are aligned with Euystacio framework principles of love,
dignity, and consensus.
"""

import json
import hashlib
import time
import random
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import os


class RhythmValidator:
    """
    Validates data packets based on their rhythmic frequency.
    Packets that don't vibrate at the correct frequency are discarded.
    """
    
    def __init__(self, base_frequency: float = 432.0):
        """
        Initialize rhythm validator.
        
        Args:
            base_frequency: Base harmonic frequency in Hz (default: 432 Hz - natural tuning)
        """
        self.base_frequency = base_frequency
        self.tolerance = 0.05  # 5% tolerance
        self.validation_log = []
        
    def calculate_packet_frequency(self, data: Dict) -> float:
        """
        Calculate the rhythmic frequency of a data packet.
        
        Args:
            data: Data packet to analyze
            
        Returns:
            Calculated frequency in Hz
        """
        # Create deterministic hash of packet content
        packet_str = json.dumps(data, sort_keys=True)
        packet_hash = hashlib.sha256(packet_str.encode()).hexdigest()
        
        # Convert hash to numeric value and map to frequency range
        hash_value = int(packet_hash[:16], 16)
        
        # Map to frequency range around base frequency
        frequency = self.base_frequency * (1 + ((hash_value % 1000) - 500) / 10000)
        
        return frequency
    
    def validate_rhythm(self, data: Dict, source_ip: Optional[str] = None) -> Tuple[bool, str]:
        """
        Validate if a packet vibrates at the correct frequency.
        
        Args:
            data: Data packet to validate
            source_ip: Source IP address (optional, not used for validation per requirement)
            
        Returns:
            Tuple of (is_valid, reason)
        """
        if not data:
            return False, "Empty packet"
        
        # Calculate packet frequency
        frequency = self.calculate_packet_frequency(data)
        
        # Check if frequency is within acceptable range
        lower_bound = self.base_frequency * (1 - self.tolerance)
        upper_bound = self.base_frequency * (1 + self.tolerance)
        
        is_valid = lower_bound <= frequency <= upper_bound
        
        # Log validation attempt
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": source_ip or "unknown",
            "frequency": frequency,
            "valid": is_valid,
            "base_frequency": self.base_frequency
        }
        self.validation_log.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self.validation_log) > 1000:
            self.validation_log = self.validation_log[-1000:]
        
        if is_valid:
            return True, f"Frequency {frequency:.2f} Hz within acceptable range"
        else:
            return False, f"Frequency {frequency:.2f} Hz outside acceptable range [{lower_bound:.2f}, {upper_bound:.2f}]"


class DynamicBlacklist:
    """
    Dynamic blacklist that tracks and blocks sources based on rhythm validation failures.
    """
    
    def __init__(self, threshold: int = 5, time_window: int = 300):
        """
        Initialize dynamic blacklist.
        
        Args:
            threshold: Number of failures before blacklisting
            time_window: Time window in seconds for counting failures
        """
        self.threshold = threshold
        self.time_window = time_window
        self.failures: Dict[str, List[float]] = {}
        self.blacklist: Dict[str, float] = {}
        self.blacklist_duration = 3600  # 1 hour
        
    def record_failure(self, source: str):
        """Record a validation failure for a source."""
        current_time = time.time()
        
        if source not in self.failures:
            self.failures[source] = []
        
        self.failures[source].append(current_time)
        
        # Clean old failures outside time window
        self.failures[source] = [
            t for t in self.failures[source]
            if current_time - t <= self.time_window
        ]
        
        # Check if threshold exceeded
        if len(self.failures[source]) >= self.threshold:
            self.blacklist[source] = current_time
    
    def is_blacklisted(self, source: str) -> bool:
        """Check if a source is currently blacklisted."""
        if source not in self.blacklist:
            return False
        
        # Check if blacklist duration has expired
        current_time = time.time()
        if current_time - self.blacklist[source] > self.blacklist_duration:
            del self.blacklist[source]
            return False
        
        return True
    
    def get_blacklist(self) -> List[str]:
        """Get current blacklist."""
        current_time = time.time()
        return [
            source for source, timestamp in self.blacklist.items()
            if current_time - timestamp <= self.blacklist_duration
        ]


class LazySecurity:
    """
    Energy-efficient security that activates only when environmental pressure is detected.
    """
    
    def __init__(self, activation_threshold: float = 50.0):
        """
        Initialize lazy security.
        
        Args:
            activation_threshold: Electromagnetic field pressure threshold in mV/m
        """
        self.activation_threshold = activation_threshold
        self.is_active = False
        self.scan_history = []
        
    def environmental_pressure_scan(self) -> float:
        """
        Perform environmental electromagnetic field pressure scan.
        
        Returns:
            Current electromagnetic field pressure in mV/m
        """
        # Simulate scan (in production, this would interface with actual sensors)
        # For now, we check system load and network activity as proxy
        
        # Base pressure
        pressure = 30.0
        
        # Add variation based on system state
        if os.path.exists("/proc/loadavg"):
            try:
                with open("/proc/loadavg", "r") as f:
                    load = float(f.read().split()[0])
                    pressure += load * 5
            except (OSError, ValueError, IndexError):
                pass
        
        # Add small random variation
        pressure += random.uniform(-5, 5)
        
        # Log scan
        self.scan_history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pressure": pressure
        })
        
        # Keep only last 100 scans
        if len(self.scan_history) > 100:
            self.scan_history = self.scan_history[-100:]
        
        return pressure
    
    def should_activate(self) -> bool:
        """
        Determine if security should be active based on scan.
        
        Returns:
            True if security should be active
        """
        pressure = self.environmental_pressure_scan()
        self.is_active = pressure > self.activation_threshold
        return self.is_active
    
    def get_status(self) -> Dict:
        """Get current lazy security status."""
        return {
            "is_active": self.is_active,
            "activation_threshold": self.activation_threshold,
            "recent_scans": self.scan_history[-10:] if self.scan_history else []
        }


class IPFSBackupManager:
    """
    IPFS-based backup system for repository configuration mirroring.
    """
    
    def __init__(self, backup_dir: str = "ipfs_backup"):
        """
        Initialize IPFS backup manager.
        
        Args:
            backup_dir: Directory for local backup cache
        """
        self.backup_dir = backup_dir
        self.backup_manifest = {}
        os.makedirs(backup_dir, exist_ok=True)
        
        # Load existing manifest if it exists
        manifest_path = os.path.join(backup_dir, "manifest.json")
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    self.backup_manifest = json.load(f)
            except (OSError, json.JSONDecodeError, UnicodeDecodeError):
                self.backup_manifest = {}
        
    def create_backup(self, config_files: List[str]) -> Dict:
        """
        Create backup of configuration files.
        
        Args:
            config_files: List of file paths to backup
            
        Returns:
            Backup manifest with file hashes
        """
        manifest = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "files": {}
        }
        
        for file_path in config_files:
            if os.path.exists(file_path):
                try:
                    # Read file in binary mode to support both text and binary files
                    with open(file_path, "rb") as f:
                        content_bytes = f.read()
                    
                    # Calculate hash on raw bytes
                    file_hash = hashlib.sha256(content_bytes).hexdigest()
                    
                    # Save to backup directory
                    backup_filename = os.path.basename(file_path)
                    backup_path = os.path.join(self.backup_dir, f"{file_hash}_{backup_filename}")
                    
                    # Write backup in binary mode to preserve exact contents
                    with open(backup_path, "wb") as f:
                        f.write(content_bytes)
                    
                    manifest["files"][file_path] = {
                        "hash": file_hash,
                        "backup_path": backup_path,
                        "size": len(content_bytes)
                    }
                except Exception as e:
                    manifest["files"][file_path] = {
                        "error": str(e)
                    }
        
        # Save manifest
        manifest_path = os.path.join(self.backup_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        
        self.backup_manifest = manifest
        return manifest
    
    def verify_backup(self, file_path: str) -> bool:
        """
        Verify a backed-up file hasn't been tampered with.
        
        Args:
            file_path: Original file path
            
        Returns:
            True if backup is valid
        """
        if file_path not in self.backup_manifest.get("files", {}):
            return False
        
        file_info = self.backup_manifest["files"][file_path]
        if "error" in file_info:
            return False
        
        backup_path = file_info["backup_path"]
        expected_hash = file_info["hash"]
        
        if not os.path.exists(backup_path):
            return False
        
        try:
            with open(backup_path, "rb") as f:
                content_bytes = f.read()
            
            actual_hash = hashlib.sha256(content_bytes).hexdigest()
            return actual_hash == expected_hash
        except (OSError, IOError):
            return False


class RescueChannel:
    """
    Lex Amoris-based messaging for unblocking nodes in case of false positives.
    """
    
    def __init__(self):
        """Initialize rescue channel."""
        self.rescue_log = []
        self.false_positive_threshold = 0.3  # 30% false positive rate triggers rescue
        
    def analyze_false_positives(self, validation_log: List[Dict]) -> float:
        """
        Analyze validation log to detect false positive patterns.
        
        Args:
            validation_log: List of validation log entries
            
        Returns:
            False positive rate (0.0 to 1.0)
        """
        if not validation_log:
            return 0.0
        
        # Count recent rejections from same source
        recent_window = 60  # Last 60 seconds
        current_time = time.time()
        
        source_stats = {}
        for entry in validation_log:
            try:
                timestamp = datetime.fromisoformat(entry["timestamp"]).timestamp()
                if current_time - timestamp > recent_window:
                    continue
                
                source = entry.get("source_ip", "unknown")
                if source not in source_stats:
                    source_stats[source] = {"total": 0, "invalid": 0}
                
                source_stats[source]["total"] += 1
                if not entry.get("valid", False):
                    source_stats[source]["invalid"] += 1
            except (KeyError, ValueError, TypeError):
                # Skip malformed or incomplete log entries
                continue
        
        # Calculate false positive rate focusing on sources with mixed outcomes
        # Only consider sources that have both valid and invalid packets in the window,
        # as these are the most indicative of potential false positives (e.g., alternating patterns).
        if not source_stats:
            return 0.0
        
        rates = []
        for stats in source_stats.values():
            total = stats.get("total", 0)
            invalid = stats.get("invalid", 0)
            # Skip sources that are entirely valid (100% success) or entirely invalid (100% failure).
            # Entirely valid sources don't need rescue.
            # Entirely invalid sources are likely attackers, not false positives.
            # False positives are characterized by mixed results (alternating valid/invalid).
            if total <= 0 or invalid == 0 or invalid == total:
                continue
            rates.append(invalid / total)
        
        return sum(rates) / len(rates) if rates else 0.0
    
    def send_rescue_message(self, source: str, reason: str = "false_positive_detected") -> Dict:
        """
        Send rescue message to unblock a node.
        
        Args:
            source: Source identifier to rescue
            reason: Reason for rescue
            
        Returns:
            Rescue message dict
        """
        message = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "rescue",
            "source": source,
            "reason": reason,
            "lex_amoris_signature": "love_first_protocol",
            "action": "unblock",
            "compassion_level": "high"
        }
        
        self.rescue_log.append(message)
        
        # Keep only last 100 entries
        if len(self.rescue_log) > 100:
            self.rescue_log = self.rescue_log[-100:]
        
        return message
    
    def should_trigger_rescue(self, validation_log: List[Dict]) -> bool:
        """
        Determine if rescue should be triggered.
        
        Args:
            validation_log: List of validation log entries
            
        Returns:
            True if rescue should be triggered
        """
        false_positive_rate = self.analyze_false_positives(validation_log)
        return false_positive_rate >= self.false_positive_threshold


class LexAmorisSecuritySystem:
    """
    Integrated Lex Amoris security system combining all components.
    """
    
    def __init__(self):
        """Initialize the complete security system."""
        self.rhythm_validator = RhythmValidator()
        self.blacklist = DynamicBlacklist()
        self.lazy_security = LazySecurity()
        self.ipfs_backup = IPFSBackupManager()
        self.rescue_channel = RescueChannel()
        
    def process_packet(self, data: Dict, source_ip: str) -> Dict:
        """
        Process incoming data packet through security system.
        
        Args:
            data: Data packet
            source_ip: Source IP address
            
        Returns:
            Processing result
        """
        result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": source_ip,
            "accepted": False,
            "reason": ""
        }
        
        # Determine lazy security state for logging
        lazy_security_active = self.lazy_security.should_activate()
        if not lazy_security_active:
            result["lazy_security_state"] = "inactive - low environmental pressure"
        
        # Check blacklist (always performed regardless of lazy security)
        if self.blacklist.is_blacklisted(source_ip):
            result["reason"] = "Source is blacklisted"
            
            # Check if rescue should be triggered (always performed to prevent false lockouts)
            if self.rescue_channel.should_trigger_rescue(self.rhythm_validator.validation_log):
                rescue_msg = self.rescue_channel.send_rescue_message(
                    source_ip,
                    "High false positive rate detected"
                )
                result["rescue"] = rescue_msg
                result["accepted"] = True
                result["reason"] = "Rescued due to false positive detection"
            
            return result
        
        # Validate rhythm (always performed regardless of lazy security)
        is_valid, validation_reason = self.rhythm_validator.validate_rhythm(data, source_ip)
        
        if not is_valid:
            self.blacklist.record_failure(source_ip)
            result["reason"] = f"Rhythm validation failed: {validation_reason}"
            return result
        
        result["accepted"] = True
        result["reason"] = validation_reason
        return result
    
    def create_configuration_backup(self) -> Dict:
        """
        Create IPFS backup of critical configuration files.
        
        Returns:
            Backup manifest
        """
        config_files = [
            "red_code.json",
            "ethical_shield.yaml",
            "governance.json",
            "package.json",
            "requirements.txt"
        ]
        
        # Filter to only existing files
        existing_files = [f for f in config_files if os.path.exists(f)]
        
        return self.ipfs_backup.create_backup(existing_files)
    
    def get_system_status(self) -> Dict:
        """
        Get complete system status.
        
        Returns:
            System status dictionary
        """
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "lazy_security": self.lazy_security.get_status(),
            "blacklist": {
                "blocked_sources": self.blacklist.get_blacklist(),
                "total_blocked": len(self.blacklist.get_blacklist())
            },
            "rhythm_validation": {
                "total_validations": len(self.rhythm_validator.validation_log),
                "recent_validations": self.rhythm_validator.validation_log[-10:]
            },
            "rescue_channel": {
                "total_rescues": len(self.rescue_channel.rescue_log),
                "recent_rescues": self.rescue_channel.rescue_log[-5:]
            },
            "backup": {
                "manifest": self.ipfs_backup.backup_manifest
            }
        }


# Convenience function for easy integration
def create_security_system() -> LexAmorisSecuritySystem:
    """Create and return a new Lex Amoris security system instance."""
    return LexAmorisSecuritySystem()
