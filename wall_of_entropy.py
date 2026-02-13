#!/usr/bin/env python3
"""
Wall of Entropy - Transparent Public Logging System

Tracks and publicly displays:
- Unauthorized access attempts
- Ethical violations
- Security events
- System integrity validations

Ensures accountability and transparency for Internet Organica framework.
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EventCategory:
    """Event categories for the Wall of Entropy."""
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    ETHICAL_VIOLATION = "ethical_violation"
    SECURITY_EVENT = "security_event"
    INTEGRITY_VALIDATION = "integrity_validation"
    RHYTHM_SYNC = "rhythm_synchronization"
    THREAT_NEUTRALIZED = "threat_neutralized"
    GOVERNANCE_ACTION = "governance_action"
    SYSTEM_STATUS = "system_status"


class EntropyWall:
    """
    Transparent public logging system for Internet Organica.
    
    Maintains an immutable, cryptographically-linked chain of events
    for complete transparency and accountability.
    """
    
    def __init__(self, log_file: str = 'wall_of_entropy.log'):
        """
        Initialize the Wall of Entropy.
        
        Args:
            log_file: Path to the entropy log file
        """
        self.log_file = Path(log_file)
        self.events = []
        self.chain_hash = None
        
        # Load existing events if log file exists
        if self.log_file.exists():
            self._load_existing_log()
        else:
            # Initialize with genesis event
            self._create_genesis_event()
        
        logger.info(f"Wall of Entropy initialized with {len(self.events)} events")
    
    def _create_genesis_event(self) -> None:
        """Create the genesis (first) event in the entropy wall."""
        genesis = {
            'event_id': 0,
            'timestamp': datetime.utcnow().isoformat(),
            'category': EventCategory.SYSTEM_STATUS,
            'severity': 'info',
            'title': 'Wall of Entropy Initialized',
            'description': 'Internet Organica transparency system activated',
            'metadata': {
                'framework': 'Internet Organica',
                'version': '1.0.0',
                'principles': ['Lex Amoris', 'NSR', 'OLF']
            },
            'previous_hash': '0' * 64,
            'event_hash': None
        }
        
        # Generate hash for genesis event
        genesis['event_hash'] = self._hash_event(genesis)
        self.chain_hash = genesis['event_hash']
        
        self.events.append(genesis)
        self._persist_log()
    
    def _load_existing_log(self) -> None:
        """Load existing events from log file."""
        try:
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                self.events = data.get('events', [])
                self.chain_hash = data.get('chain_hash')
                
            logger.info(f"Loaded {len(self.events)} events from existing log")
        except Exception as e:
            logger.error(f"Error loading existing log: {e}")
            self._create_genesis_event()
    
    def log_event(self, category: str, severity: str, title: str, 
                  description: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Log an event to the Wall of Entropy.
        
        Args:
            category: Event category (use EventCategory constants)
            severity: Event severity (info, warning, error, critical)
            title: Brief event title
            description: Detailed event description
            metadata: Optional additional data
            
        Returns:
            dict: The logged event
        """
        event = {
            'event_id': len(self.events),
            'timestamp': datetime.utcnow().isoformat(),
            'category': category,
            'severity': severity,
            'title': title,
            'description': description,
            'metadata': metadata or {},
            'previous_hash': self.chain_hash,
            'event_hash': None
        }
        
        # Generate hash linking to previous event
        event['event_hash'] = self._hash_event(event)
        self.chain_hash = event['event_hash']
        
        # Add to chain
        self.events.append(event)
        
        # Persist to disk
        self._persist_log()
        
        # Log to console
        logger.log(
            self._get_log_level(severity),
            f"[{category}] {title}: {description}"
        )
        
        return event
    
    def _hash_event(self, event: Dict[str, Any]) -> str:
        """
        Generate cryptographic hash of event.
        
        Args:
            event: Event dictionary
            
        Returns:
            str: SHA-256 hash of event
        """
        # Create deterministic string representation
        event_copy = event.copy()
        event_copy.pop('event_hash', None)  # Remove hash field if present
        
        event_str = json.dumps(event_copy, sort_keys=True)
        return hashlib.sha256(event_str.encode()).hexdigest()
    
    def _persist_log(self) -> None:
        """Persist the entropy log to disk."""
        log_data = {
            'chain_hash': self.chain_hash,
            'total_events': len(self.events),
            'last_updated': datetime.utcnow().isoformat(),
            'events': self.events
        }
        
        try:
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error persisting entropy log: {e}")
    
    def _get_log_level(self, severity: str) -> int:
        """
        Convert severity string to logging level.
        
        Args:
            severity: Severity string
            
        Returns:
            int: Logging level constant
        """
        levels = {
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        return levels.get(severity.lower(), logging.INFO)
    
    def verify_chain_integrity(self) -> bool:
        """
        Verify the integrity of the event chain.
        
        Returns:
            bool: True if chain is valid
        """
        if not self.events:
            return True
        
        for i, event in enumerate(self.events):
            # Verify event hash
            expected_hash = self._hash_event(event)
            if event['event_hash'] != expected_hash:
                logger.error(f"Event {i} hash mismatch")
                return False
            
            # Verify chain linkage
            if i > 0:
                previous_event = self.events[i - 1]
                if event['previous_hash'] != previous_event['event_hash']:
                    logger.error(f"Event {i} chain break")
                    return False
        
        logger.info("Chain integrity verified successfully")
        return True
    
    def get_events(self, category: Optional[str] = None, 
                   severity: Optional[str] = None,
                   limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve events from the wall.
        
        Args:
            category: Filter by category (optional)
            severity: Filter by severity (optional)
            limit: Maximum number of events to return (optional)
            
        Returns:
            list: Filtered events
        """
        filtered = self.events
        
        if category:
            filtered = [e for e in filtered if e['category'] == category]
        
        if severity:
            filtered = [e for e in filtered if e['severity'] == severity]
        
        if limit:
            filtered = filtered[-limit:]
        
        return filtered
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about logged events.
        
        Returns:
            dict: Event statistics
        """
        # Count by category
        category_counts = {}
        for event in self.events:
            cat = event['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Count by severity
        severity_counts = {}
        for event in self.events:
            sev = event['severity']
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        # Get time range
        if self.events:
            first_event = self.events[0]['timestamp']
            last_event = self.events[-1]['timestamp']
        else:
            first_event = last_event = None
        
        stats = {
            'total_events': len(self.events),
            'categories': category_counts,
            'severities': severity_counts,
            'first_event': first_event,
            'last_event': last_event,
            'chain_valid': self.verify_chain_integrity()
        }
        
        return stats
    
    def export_public_report(self, filepath: str = 'entropy_wall_report.json') -> None:
        """
        Export a public transparency report.
        
        Args:
            filepath: Path to save report
        """
        report = {
            'report_generated': datetime.utcnow().isoformat(),
            'framework': 'Internet Organica',
            'principles': ['Lex Amoris', 'NSR', 'OLF'],
            'statistics': self.get_statistics(),
            'recent_events': self.get_events(limit=100),
            'chain_integrity': self.verify_chain_integrity()
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Public transparency report exported to {filepath}")
    
    def generate_html_dashboard(self, filepath: str = 'entropy_wall_dashboard.html') -> None:
        """
        Generate an HTML dashboard for viewing the Wall of Entropy.
        
        Args:
            filepath: Path to save HTML file
        """
        stats = self.get_statistics()
        recent_events = self.get_events(limit=50)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wall of Entropy - Internet Organica</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            color: #667eea;
        }}
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}
        .event {{
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #28a745;
        }}
        .event.warning {{ border-left-color: #ffc107; }}
        .event.error {{ border-left-color: #dc3545; }}
        .event.critical {{ border-left-color: #721c24; }}
        .event-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }}
        .event-title {{
            font-weight: bold;
            color: #667eea;
        }}
        .event-time {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        .event-description {{
            color: #495057;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: bold;
            margin-right: 5px;
        }}
        .badge.info {{ background: #17a2b8; color: white; }}
        .badge.warning {{ background: #ffc107; color: #333; }}
        .badge.error {{ background: #dc3545; color: white; }}
        .badge.critical {{ background: #721c24; color: white; }}
        .integrity {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌿 Wall of Entropy - Internet Organica</h1>
        
        <div class="integrity">
            ✓ Chain Integrity: {'VERIFIED' if stats['chain_valid'] else 'COMPROMISED'}
        </div>
        
        <h2>Statistics</h2>
        <div class="stats">
            <div class="stat-card">
                <h3>Total Events</h3>
                <div class="value">{stats['total_events']}</div>
            </div>
"""
        
        # Add category stats
        for category, count in stats.get('categories', {}).items():
            html += f"""
            <div class="stat-card">
                <h3>{category.replace('_', ' ').title()}</h3>
                <div class="value">{count}</div>
            </div>
"""
        
        html += """
        </div>
        
        <h2>Recent Events</h2>
"""
        
        # Add recent events
        for event in reversed(recent_events):
            severity = event['severity']
            html += f"""
        <div class="event {severity}">
            <div class="event-header">
                <span class="event-title">{event['title']}</span>
                <span class="event-time">{event['timestamp']}</span>
            </div>
            <div>
                <span class="badge {severity}">{severity.upper()}</span>
                <span class="badge info">{event['category']}</span>
            </div>
            <div class="event-description">{event['description']}</div>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        logger.info(f"HTML dashboard generated at {filepath}")


# Global entropy wall instance
wall = EntropyWall()


if __name__ == '__main__':
    """
    Demonstration of Wall of Entropy logging system.
    """
    print("=" * 70)
    print("Wall of Entropy - Internet Organica Framework")
    print("=" * 70)
    print("\nTransparent Public Logging System")
    print("Tracks: Unauthorized Access, Ethical Violations, Security Events")
    print("\n" + "=" * 70)
    
    # Initialize wall
    wall = EntropyWall('demo_wall_of_entropy.log')
    
    # Log various events
    print("\nLogging demonstration events...\n")
    
    wall.log_event(
        EventCategory.SECURITY_EVENT,
        'info',
        'SovereignShield Activated',
        'Protection system successfully initialized'
    )
    
    wall.log_event(
        EventCategory.THREAT_NEUTRALIZED,
        'warning',
        'SPID Attempt Blocked',
        'Detected and neutralized system profiling attempt',
        {'source_ip': '192.168.1.100', 'pattern': 'fingerprint'}
    )
    
    wall.log_event(
        EventCategory.UNAUTHORIZED_ACCESS,
        'error',
        'Unauthorized Data Scraping Attempt',
        'Blocked bulk data extraction request',
        {'user_agent': 'DataScraper/1.0', 'requests': 500}
    )
    
    wall.log_event(
        EventCategory.INTEGRITY_VALIDATION,
        'info',
        'Biological Rhythm Sync Verified',
        'System operating at 0.432 Hz resonance',
        {'frequency': 0.432, 'deviation': 0.0001}
    )
    
    # Verify chain
    print("\nVerifying chain integrity...")
    if wall.verify_chain_integrity():
        print("✓ Chain integrity verified\n")
    else:
        print("✗ Chain integrity compromised\n")
    
    # Show statistics
    print("=" * 70)
    print("Wall Statistics:")
    print("=" * 70)
    stats = wall.get_statistics()
    print(f"Total Events: {stats['total_events']}")
    print(f"Chain Valid: {stats['chain_valid']}")
    print("\nEvents by Category:")
    for category, count in stats['categories'].items():
        print(f"  {category}: {count}")
    print("\nEvents by Severity:")
    for severity, count in stats['severities'].items():
        print(f"  {severity}: {count}")
    
    # Export reports
    wall.export_public_report('demo_entropy_report.json')
    wall.generate_html_dashboard('demo_entropy_dashboard.html')
    
    print("\n✓ Public report exported to demo_entropy_report.json")
    print("✓ HTML dashboard generated at demo_entropy_dashboard.html")
    print("\n" + "=" * 70)
    print("Wall of Entropy demonstration complete.")
    print("=" * 70)
