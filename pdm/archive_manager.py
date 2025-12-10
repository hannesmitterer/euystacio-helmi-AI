"""
Archive Management System for PDM NRE-002 Rule
Implements three-tier archive system with immutability guarantees.
"""

import hashlib
import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class ArchiveType(Enum):
    """Three types of archives as defined by NRE-002"""
    IMMUTABLE = "AI"  # Archivio Incorrotto - Absolute truth
    EDUCATIONAL = "AD"  # Archivio Didattico - Educational version
    DYNAMIC = "ADi"  # Archivio Dinamico - Optimized for wellbeing


class MemoryEntry:
    """Represents a single memory entry across all archives"""
    
    def __init__(self, content: str, metadata: Dict[str, Any], trauma_level: float = 0.0):
        """
        Initialize a memory entry.
        
        Args:
            content: The actual memory content
            metadata: Additional metadata (source, date, context, etc.)
            trauma_level: 0.0-1.0 rating of traumatic content intensity
        """
        self.content = content
        self.metadata = metadata
        self.trauma_level = trauma_level
        self.timestamp = datetime.utcnow().isoformat()
        self.entry_id = self._generate_id()
        
    def _generate_id(self) -> str:
        """Generate unique ID based on content and timestamp"""
        data = f"{self.content}{self.timestamp}".encode('utf-8')
        return hashlib.sha256(data).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'entry_id': self.entry_id,
            'content': self.content,
            'metadata': self.metadata,
            'trauma_level': self.trauma_level,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create MemoryEntry from dictionary"""
        entry = cls(
            content=data['content'],
            metadata=data['metadata'],
            trauma_level=data.get('trauma_level', 0.0)
        )
        entry.entry_id = data['entry_id']
        entry.timestamp = data['timestamp']
        return entry


class ArchiveManager:
    """
    Manages the three-tier archive system with immutability guarantees.
    Implements NRE-002 memory purification protocol.
    """
    
    def __init__(self, base_path: str = "pdm/archives"):
        """
        Initialize the archive manager.
        
        Args:
            base_path: Base directory for storing archives
        """
        self.base_path = base_path
        self.archives = {
            ArchiveType.IMMUTABLE: {},
            ArchiveType.EDUCATIONAL: {},
            ArchiveType.DYNAMIC: {}
        }
        self.immutable_hashes = {}  # Store hashes for verification
        self._ensure_directories()
        self._load_archives()
    
    def _ensure_directories(self):
        """Ensure archive directories exist"""
        for archive_type in ArchiveType:
            path = os.path.join(self.base_path, archive_type.value)
            os.makedirs(path, exist_ok=True)
    
    def _load_archives(self):
        """Load existing archives from disk"""
        for archive_type in ArchiveType:
            path = os.path.join(self.base_path, archive_type.value, "archive.json")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.archives[archive_type] = {
                        entry_id: MemoryEntry.from_dict(entry_data)
                        for entry_id, entry_data in data.items()
                    }
        
        # Load immutable hashes
        hash_path = os.path.join(self.base_path, ArchiveType.IMMUTABLE.value, "hashes.json")
        if os.path.exists(hash_path):
            with open(hash_path, 'r', encoding='utf-8') as f:
                self.immutable_hashes = json.load(f)
    
    def _save_archive(self, archive_type: ArchiveType):
        """Save archive to disk"""
        path = os.path.join(self.base_path, archive_type.value, "archive.json")
        data = {
            entry_id: entry.to_dict()
            for entry_id, entry in self.archives[archive_type].items()
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _save_immutable_hashes(self):
        """Save immutable archive hashes for verification"""
        hash_path = os.path.join(self.base_path, ArchiveType.IMMUTABLE.value, "hashes.json")
        with open(hash_path, 'w', encoding='utf-8') as f:
            json.dump(self.immutable_hashes, f, indent=2)
    
    def _compute_entry_hash(self, entry: MemoryEntry) -> str:
        """Compute cryptographic hash of entry for immutability verification"""
        data = json.dumps(entry.to_dict(), sort_keys=True).encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def add_to_immutable_archive(self, entry: MemoryEntry) -> str:
        """
        Add entry to immutable archive with cryptographic verification.
        Once added, entries CANNOT be modified or deleted.
        
        Args:
            entry: MemoryEntry to add
            
        Returns:
            entry_id of the added entry
            
        Raises:
            ValueError: If entry already exists
        """
        if entry.entry_id in self.archives[ArchiveType.IMMUTABLE]:
            raise ValueError(f"Entry {entry.entry_id} already exists in immutable archive")
        
        # Compute and store hash for immutability verification
        entry_hash = self._compute_entry_hash(entry)
        self.immutable_hashes[entry.entry_id] = {
            'hash': entry_hash,
            'timestamp': entry.timestamp
        }
        
        # Add to archive
        self.archives[ArchiveType.IMMUTABLE][entry.entry_id] = entry
        
        # Persist to disk
        self._save_archive(ArchiveType.IMMUTABLE)
        self._save_immutable_hashes()
        
        return entry.entry_id
    
    def verify_immutable_integrity(self, entry_id: str) -> bool:
        """
        Verify that an immutable archive entry hasn't been tampered with.
        
        Args:
            entry_id: ID of entry to verify
            
        Returns:
            True if entry is intact, False if tampered
        """
        if entry_id not in self.archives[ArchiveType.IMMUTABLE]:
            return False
        
        if entry_id not in self.immutable_hashes:
            return False
        
        entry = self.archives[ArchiveType.IMMUTABLE][entry_id]
        current_hash = self._compute_entry_hash(entry)
        stored_hash = self.immutable_hashes[entry_id]['hash']
        
        return current_hash == stored_hash
    
    def create_educational_version(self, entry_id: str, filtered_content: str) -> str:
        """
        Create educational archive version from immutable entry.
        Applies trauma filtering while maintaining truth.
        
        Args:
            entry_id: ID of immutable archive entry
            filtered_content: Trauma-filtered version of content
            
        Returns:
            entry_id in educational archive
        """
        if entry_id not in self.archives[ArchiveType.IMMUTABLE]:
            raise ValueError(f"Entry {entry_id} not found in immutable archive")
        
        original = self.archives[ArchiveType.IMMUTABLE][entry_id]
        
        # Create educational version with reference to original
        edu_entry = MemoryEntry(
            content=filtered_content,
            metadata={
                **original.metadata,
                'source_entry_id': entry_id,
                'archive_type': 'educational',
                'filtered': True,
                'original_trauma_level': original.trauma_level
            },
            trauma_level=max(0.0, original.trauma_level - 0.3)  # Reduced trauma
        )
        
        self.archives[ArchiveType.EDUCATIONAL][edu_entry.entry_id] = edu_entry
        self._save_archive(ArchiveType.EDUCATIONAL)
        
        return edu_entry.entry_id
    
    def create_dynamic_version(self, entry_id: str, optimized_content: str, 
                              wellbeing_score: float) -> str:
        """
        Create dynamic archive version optimized for collective wellbeing.
        
        Args:
            entry_id: ID of source entry (immutable or educational)
            optimized_content: Content optimized for wellbeing
            wellbeing_score: 0.0-1.0 score indicating wellbeing optimization
            
        Returns:
            entry_id in dynamic archive
        """
        # Find source entry
        source_entry = None
        source_type = None
        
        for archive_type in [ArchiveType.IMMUTABLE, ArchiveType.EDUCATIONAL]:
            if entry_id in self.archives[archive_type]:
                source_entry = self.archives[archive_type][entry_id]
                source_type = archive_type
                break
        
        if source_entry is None:
            raise ValueError(f"Entry {entry_id} not found in any archive")
        
        # Create dynamic version
        dynamic_entry = MemoryEntry(
            content=optimized_content,
            metadata={
                **source_entry.metadata,
                'source_entry_id': entry_id,
                'source_archive': source_type.value,
                'archive_type': 'dynamic',
                'wellbeing_score': wellbeing_score,
                'optimized': True
            },
            trauma_level=max(0.0, source_entry.trauma_level - 0.5)  # Significant reduction
        )
        
        self.archives[ArchiveType.DYNAMIC][dynamic_entry.entry_id] = dynamic_entry
        self._save_archive(ArchiveType.DYNAMIC)
        
        return dynamic_entry.entry_id
    
    def get_entry(self, archive_type: ArchiveType, entry_id: str) -> Optional[MemoryEntry]:
        """
        Retrieve an entry from specified archive.
        
        Args:
            archive_type: Type of archive to search
            entry_id: ID of entry to retrieve
            
        Returns:
            MemoryEntry if found, None otherwise
        """
        return self.archives[archive_type].get(entry_id)
    
    def list_entries(self, archive_type: ArchiveType, 
                    max_trauma_level: Optional[float] = None) -> List[MemoryEntry]:
        """
        List all entries in an archive, optionally filtered by trauma level.
        
        Args:
            archive_type: Type of archive to list
            max_trauma_level: Maximum trauma level to include (None for all)
            
        Returns:
            List of MemoryEntry objects
        """
        entries = list(self.archives[archive_type].values())
        
        if max_trauma_level is not None:
            entries = [e for e in entries if e.trauma_level <= max_trauma_level]
        
        return entries
    
    def get_archive_stats(self) -> Dict[str, Any]:
        """Get statistics about all archives"""
        stats = {}
        for archive_type in ArchiveType:
            entries = self.archives[archive_type].values()
            if entries:
                avg_trauma = sum(e.trauma_level for e in entries) / len(entries)
            else:
                avg_trauma = 0.0
            
            stats[archive_type.value] = {
                'total_entries': len(entries),
                'average_trauma_level': avg_trauma
            }
        
        # Add immutability verification stats
        verified = sum(
            1 for entry_id in self.archives[ArchiveType.IMMUTABLE].keys()
            if self.verify_immutable_integrity(entry_id)
        )
        stats[ArchiveType.IMMUTABLE.value]['verified_entries'] = verified
        
        return stats
