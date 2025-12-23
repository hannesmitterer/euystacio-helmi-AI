"""
Access Control System for PDM NRE-002 Rule
Implements role-based access with temporal decay filtering.
"""

from enum import Enum
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import random


class UserRole(Enum):
    """User roles with different access privileges"""
    SURVIVOR = "survivor"  # Trauma survivors who may want to forget
    STUDENT = "student"  # Students requiring educational content
    MINOR_STUDENT = "minor_student"  # Students under 18
    RESEARCHER = "researcher"  # Researchers requiring complete testimonies
    VERIFIED_USER = "verified_user"  # Verified users (council, tutors)
    PUBLIC = "public"  # General public


class User:
    """Represents a user with role and learning progress"""
    
    def __init__(self, user_id: str, role: UserRole, 
                 cdr: float = 0.5, learning_progress: float = 0.0):
        """
        Initialize user.
        
        Args:
            user_id: Unique user identifier
            role: User's role
            cdr: Collective Distress Rating (0.0-1.0)
            learning_progress: Learning progress score (0.0-1.0)
        """
        self.user_id = user_id
        self.role = role
        self.cdr = cdr  # Higher CDR = more distress
        self.learning_progress = learning_progress
        self.access_history: List[Dict] = []
    
    def record_access(self, entry_id: str, archive_type: str, granted: bool):
        """Record access attempt for audit trail"""
        self.access_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'entry_id': entry_id,
            'archive_type': archive_type,
            'granted': granted
        })


class AccessController:
    """
    Controls access to different archive tiers based on user role and CDR.
    Implements Temporal Decay of Access (TDR) filtering.
    """
    
    def __init__(self):
        """Initialize access controller"""
        self.users: Dict[str, User] = {}
        self.access_log: List[Dict] = []
        
        # Define base access permissions by role
        self.role_permissions = {
            UserRole.VERIFIED_USER: {
                'immutable': True,
                'educational': True,
                'dynamic': True,
                'requires_tdr': False
            },
            UserRole.RESEARCHER: {
                'immutable': True,
                'educational': True,
                'dynamic': True,
                'requires_tdr': True,
                'min_learning_progress': 0.3
            },
            UserRole.SURVIVOR: {
                'immutable': False,
                'educational': True,
                'dynamic': True,
                'requires_tdr': False
            },
            UserRole.STUDENT: {
                'immutable': False,
                'educational': True,
                'dynamic': True,
                'requires_tdr': True
            },
            UserRole.MINOR_STUDENT: {
                'immutable': False,
                'educational': True,
                'dynamic': True,
                'requires_tdr': True,
                'max_trauma_level': 0.3
            },
            UserRole.PUBLIC: {
                'immutable': False,
                'educational': False,
                'dynamic': True,
                'requires_tdr': False
            }
        }
    
    def register_user(self, user: User):
        """Register a user in the system"""
        self.users[user.user_id] = user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by ID"""
        return self.users.get(user_id)
    
    def calculate_tdr_factor(self, user: User, entry_trauma_level: float) -> float:
        """
        Calculate Temporal Decay of Access (TDR) factor.
        Regulates access level based on user's CDR and entry trauma.
        
        Args:
            user: User requesting access
            entry_trauma_level: Trauma level of requested entry
            
        Returns:
            TDR factor (0.0-1.0): probability of granting access
        """
        # Base TDR calculation
        # Lower CDR and higher learning progress = higher access probability
        distress_factor = 1.0 - user.cdr
        learning_factor = user.learning_progress
        trauma_factor = 1.0 - entry_trauma_level
        
        # Weighted combination
        tdr = (distress_factor * 0.4 + 
               learning_factor * 0.4 + 
               trauma_factor * 0.2)
        
        # Ensure bounds
        return max(0.0, min(1.0, tdr))
    
    def check_access(self, user_id: str, entry_id: str, 
                    archive_type: str, entry_trauma_level: float) -> Dict:
        """
        Check if user has access to a specific entry.
        
        Args:
            user_id: ID of user requesting access
            entry_id: ID of entry being requested
            archive_type: Type of archive (AI, AD, ADi)
            entry_trauma_level: Trauma level of the entry
            
        Returns:
            Dict with 'granted' (bool), 'reason' (str), 'tdr_factor' (float)
        """
        user = self.get_user(user_id)
        if not user:
            return {
                'granted': False,
                'reason': 'User not found',
                'tdr_factor': 0.0,
                'explanation': 'You must be registered to access archives.'
            }
        
        # Get role permissions
        perms = self.role_permissions[user.role]
        
        # Map archive type to permission key
        archive_key_map = {
            'AI': 'immutable',
            'AD': 'educational',
            'ADi': 'dynamic'
        }
        archive_key = archive_key_map.get(archive_type)
        
        if not archive_key:
            return {
                'granted': False,
                'reason': 'Invalid archive type',
                'tdr_factor': 0.0,
                'explanation': 'The requested archive type does not exist.'
            }
        
        # Check base permission
        if not perms.get(archive_key, False):
            user.record_access(entry_id, archive_type, False)
            return {
                'granted': False,
                'reason': f'Role {user.role.value} does not have access to {archive_type} archive',
                'tdr_factor': 0.0,
                'explanation': self._generate_denial_explanation(user, archive_type)
            }
        
        # Check trauma level restrictions (e.g., for minors)
        max_trauma = perms.get('max_trauma_level')
        if max_trauma is not None and entry_trauma_level > max_trauma:
            user.record_access(entry_id, archive_type, False)
            return {
                'granted': False,
                'reason': f'Entry trauma level {entry_trauma_level} exceeds maximum {max_trauma} for role',
                'tdr_factor': 0.0,
                'explanation': (
                    f'This content has been filtered for your protection. '
                    f'The trauma level is too high for {user.role.value}s. '
                    f'Please access the Dynamic Archive (ADi) for optimized content.'
                )
            }
        
        # Check learning progress requirements
        min_progress = perms.get('min_learning_progress', 0.0)
        if user.learning_progress < min_progress:
            user.record_access(entry_id, archive_type, False)
            return {
                'granted': False,
                'reason': f'Insufficient learning progress: {user.learning_progress} < {min_progress}',
                'tdr_factor': 0.0,
                'explanation': (
                    f'Your learning progress ({user.learning_progress:.1%}) is below '
                    f'the required threshold ({min_progress:.1%}) for accessing this archive. '
                    f'Continue your educational journey to unlock deeper access.'
                )
            }
        
        # Apply TDR filter if required
        if perms.get('requires_tdr', False):
            tdr_factor = self.calculate_tdr_factor(user, entry_trauma_level)
            
            # Probabilistic access based on TDR
            if random.random() > tdr_factor:
                user.record_access(entry_id, archive_type, False)
                return {
                    'granted': False,
                    'reason': f'TDR filter denied access (factor: {tdr_factor:.2f})',
                    'tdr_factor': tdr_factor,
                    'explanation': (
                        f'Access temporarily restricted based on your current distress level '
                        f'and learning progress. Try again later or access alternative archives.'
                    )
                }
        else:
            tdr_factor = 1.0
        
        # Access granted
        user.record_access(entry_id, archive_type, True)
        self._log_access(user, entry_id, archive_type, True, tdr_factor)
        
        return {
            'granted': True,
            'reason': 'Access granted',
            'tdr_factor': tdr_factor,
            'explanation': 'You have been granted access to this memory.'
        }
    
    def _generate_denial_explanation(self, user: User, archive_type: str) -> str:
        """Generate user-friendly explanation for access denial"""
        explanations = {
            'AI': {
                UserRole.SURVIVOR: (
                    'The Immutable Archive contains unfiltered historical testimonies. '
                    'As a survivor, you have the right to access trauma-reduced versions '
                    'in the Educational or Dynamic Archives. This protects your wellbeing '
                    'while preserving historical truth for verified researchers.'
                ),
                UserRole.STUDENT: (
                    'The Immutable Archive is reserved for verified researchers and '
                    'institutional users. Educational content is available in the '
                    'Educational Archive (AD), which maintains truth while reducing '
                    'unnecessary traumatic detail.'
                ),
                UserRole.MINOR_STUDENT: (
                    'The Immutable Archive contains content that may not be appropriate '
                    'for minors. Age-appropriate educational materials are available in '
                    'the Educational and Dynamic Archives.'
                ),
                UserRole.PUBLIC: (
                    'The Immutable Archive requires verification for access. Public users '
                    'can access the Dynamic Archive (ADi) which provides optimized content '
                    'for general audiences.'
                )
            }
        }
        
        return explanations.get(archive_type, {}).get(
            user.role,
            f'Your role ({user.role.value}) does not have permission to access this archive.'
        )
    
    def _log_access(self, user: User, entry_id: str, archive_type: str, 
                   granted: bool, tdr_factor: float):
        """Log access attempt for auditing"""
        self.access_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user.user_id,
            'user_role': user.role.value,
            'entry_id': entry_id,
            'archive_type': archive_type,
            'granted': granted,
            'tdr_factor': tdr_factor,
            'cdr': user.cdr,
            'learning_progress': user.learning_progress
        })
    
    def get_access_statistics(self, user_id: Optional[str] = None) -> Dict:
        """
        Get access statistics, optionally for a specific user.
        
        Args:
            user_id: Optional user ID to filter by
            
        Returns:
            Dictionary of access statistics
        """
        logs = self.access_log
        if user_id:
            logs = [log for log in logs if log['user_id'] == user_id]
        
        if not logs:
            return {
                'total_requests': 0,
                'granted': 0,
                'denied': 0,
                'grant_rate': 0.0
            }
        
        granted = sum(1 for log in logs if log['granted'])
        denied = len(logs) - granted
        
        return {
            'total_requests': len(logs),
            'granted': granted,
            'denied': denied,
            'grant_rate': granted / len(logs) if logs else 0.0,
            'average_tdr': sum(log['tdr_factor'] for log in logs) / len(logs),
            'by_archive': self._stats_by_archive(logs)
        }
    
    def _stats_by_archive(self, logs: List[Dict]) -> Dict:
        """Get statistics broken down by archive type"""
        stats = {}
        for archive_type in ['AI', 'AD', 'ADi']:
            archive_logs = [log for log in logs if log['archive_type'] == archive_type]
            if archive_logs:
                granted = sum(1 for log in archive_logs if log['granted'])
                stats[archive_type] = {
                    'total': len(archive_logs),
                    'granted': granted,
                    'denied': len(archive_logs) - granted,
                    'grant_rate': granted / len(archive_logs)
                }
            else:
                stats[archive_type] = {
                    'total': 0,
                    'granted': 0,
                    'denied': 0,
                    'grant_rate': 0.0
                }
        return stats
