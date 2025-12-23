"""
PDM System - Main Integration Module
Integrates all PDM components and provides high-level API.
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .archive_manager import ArchiveManager, ArchiveType, MemoryEntry
from .access_control import AccessController, User, UserRole
from .filters import TraumaFilter, TemporalDecayFilter, WellbeingOptimizer
from .antipatterns import AntiPatternEngine, AntiPatternViolation


class PDMSystem:
    """
    Main PDM (Protocollo di Depurazione della Memoria) System
    Implements NRE-002 rule for stratified memory management.
    """
    
    def __init__(self, base_path: str = "pdm", red_code_path: str = "red_code.json"):
        """
        Initialize PDM system.
        
        Args:
            base_path: Base directory for PDM data
            red_code_path: Path to Red Code integration file
        """
        self.base_path = base_path
        self.red_code_path = red_code_path
        
        # Initialize components
        self.archive_manager = ArchiveManager(base_path=os.path.join(base_path, "archives"))
        self.access_controller = AccessController()
        self.trauma_filter = TraumaFilter()
        self.temporal_filter = TemporalDecayFilter()
        self.wellbeing_optimizer = WellbeingOptimizer()
        self.antipattern_engine = AntiPatternEngine()
        
        # Integration state
        self.system_active = True
        self.integration_log: List[Dict] = []
        
        self._integrate_with_red_code()
    
    def _integrate_with_red_code(self):
        """Integrate PDM with existing Red Code system"""
        try:
            if os.path.exists(self.red_code_path):
                with open(self.red_code_path, 'r', encoding='utf-8') as f:
                    red_code = json.load(f)
                
                # Add PDM integration marker
                if 'pdm_integration' not in red_code:
                    red_code['pdm_integration'] = {
                        'version': '1.0.0',
                        'rule': 'NRE-002',
                        'activated': datetime.utcnow().isoformat(),
                        'status': 'active'
                    }
                    
                    with open(self.red_code_path, 'w', encoding='utf-8') as f:
                        json.dump(red_code, f, indent=2, ensure_ascii=False)
                    
                    self._log_integration('PDM integrated with Red Code system')
        except Exception as e:
            self._log_integration(f'Red Code integration warning: {e}')
    
    def _log_integration(self, message: str):
        """Log integration events"""
        self.integration_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'message': message
        })
    
    def add_memory(self, content: str, metadata: Dict, 
                  auto_process: bool = True) -> Dict:
        """
        Add new memory to the system.
        Automatically creates immutable, educational, and dynamic versions.
        
        Args:
            content: Memory content
            metadata: Metadata about the memory
            auto_process: Whether to automatically create filtered versions
            
        Returns:
            Dictionary with entry IDs for all archive types
        """
        # Analyze trauma level
        trauma_level = self.trauma_filter.analyze_trauma_level(content)
        
        # Create immutable entry
        entry = MemoryEntry(content, metadata, trauma_level)
        immutable_id = self.archive_manager.add_to_immutable_archive(entry)
        
        result = {
            'immutable_id': immutable_id,
            'trauma_level': trauma_level,
            'educational_id': None,
            'dynamic_id': None
        }
        
        if auto_process:
            # Create educational version
            filtered_content, filter_report = self.trauma_filter.apply_filter(
                content, target_level=0.3
            )
            edu_id = self.archive_manager.create_educational_version(
                immutable_id, filtered_content
            )
            result['educational_id'] = edu_id
            result['filter_report'] = filter_report
            
            # Create dynamic version
            optimized_content, wellbeing_score = self.wellbeing_optimizer.optimize_content(
                filtered_content, educational_context=True
            )
            dynamic_id = self.archive_manager.create_dynamic_version(
                edu_id, optimized_content, wellbeing_score
            )
            result['dynamic_id'] = dynamic_id
            result['wellbeing_score'] = wellbeing_score
            
            # Check for truth denial through excessive filtering
            violation = self.antipattern_engine.check_truth_denial_filtering(
                original_trauma=trauma_level,
                filtered_trauma=trauma_level - filter_report['reduction_achieved'],
                important_context_removed=filter_report['replacements_made'] > 10
            )
            if violation:
                result['antipattern_warning'] = violation.to_dict()
        
        return result
    
    def request_access(self, user_id: str, entry_id: str, 
                      archive_type: str) -> Dict:
        """
        Process access request with full ethical checks.
        
        Args:
            user_id: User requesting access
            entry_id: ID of entry being requested
            archive_type: Type of archive (AI, AD, or ADi)
            
        Returns:
            Access decision with content if granted
        """
        # Get user
        user = self.access_controller.get_user(user_id)
        if not user:
            return {
                'granted': False,
                'error': 'User not found',
                'content': None
            }
        
        # Get entry to determine trauma level
        archive_type_enum = {
            'AI': ArchiveType.IMMUTABLE,
            'AD': ArchiveType.EDUCATIONAL,
            'ADi': ArchiveType.DYNAMIC
        }.get(archive_type)
        
        if not archive_type_enum:
            return {
                'granted': False,
                'error': 'Invalid archive type',
                'content': None
            }
        
        entry = self.archive_manager.get_entry(archive_type_enum, entry_id)
        if not entry:
            return {
                'granted': False,
                'error': 'Entry not found',
                'content': None
            }
        
        # Record access attempt for temporal tracking
        self.temporal_filter.record_attempt(user_id)
        
        # Check for rumination warning
        if self.temporal_filter.should_suggest_break(user_id):
            rumination_warning = (
                "You've been accessing memory archives frequently. "
                "Consider taking a break to protect your wellbeing. "
                "Support resources are available."
            )
        else:
            rumination_warning = None
        
        # Check access
        access_result = self.access_controller.check_access(
            user_id=user_id,
            entry_id=entry_id,
            archive_type=archive_type,
            entry_trauma_level=entry.trauma_level
        )
        
        # Check for antipatterns
        user_pattern = self.temporal_filter.get_user_access_pattern(user_id)
        
        # Get recent trauma exposure
        recent_trauma = self._get_recent_trauma_exposure(user_id)
        
        trauma_violation = self.antipattern_engine.check_trauma_perpetuation(
            user_access_pattern=user_pattern,
            user_cdr=user.cdr,
            recent_trauma_exposure=recent_trauma
        )
        
        # Check for truth denial if researcher denied
        if not access_result['granted'] and user.role == UserRole.RESEARCHER:
            user_stats = self.access_controller.get_access_statistics(user_id)
            denied_count = user_stats.get('denied', 0)
            
            truth_violation = self.antipattern_engine.check_truth_denial_access(
                user_role=user.role.value,
                denied_count=denied_count,
                access_reason=access_result['reason'],
                user_credentials_verified=user.role == UserRole.VERIFIED_USER
            )
        else:
            truth_violation = None
        
        # Build response
        response = {
            'granted': access_result['granted'],
            'reason': access_result['reason'],
            'explanation': access_result['explanation'],
            'tdr_factor': access_result['tdr_factor'],
            'content': entry.to_dict() if access_result['granted'] else None,
            'rumination_warning': rumination_warning,
            'antipattern_warnings': []
        }
        
        if trauma_violation:
            response['antipattern_warnings'].append(trauma_violation.to_dict())
        if truth_violation:
            response['antipattern_warnings'].append(truth_violation.to_dict())
        
        return response
    
    def _get_recent_trauma_exposure(self, user_id: str) -> List[float]:
        """Get recent trauma exposure levels for a user"""
        user = self.access_controller.get_user(user_id)
        if not user or not user.access_history:
            return []
        
        # Get last 10 accesses
        recent = user.access_history[-10:]
        trauma_levels = []
        
        for access in recent:
            if access['granted']:
                # Try to find the entry and get its trauma level
                for archive_type in ArchiveType:
                    entry = self.archive_manager.get_entry(
                        archive_type, access['entry_id']
                    )
                    if entry:
                        trauma_levels.append(entry.trauma_level)
                        break
        
        return trauma_levels
    
    def register_user(self, user_id: str, role: str, cdr: float = 0.5,
                     learning_progress: float = 0.0) -> User:
        """
        Register a new user in the system.
        
        Args:
            user_id: Unique user identifier
            role: User role (survivor, student, minor_student, researcher, verified_user, public)
            cdr: Collective Distress Rating (0.0-1.0)
            learning_progress: Learning progress (0.0-1.0)
            
        Returns:
            Created User object
        """
        role_enum = UserRole[role.upper()]
        user = User(user_id, role_enum, cdr, learning_progress)
        self.access_controller.register_user(user)
        return user
    
    def get_system_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        archive_stats = self.archive_manager.get_archive_stats()
        access_stats = self.access_controller.get_access_statistics()
        filter_stats = self.trauma_filter.get_filter_statistics()
        antipattern_stats = self.antipattern_engine.get_violation_statistics()
        
        return {
            'system_status': 'active' if self.system_active else 'inactive',
            'archives': archive_stats,
            'access_control': access_stats,
            'filtering': filter_stats,
            'antipatterns': antipattern_stats,
            'integration': {
                'red_code_integrated': os.path.exists(self.red_code_path),
                'events_logged': len(self.integration_log)
            }
        }
    
    def generate_transparency_report(self) -> str:
        """Generate human-readable transparency report"""
        stats = self.get_system_statistics()
        
        report = "=" * 60 + "\n"
        report += "PDM (Protocollo di Depurazione della Memoria) System Report\n"
        report += "NRE-002 Rule Implementation\n"
        report += "=" * 60 + "\n\n"
        
        report += "ARCHIVE STATISTICS:\n"
        for archive_type, data in stats['archives'].items():
            report += f"  {archive_type}:\n"
            report += f"    - Total Entries: {data['total_entries']}\n"
            report += f"    - Avg Trauma Level: {data['average_trauma_level']:.2f}\n"
            if 'verified_entries' in data:
                report += f"    - Verified Entries: {data['verified_entries']}\n"
        
        report += "\nACCESS CONTROL STATISTICS:\n"
        report += f"  - Total Requests: {stats['access_control']['total_requests']}\n"
        report += f"  - Granted: {stats['access_control']['granted']}\n"
        report += f"  - Denied: {stats['access_control']['denied']}\n"
        report += f"  - Grant Rate: {stats['access_control']['grant_rate']:.1%}\n"
        
        report += "\nFILTERING STATISTICS:\n"
        report += f"  - Total Filterings: {stats['filtering']['total_filterings']}\n"
        report += f"  - Avg Trauma Reduction: {stats['filtering']['average_reduction']:.2f}\n"
        report += f"  - Avg Replacements: {stats['filtering']['average_replacements']:.1f}\n"
        
        report += "\nANTIPATTERN DETECTION:\n"
        report += f"  - Total Violations: {stats['antipatterns']['total_violations']}\n"
        report += f"  - Trauma Perpetuation: {stats['antipatterns']['trauma_perpetuation']}\n"
        report += f"  - Truth Denial: {stats['antipatterns']['truth_denial']}\n"
        
        report += "\nSeverity Breakdown:\n"
        for severity, count in stats['antipatterns']['by_severity'].items():
            report += f"  - {severity.capitalize()}: {count}\n"
        
        report += "\n" + self.antipattern_engine.generate_report()
        
        return report
    
    def export_audit_log(self, filepath: str):
        """Export complete audit log for transparency"""
        audit_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'system_statistics': self.get_system_statistics(),
            'access_log': self.access_controller.access_log,
            'integration_log': self.integration_log,
            'antipattern_violations': [
                v.to_dict() for v in self.antipattern_engine.get_all_violations()
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(audit_data, f, indent=2, ensure_ascii=False)
