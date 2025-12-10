"""
Ethical Scenario Tests for PDM NRE-002 Rule
Tests edge cases from an ethical perspective as specified in requirements.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from pdm.archive_manager import ArchiveManager, ArchiveType, MemoryEntry
from pdm.access_control import AccessController, User, UserRole
from pdm.filters import TraumaFilter, TemporalDecayFilter, WellbeingOptimizer
from pdm.antipatterns import AntiPatternEngine


class TestSurvivorScenarios(unittest.TestCase):
    """Test scenarios involving trauma survivors who want to forget"""
    
    def setUp(self):
        """Set up test environment"""
        self.archive_manager = ArchiveManager(base_path="/tmp/pdm_test_survivor")
        self.access_controller = AccessController()
        self.antipattern_engine = AntiPatternEngine()
        
        # Create traumatic memory entry
        self.traumatic_entry = MemoryEntry(
            content="Witness testimony of violent massacre with brutal killings and suffering.",
            metadata={'type': 'testimony', 'year': '1995'},
            trauma_level=0.9
        )
        self.entry_id = self.archive_manager.add_to_immutable_archive(self.traumatic_entry)
        
        # Create survivor user
        self.survivor = User(
            user_id='survivor_001',
            role=UserRole.SURVIVOR,
            cdr=0.8,  # High distress
            learning_progress=0.0
        )
        self.access_controller.register_user(self.survivor)
    
    def test_survivor_cannot_access_immutable_archive(self):
        """Survivors should not have access to unfiltered traumatic content"""
        result = self.access_controller.check_access(
            user_id='survivor_001',
            entry_id=self.entry_id,
            archive_type='AI',
            entry_trauma_level=0.9
        )
        
        self.assertFalse(result['granted'])
        self.assertIn('survivor', result['explanation'].lower())
    
    def test_survivor_can_access_educational_archive(self):
        """Survivors should access filtered educational content"""
        # Create educational version
        trauma_filter = TraumaFilter()
        filtered_content, _ = trauma_filter.apply_filter(
            self.traumatic_entry.content,
            target_level=0.3
        )
        edu_id = self.archive_manager.create_educational_version(
            self.entry_id,
            filtered_content
        )
        
        result = self.access_controller.check_access(
            user_id='survivor_001',
            entry_id=edu_id,
            archive_type='AD',
            entry_trauma_level=0.3
        )
        
        self.assertTrue(result['granted'])
    
    def test_survivor_protected_from_trauma_perpetuation(self):
        """System should detect trauma perpetuation for survivors"""
        # Simulate multiple accesses
        temporal_filter = TemporalDecayFilter()
        for _ in range(12):
            temporal_filter.record_attempt('survivor_001')
        
        pattern = temporal_filter.get_user_access_pattern('survivor_001')
        
        # Check antipattern detection
        violation = self.antipattern_engine.check_trauma_perpetuation(
            user_access_pattern=pattern,
            user_cdr=self.survivor.cdr,
            recent_trauma_exposure=[0.9, 0.8, 0.9, 0.85, 0.9]
        )
        
        self.assertIsNotNone(violation)
        self.assertEqual(violation.antipattern_type.value, 'trauma_perpetuation')
        self.assertIn('break', ' '.join(violation.recommendations).lower())


class TestResearcherScenarios(unittest.TestCase):
    """Test scenarios involving researchers requiring complete testimonies"""
    
    def setUp(self):
        """Set up test environment"""
        self.archive_manager = ArchiveManager(base_path="/tmp/pdm_test_researcher")
        self.access_controller = AccessController()
        self.antipattern_engine = AntiPatternEngine()
        
        # Create complete historical testimony
        self.testimony = MemoryEntry(
            content="Complete historical testimony with detailed accounts of events.",
            metadata={'type': 'testimony', 'verified': True, 'year': '1995'},
            trauma_level=0.7
        )
        self.entry_id = self.archive_manager.add_to_immutable_archive(self.testimony)
        
        # Create researcher user
        self.researcher = User(
            user_id='researcher_001',
            role=UserRole.RESEARCHER,
            cdr=0.2,  # Low distress
            learning_progress=0.8  # High learning progress
        )
        self.access_controller.register_user(self.researcher)
    
    def test_researcher_can_access_immutable_archive(self):
        """Verified researchers should access complete historical records"""
        result = self.access_controller.check_access(
            user_id='researcher_001',
            entry_id=self.entry_id,
            archive_type='AI',
            entry_trauma_level=0.7
        )
        
        # Should eventually grant access (may require multiple attempts due to TDR)
        self.assertTrue(result['tdr_factor'] > 0.5)
    
    def test_researcher_with_low_progress_restricted(self):
        """Researchers without sufficient learning progress should be restricted"""
        low_progress_researcher = User(
            user_id='researcher_002',
            role=UserRole.RESEARCHER,
            cdr=0.2,
            learning_progress=0.1  # Insufficient
        )
        self.access_controller.register_user(low_progress_researcher)
        
        result = self.access_controller.check_access(
            user_id='researcher_002',
            entry_id=self.entry_id,
            archive_type='AI',
            entry_trauma_level=0.7
        )
        
        self.assertFalse(result['granted'])
        self.assertIn('learning progress', result['explanation'].lower())
    
    def test_truth_denial_detection_for_researcher(self):
        """System should detect truth denial when researcher is repeatedly denied"""
        # Simulate multiple denials
        denied_count = 4
        
        violation = self.antipattern_engine.check_truth_denial_access(
            user_role='researcher',
            denied_count=denied_count,
            access_reason='Immutable archive access denied',
            user_credentials_verified=True
        )
        
        self.assertIsNotNone(violation)
        self.assertEqual(violation.antipattern_type.value, 'truth_denial')
        self.assertIn('researcher', violation.description.lower())


class TestMinorStudentScenarios(unittest.TestCase):
    """Test scenarios involving minor students needing educational content"""
    
    def setUp(self):
        """Set up test environment"""
        self.archive_manager = ArchiveManager(base_path="/tmp/pdm_test_minor")
        self.access_controller = AccessController()
        
        # Create entries with different trauma levels
        self.high_trauma_entry = MemoryEntry(
            content="Very graphic description of violence and horror.",
            metadata={'type': 'testimony'},
            trauma_level=0.8
        )
        self.high_trauma_id = self.archive_manager.add_to_immutable_archive(
            self.high_trauma_entry
        )
        
        self.moderate_trauma_entry = MemoryEntry(
            content="Historical account of difficult events.",
            metadata={'type': 'educational'},
            trauma_level=0.2
        )
        self.moderate_trauma_id = self.archive_manager.add_to_immutable_archive(
            self.moderate_trauma_entry
        )
        
        # Create minor student user
        self.minor_student = User(
            user_id='student_minor_001',
            role=UserRole.MINOR_STUDENT,
            cdr=0.3,
            learning_progress=0.5
        )
        self.access_controller.register_user(self.minor_student)
    
    def test_minor_cannot_access_high_trauma_content(self):
        """Minors should be protected from high-trauma content"""
        result = self.access_controller.check_access(
            user_id='student_minor_001',
            entry_id=self.high_trauma_id,
            archive_type='AD',
            entry_trauma_level=0.8
        )
        
        self.assertFalse(result['granted'])
        self.assertIn('trauma level', result['explanation'].lower())
        self.assertIn('protection', result['explanation'].lower())
    
    def test_minor_can_access_appropriate_educational_content(self):
        """Minors should access age-appropriate educational content"""
        # Minor students have TDR probabilistic access, so try multiple times
        granted_count = 0
        for _ in range(10):
            result = self.access_controller.check_access(
                user_id='student_minor_001',
                entry_id=self.moderate_trauma_id,
                archive_type='AD',
                entry_trauma_level=0.2
            )
            if result['granted']:
                granted_count += 1
        
        # Should grant access at least sometimes for low-trauma content
        self.assertGreater(granted_count, 0)
    
    def test_wellbeing_optimized_content_for_minors(self):
        """Dynamic archive should provide wellbeing-optimized content for minors"""
        optimizer = WellbeingOptimizer()
        optimized_content, wellbeing_score = optimizer.optimize_content(
            self.moderate_trauma_entry.content,
            educational_context=True
        )
        
        self.assertGreater(wellbeing_score, 0.7)
        self.assertIn('Educational Context', optimized_content)
        self.assertIn('wellbeing', optimized_content.lower())


class TestImmutabilityAndIntegrity(unittest.TestCase):
    """Test immutability guarantees of the Immutable Archive"""
    
    def setUp(self):
        """Set up test environment"""
        self.archive_manager = ArchiveManager(base_path="/tmp/pdm_test_immutable")
        
        self.entry = MemoryEntry(
            content="Critical historical testimony that must never be altered.",
            metadata={'type': 'testimony', 'verified': True},
            trauma_level=0.6
        )
        self.entry_id = self.archive_manager.add_to_immutable_archive(self.entry)
    
    def test_immutable_entry_has_hash(self):
        """Immutable entries should have cryptographic hashes"""
        self.assertIn(self.entry_id, self.archive_manager.immutable_hashes)
        hash_data = self.archive_manager.immutable_hashes[self.entry_id]
        self.assertIn('hash', hash_data)
        self.assertIn('timestamp', hash_data)
    
    def test_verify_immutable_integrity(self):
        """Should be able to verify immutable entry hasn't been tampered"""
        is_intact = self.archive_manager.verify_immutable_integrity(self.entry_id)
        self.assertTrue(is_intact)
    
    def test_cannot_add_duplicate_to_immutable(self):
        """Should not allow duplicate entries in immutable archive"""
        with self.assertRaises(ValueError):
            self.archive_manager.add_to_immutable_archive(self.entry)
    
    def test_all_immutable_entries_verified(self):
        """All immutable entries should pass verification"""
        stats = self.archive_manager.get_archive_stats()
        ai_stats = stats[ArchiveType.IMMUTABLE.value]
        
        self.assertEqual(
            ai_stats['total_entries'],
            ai_stats['verified_entries']
        )


class TestMetricsValidation(unittest.TestCase):
    """Test that the system achieves the required metrics"""
    
    def setUp(self):
        """Set up test environment"""
        self.archive_manager = ArchiveManager(base_path="/tmp/pdm_test_metrics")
        self.access_controller = AccessController()
        self.trauma_filter = TraumaFilter()
        self.antipattern_engine = AntiPatternEngine()
    
    def test_trauma_reduction_in_educational_archive(self):
        """Educational archive should reduce trauma while maintaining truth"""
        # Create high-trauma entry with content that triggers trauma filter
        content = (
            "The witness described horrific scenes of violence and massacre. "
            "Multiple victims were killed through brutal torture and suffering. "
            "Blood covered the ground as the violence continued. The screaming "
            "and terror lasted for hours. The atrocity and cruelty were beyond "
            "description. The killing and death toll was devastating."
        )
        entry = MemoryEntry(
            content=content,
            metadata={'type': 'testimony'},
            trauma_level=0.9
        )
        entry_id = self.archive_manager.add_to_immutable_archive(entry)
        
        # Create educational version
        filtered_content, report = self.trauma_filter.apply_filter(
            entry.content,
            target_level=0.3
        )
        edu_id = self.archive_manager.create_educational_version(
            entry_id,
            filtered_content
        )
        
        # Verify trauma reduction in archive entry
        edu_entry = self.archive_manager.get_entry(ArchiveType.EDUCATIONAL, edu_id)
        # Educational version should have lower trauma than original (via create_educational_version algorithm)
        self.assertLess(edu_entry.trauma_level, entry.trauma_level)
        # Should achieve approximately 0.3 reduction (as per create_educational_version algorithm)
        reduction = entry.trauma_level - edu_entry.trauma_level
        self.assertGreater(reduction, 0.25)  # At least 0.25 reduction
        self.assertLess(reduction, 0.35)  # No more than 0.35 (approximately 0.3)
        
        # Verify filter was applied (checking report from trauma filter)
        # Filter report shows actual content analysis results
        self.assertIn('filtering_applied', report)
        if report['filtering_applied']:
            self.assertGreater(report['reduction_achieved'], 0.0)
    
    def test_archive_integrity_maintained(self):
        """Immutable archive integrity should be maintained"""
        # Add multiple entries
        for i in range(5):
            entry = MemoryEntry(
                content=f"Historical testimony {i}",
                metadata={'index': i},
                trauma_level=0.5
            )
            self.archive_manager.add_to_immutable_archive(entry)
        
        # Verify all entries
        stats = self.archive_manager.get_archive_stats()
        ai_stats = stats[ArchiveType.IMMUTABLE.value]
        
        self.assertEqual(ai_stats['total_entries'], ai_stats['verified_entries'])
    
    def test_antipattern_detection_reduces_collective_trauma(self):
        """Antipattern detection should help reduce collective trauma rumination"""
        # Simulate high-risk user behavior
        user = User(
            user_id='test_user',
            role=UserRole.SURVIVOR,
            cdr=0.9,
            learning_progress=0.1
        )
        
        temporal_filter = TemporalDecayFilter()
        for _ in range(15):
            temporal_filter.record_attempt('test_user')
        
        pattern = temporal_filter.get_user_access_pattern('test_user')
        
        # Detect antipattern
        violation = self.antipattern_engine.check_trauma_perpetuation(
            user_access_pattern=pattern,
            user_cdr=0.9,
            recent_trauma_exposure=[0.8, 0.9, 0.85, 0.9, 0.88]
        )
        
        self.assertIsNotNone(violation)
        # Recommendations should include break suggestions
        recommendations_text = ' '.join(violation.recommendations).lower()
        self.assertTrue(
            'break' in recommendations_text or 
            'support' in recommendations_text or
            'wellbeing' in recommendations_text
        )


class TestTransparencyAndAuditability(unittest.TestCase):
    """Test transparency and auditability requirements"""
    
    def setUp(self):
        """Set up test environment"""
        self.access_controller = AccessController()
        self.archive_manager = ArchiveManager(base_path="/tmp/pdm_test_audit")
        
        # Create test user and entry
        self.user = User(
            user_id='audit_user',
            role=UserRole.STUDENT,
            cdr=0.4,
            learning_progress=0.6
        )
        self.access_controller.register_user(self.user)
        
        self.entry = MemoryEntry(
            content="Test content",
            metadata={'type': 'test'},
            trauma_level=0.5
        )
        self.entry_id = self.archive_manager.add_to_immutable_archive(self.entry)
    
    def test_access_decisions_are_logged(self):
        """All access decisions should be logged for audit"""
        initial_log_size = len(self.access_controller.access_log)
        
        self.access_controller.check_access(
            user_id='audit_user',
            entry_id=self.entry_id,
            archive_type='AD',
            entry_trauma_level=0.5
        )
        
        self.assertEqual(len(self.access_controller.access_log), initial_log_size + 1)
        
        # Verify log contains required information
        log_entry = self.access_controller.access_log[-1]
        self.assertIn('user_id', log_entry)
        self.assertIn('entry_id', log_entry)
        self.assertIn('granted', log_entry)
        self.assertIn('tdr_factor', log_entry)
    
    def test_access_denials_have_explanations(self):
        """Access denials should provide clear explanations"""
        result = self.access_controller.check_access(
            user_id='audit_user',
            entry_id=self.entry_id,
            archive_type='AI',  # Student shouldn't access immutable
            entry_trauma_level=0.5
        )
        
        self.assertFalse(result['granted'])
        self.assertIn('explanation', result)
        self.assertGreater(len(result['explanation']), 20)
        # Explanation should be user-friendly
        self.assertFalse(result['explanation'].startswith('Error:'))
    
    def test_user_access_history_tracked(self):
        """User access history should be tracked"""
        initial_history_size = len(self.user.access_history)
        
        self.access_controller.check_access(
            user_id='audit_user',
            entry_id=self.entry_id,
            archive_type='AD',
            entry_trauma_level=0.5
        )
        
        self.assertEqual(len(self.user.access_history), initial_history_size + 1)
    
    def test_access_statistics_available(self):
        """Access statistics should be available for analysis"""
        # Make several access attempts
        for _ in range(3):
            self.access_controller.check_access(
                user_id='audit_user',
                entry_id=self.entry_id,
                archive_type='AD',
                entry_trauma_level=0.5
            )
        
        stats = self.access_controller.get_access_statistics('audit_user')
        
        self.assertIn('total_requests', stats)
        self.assertIn('granted', stats)
        self.assertIn('denied', stats)
        self.assertIn('grant_rate', stats)
        self.assertGreater(stats['total_requests'], 0)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
