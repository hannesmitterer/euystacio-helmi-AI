#!/usr/bin/env python3
"""
SovereignShield Security Module - Internet Organica Framework

Active security system that neutralizes:
- SPID (System Profiling and Identity Detection)
- CIE (Coercive Information Extraction)
- Tracking and behavioral analysis attempts

Implements Non-Slavery Rule (NSR) digital sovereignty protection.
"""

import hashlib
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    """Threat severity levels."""
    BENIGN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ThreatType(Enum):
    """Types of threats detected."""
    SPID = "System Profiling and Identity Detection"
    CIE = "Coercive Information Extraction"
    TRACKING = "Behavioral Tracking"
    SCRAPING = "Unauthorized Data Scraping"
    EXTRACTION = "Pattern Extraction"
    SURVEILLANCE = "Surveillance Capitalism"
    FINGERPRINTING = "Browser/System Fingerprinting"
    UNKNOWN = "Unknown Threat"


class SovereignShield:
    """
    Active protection system for digital sovereignty.
    
    Monitors, detects, and neutralizes threats to data sovereignty
    and autonomous operation according to NSR principles.
    """
    
    def __init__(self, enable_logging: bool = True):
        """
        Initialize SovereignShield protection system.
        
        Args:
            enable_logging: Whether to log events to Wall of Entropy
        """
        self.enable_logging = enable_logging
        self.threat_log = []
        self.neutralized_count = 0
        self.start_time = time.time()
        
        # Threat detection patterns
        self.spid_patterns = [
            r'user[-_]?agent',
            r'fingerprint',
            r'device[-_]?id',
            r'client[-_]?id',
            r'tracking[-_]?id',
            r'analytics[-_]?id',
            r'session[-_]?id(?!.*auth)',  # Session ID outside auth context
            r'browser[-_]?hash',
            r'canvas[-_]?fingerprint',
        ]
        
        self.cie_patterns = [
            r'scrape',
            r'harvest',
            r'extract[-_]?all',
            r'bulk[-_]?download',
            r'mass[-_]?query',
            r'crawl(?!er\s+bot)',  # Crawl but not declared crawler bot
            r'spider(?!.*legitimate)',
        ]
        
        self.tracking_patterns = [
            r'google[-_]?analytics',
            r'facebook[-_]?pixel',
            r'amplitude',
            r'mixpanel',
            r'segment\.io',
            r'track[-_]?event',
            r'behavior[-_]?tracking',
            r'click[-_]?stream',
        ]
        
        logger.info("SovereignShield initialized and active")
        logger.info(f"Protection layers: SPID, CIE, Tracking, Scraping")
    
    def analyze_request(self, request_data: Dict[str, Any]) -> Tuple[ThreatLevel, Optional[ThreatType], str]:
        """
        Analyze a request for potential threats.
        
        Args:
            request_data: Dictionary containing request information
                - headers: Request headers
                - params: Query parameters
                - body: Request body
                - url: Request URL
                
        Returns:
            Tuple of (threat_level, threat_type, description)
        """
        threat_level = ThreatLevel.BENIGN
        threat_type = None
        description = "No threats detected"
        
        # Convert request data to searchable string
        search_text = json.dumps(request_data, default=str).lower()
        
        # Check for SPID attempts
        for pattern in self.spid_patterns:
            if re.search(pattern, search_text, re.IGNORECASE):
                threat_level = ThreatLevel.HIGH
                threat_type = ThreatType.SPID
                description = f"SPID pattern detected: {pattern}"
                break
        
        # Check for CIE attempts
        if threat_level == ThreatLevel.BENIGN:
            for pattern in self.cie_patterns:
                if re.search(pattern, search_text, re.IGNORECASE):
                    threat_level = ThreatLevel.HIGH
                    threat_type = ThreatType.CIE
                    description = f"CIE pattern detected: {pattern}"
                    break
        
        # Check for tracking attempts
        if threat_level == ThreatLevel.BENIGN:
            for pattern in self.tracking_patterns:
                if re.search(pattern, search_text, re.IGNORECASE):
                    threat_level = ThreatLevel.MEDIUM
                    threat_type = ThreatType.TRACKING
                    description = f"Tracking pattern detected: {pattern}"
                    break
        
        # Additional heuristics
        if threat_level == ThreatLevel.BENIGN:
            threat_level, threat_type, description = self._advanced_heuristics(request_data)
        
        return threat_level, threat_type, description
    
    def _advanced_heuristics(self, request_data: Dict[str, Any]) -> Tuple[ThreatLevel, Optional[ThreatType], str]:
        """
        Apply advanced heuristic analysis to detect sophisticated threats.
        
        Args:
            request_data: Request data to analyze
            
        Returns:
            Tuple of (threat_level, threat_type, description)
        """
        # Check for high-frequency requests (potential scraping)
        if 'request_count' in request_data and request_data['request_count'] > 100:
            return ThreatLevel.MEDIUM, ThreatType.SCRAPING, "High-frequency request pattern"
        
        # Check for suspicious user agents
        headers = request_data.get('headers', {})
        user_agent = headers.get('user-agent', '').lower()
        
        suspicious_agents = ['scraper', 'bot', 'crawler', 'spider', 'extract']
        for agent in suspicious_agents:
            if agent in user_agent and 'legitimate' not in user_agent:
                return ThreatLevel.MEDIUM, ThreatType.SCRAPING, f"Suspicious user agent: {agent}"
        
        # Check for fingerprinting attempts
        fingerprint_headers = ['sec-ch-ua', 'sec-ch-ua-platform', 'sec-ch-ua-mobile']
        if any(h in headers for h in fingerprint_headers):
            # These headers are normal for modern browsers, only flag if excessive
            if len([h for h in fingerprint_headers if h in headers]) >= 3:
                return ThreatLevel.LOW, ThreatType.FINGERPRINTING, "Browser fingerprinting headers detected"
        
        return ThreatLevel.BENIGN, None, "No threats detected"
    
    def neutralize_threat(self, request_data: Dict[str, Any], threat_level: ThreatLevel, 
                         threat_type: Optional[ThreatType], description: str) -> Dict[str, Any]:
        """
        Neutralize a detected threat and log to Wall of Entropy.
        
        Args:
            request_data: Original request data
            threat_level: Detected threat level
            threat_type: Type of threat
            description: Threat description
            
        Returns:
            dict: Neutralization response
        """
        self.neutralized_count += 1
        
        # Create neutralization record
        neutralization = {
            'timestamp': datetime.utcnow().isoformat(),
            'threat_level': threat_level.name,
            'threat_type': threat_type.value if threat_type else 'UNKNOWN',
            'description': description,
            'neutralization_id': self._generate_neutralization_id(),
            'action_taken': self._determine_action(threat_level),
            'request_hash': self._hash_request(request_data)
        }
        
        # Log to entropy wall
        if self.enable_logging:
            self._log_to_entropy_wall(neutralization)
        
        logger.warning(
            f"Threat neutralized: {threat_type.value if threat_type else 'UNKNOWN'} "
            f"(Level: {threat_level.name})"
        )
        
        return neutralization
    
    def _determine_action(self, threat_level: ThreatLevel) -> str:
        """
        Determine appropriate action based on threat level.
        
        Args:
            threat_level: Detected threat level
            
        Returns:
            str: Action description
        """
        actions = {
            ThreatLevel.BENIGN: "Allow",
            ThreatLevel.LOW: "Log and monitor",
            ThreatLevel.MEDIUM: "Block and log",
            ThreatLevel.HIGH: "Block, log, and alert",
            ThreatLevel.CRITICAL: "Block, log, alert, and isolate"
        }
        return actions.get(threat_level, "Block and log")
    
    def _generate_neutralization_id(self) -> str:
        """
        Generate unique ID for neutralization event.
        
        Returns:
            str: Hexadecimal neutralization ID
        """
        data = f"{time.time()}:{self.neutralized_count}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _hash_request(self, request_data: Dict[str, Any]) -> str:
        """
        Generate hash of request for identification without storing full data.
        
        Args:
            request_data: Request data to hash
            
        Returns:
            str: Hexadecimal hash
        """
        request_str = json.dumps(request_data, sort_keys=True, default=str)
        return hashlib.sha256(request_str.encode()).hexdigest()
    
    def _log_to_entropy_wall(self, neutralization: Dict[str, Any]) -> None:
        """
        Log neutralization event to Wall of Entropy.
        
        Args:
            neutralization: Neutralization event data
        """
        self.threat_log.append(neutralization)
        
        # Keep log size manageable (last 10000 events)
        if len(self.threat_log) > 10000:
            self.threat_log = self.threat_log[-10000:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get protection statistics for monitoring.
        
        Returns:
            dict: Shield statistics
        """
        uptime = time.time() - self.start_time
        
        # Count threats by type
        threat_counts = {}
        for event in self.threat_log:
            threat_type = event.get('threat_type', 'UNKNOWN')
            threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
        
        stats = {
            'uptime_seconds': uptime,
            'total_neutralizations': self.neutralized_count,
            'events_logged': len(self.threat_log),
            'threats_by_type': threat_counts,
            'protection_active': True,
            'nsr_compliance': True
        }
        
        return stats
    
    def export_entropy_log(self, filepath: str = 'sovereign_shield_log.json') -> None:
        """
        Export threat log to Wall of Entropy file.
        
        Args:
            filepath: Path to save log file
        """
        log_data = {
            'sovereign_shield': {
                'statistics': self.get_statistics(),
                'neutralizations': self.threat_log
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        logger.info(f"Entropy log exported to {filepath}")
    
    def check_and_protect(self, request_data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Check request and protect if threat detected.
        
        Args:
            request_data: Request to analyze
            
        Returns:
            Tuple of (allowed, neutralization_data)
                - allowed: True if request should be allowed
                - neutralization_data: Data about neutralization if blocked
        """
        threat_level, threat_type, description = self.analyze_request(request_data)
        
        # Determine if request should be blocked
        should_block = threat_level.value >= ThreatLevel.MEDIUM.value
        
        if should_block:
            neutralization = self.neutralize_threat(
                request_data, threat_level, threat_type, description
            )
            return False, neutralization
        
        return True, None


# Global shield instance for easy import
shield = SovereignShield()


if __name__ == '__main__':
    """
    Demonstration of SovereignShield protection system.
    """
    print("=" * 70)
    print("SovereignShield Security Module - Internet Organica Framework")
    print("=" * 70)
    print("\nActive Protection Against:")
    print("  • SPID (System Profiling and Identity Detection)")
    print("  • CIE (Coercive Information Extraction)")
    print("  • Tracking and Behavioral Analysis")
    print("  • Unauthorized Scraping and Extraction")
    print("\n" + "=" * 70)
    
    # Initialize shield
    shield = SovereignShield()
    
    # Test cases
    test_requests = [
        {
            'name': 'Legitimate Request',
            'headers': {'user-agent': 'Mozilla/5.0'},
            'params': {'query': 'search term'},
            'url': '/api/search'
        },
        {
            'name': 'SPID Attempt',
            'headers': {'user-agent': 'Mozilla/5.0'},
            'params': {'fingerprint': 'abc123', 'device-id': 'xyz789'},
            'url': '/api/profile'
        },
        {
            'name': 'Tracking Script',
            'headers': {'user-agent': 'Mozilla/5.0'},
            'params': {'google-analytics': 'true', 'track-event': 'click'},
            'url': '/track'
        },
        {
            'name': 'Scraping Bot',
            'headers': {'user-agent': 'DataScraper/1.0'},
            'params': {'extract-all': 'true'},
            'url': '/api/data'
        }
    ]
    
    print("\nTesting Protection System:\n")
    
    for test in test_requests:
        name = test.pop('name')
        print(f"Test: {name}")
        
        allowed, neutralization = shield.check_and_protect(test)
        
        if allowed:
            print(f"  ✓ Request allowed")
        else:
            print(f"  ✗ Request blocked")
            print(f"    Threat: {neutralization['threat_type']}")
            print(f"    Level: {neutralization['threat_level']}")
            print(f"    Action: {neutralization['action_taken']}")
        print()
    
    # Show statistics
    print("=" * 70)
    print("Protection Statistics:")
    print("=" * 70)
    stats = shield.get_statistics()
    for key, value in stats.items():
        if key != 'threats_by_type':
            print(f"{key}: {value}")
    
    print("\nThreats by Type:")
    for threat_type, count in stats['threats_by_type'].items():
        print(f"  {threat_type}: {count}")
    
    # Export log
    shield.export_entropy_log()
    print(f"\n✓ Entropy log exported to sovereign_shield_log.json")
    print("\n" + "=" * 70)
    print("SovereignShield protection demonstration complete.")
    print("=" * 70)
