"""
blacklist.py - Permanent Blacklist System for EUYSTACIO Framework

This module implements a permanent blacklist to block communication from
suspicious nodes and entities that threaten system security.
Provides protection against attacks and unauthorized access attempts.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Set

BLACKLIST_PATH = "blacklist.json"


class EuystacioBlacklist:
    """
    Permanent blacklist management for EUYSTACIO framework.
    Blocks suspicious nodes and entities to ensure system security.
    """
    
    def __init__(self, blacklist_path: str = BLACKLIST_PATH):
        """Initialize blacklist with persistent storage."""
        self.blacklist_path = blacklist_path
        self.blacklist_data = self._load_or_create_blacklist()
    
    def _load_or_create_blacklist(self) -> Dict:
        """Load existing blacklist or create new one with default structure."""
        if os.path.exists(self.blacklist_path):
            try:
                with open(self.blacklist_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure all required fields exist
                    if not isinstance(data, dict):
                        return self._create_default_blacklist()
                    if 'blocked_entities' not in data:
                        data['blocked_entities'] = []
                    if 'metadata' not in data:
                        data['metadata'] = self._create_metadata()
                    return data
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, create new blacklist
                return self._create_default_blacklist()
        else:
            return self._create_default_blacklist()
    
    def _create_default_blacklist(self) -> Dict:
        """Create default blacklist structure."""
        return {
            "blocked_entities": [],
            "metadata": self._create_metadata(),
            "statistics": {
                "total_blocked": 0,
                "total_blocks_prevented": 0,
                "last_threat_detected": None
            }
        }
    
    def _create_metadata(self) -> Dict:
        """Create metadata for blacklist."""
        return {
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "framework": "EUYSTACIO",
            "purpose": "Permanent protection against suspicious entities"
        }
    
    def _save_blacklist(self) -> bool:
        """Save blacklist to persistent storage."""
        try:
            self.blacklist_data['metadata']['last_updated'] = datetime.utcnow().isoformat()
            with open(self.blacklist_path, 'w', encoding='utf-8') as f:
                json.dump(self.blacklist_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving blacklist: {e}")
            return False
    
    def add_entity(self, entity_id: str, entity_type: str, reason: str, 
                   severity: str = "high", metadata: Optional[Dict] = None) -> bool:
        """
        Add an entity to the blacklist.
        
        Args:
            entity_id: Unique identifier for the entity (IP, node ID, etc.)
            entity_type: Type of entity (ip_address, node_id, ai_agent, etc.)
            reason: Reason for blocking
            severity: Threat severity level (critical, high, medium, low)
            metadata: Additional metadata about the entity
        
        Returns:
            True if successfully added, False otherwise
        """
        # Check if entity already exists
        if self.is_blocked(entity_id):
            return False
        
        entity_record = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "reason": reason,
            "severity": severity,
            "blocked_at": datetime.utcnow().isoformat(),
            "blocked_by": "EUYSTACIO_SECURITY_SYSTEM",
            "metadata": metadata or {}
        }
        
        self.blacklist_data['blocked_entities'].append(entity_record)
        self.blacklist_data['statistics']['total_blocked'] += 1
        
        return self._save_blacklist()
    
    def remove_entity(self, entity_id: str) -> bool:
        """
        Remove an entity from the blacklist.
        
        Args:
            entity_id: Unique identifier for the entity
        
        Returns:
            True if successfully removed, False if not found
        """
        original_length = len(self.blacklist_data['blocked_entities'])
        self.blacklist_data['blocked_entities'] = [
            entity for entity in self.blacklist_data['blocked_entities']
            if entity['entity_id'] != entity_id
        ]
        
        if len(self.blacklist_data['blocked_entities']) < original_length:
            self.blacklist_data['statistics']['total_blocked'] -= 1
            self._save_blacklist()
            return True
        return False
    
    def is_blocked(self, entity_id: str) -> bool:
        """
        Check if an entity is blocked.
        
        Args:
            entity_id: Unique identifier for the entity
        
        Returns:
            True if entity is blocked, False otherwise
        """
        for entity in self.blacklist_data['blocked_entities']:
            if entity['entity_id'] == entity_id:
                return True
        return False
    
    def get_entity(self, entity_id: str) -> Optional[Dict]:
        """
        Get details of a blocked entity.
        
        Args:
            entity_id: Unique identifier for the entity
        
        Returns:
            Entity record if found, None otherwise
        """
        for entity in self.blacklist_data['blocked_entities']:
            if entity['entity_id'] == entity_id:
                return entity
        return None
    
    def list_blocked_entities(self, entity_type: Optional[str] = None, 
                             severity: Optional[str] = None) -> List[Dict]:
        """
        List all blocked entities with optional filtering.
        
        Args:
            entity_type: Filter by entity type
            severity: Filter by severity level
        
        Returns:
            List of blocked entity records
        """
        entities = self.blacklist_data['blocked_entities']
        
        if entity_type:
            entities = [e for e in entities if e['entity_type'] == entity_type]
        
        if severity:
            entities = [e for e in entities if e['severity'] == severity]
        
        return entities
    
    def check_and_log_attempt(self, entity_id: str) -> bool:
        """
        Check if entity is blocked and log the attempt.
        
        Args:
            entity_id: Unique identifier for the entity
        
        Returns:
            True if blocked (attempt prevented), False if allowed
        """
        if self.is_blocked(entity_id):
            self.blacklist_data['statistics']['total_blocks_prevented'] += 1
            self.blacklist_data['statistics']['last_threat_detected'] = datetime.utcnow().isoformat()
            self._save_blacklist()
            return True
        return False
    
    def get_statistics(self) -> Dict:
        """Get blacklist statistics."""
        return self.blacklist_data.get('statistics', {})
    
    def get_all_blocked_ids(self) -> Set[str]:
        """
        Get set of all blocked entity IDs for quick lookup.
        
        Returns:
            Set of blocked entity IDs
        """
        return {entity['entity_id'] for entity in self.blacklist_data['blocked_entities']}


# Global blacklist instance for backwards compatibility
# For new code, prefer using get_blacklist() or creating your own instance
_global_blacklist = None


def get_blacklist(blacklist_path: str = BLACKLIST_PATH) -> EuystacioBlacklist:
    """
    Get or create the global blacklist instance.
    
    Args:
        blacklist_path: Path to blacklist file
    
    Returns:
        Global EuystacioBlacklist instance
    """
    global _global_blacklist
    if _global_blacklist is None:
        _global_blacklist = EuystacioBlacklist(blacklist_path)
    return _global_blacklist


# Module-level blacklist for backwards compatibility
blacklist = get_blacklist()


def ensure_blacklist(path: str = BLACKLIST_PATH) -> bool:
    """
    Ensure blacklist file exists with proper structure.
    
    Args:
        path: Path to blacklist file
    
    Returns:
        True if blacklist exists or was created successfully
    """
    try:
        bl = EuystacioBlacklist(path)
        bl._save_blacklist()  # Ensure it's saved to disk
        return os.path.exists(path)
    except Exception:
        return False
