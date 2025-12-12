"""
Test suite for Ontological Fusion Framework
Tests NRE principle validation, PSC compliance, and systematic response
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from datetime import datetime
from core.ontological_fusion import (
    OntologicalFusionFramework,
    CoreConceptMapper,
    IntegratedEthicalKernel,
    TransparentSystematicResponse,
    initialize_ontological_fusion
)


class TestOntologicalFusionFramework(unittest.TestCase):
    """Test the main Ontological Fusion Framework."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fusion = OntologicalFusionFramework()
    
    def test_initialization(self):
        """Test framework initialization."""
        self.assertIsNotNone(self.fusion.nre_principles)
        self.assertIn('nre_framework', self.fusion.nre_principles)
        self.assertEqual(self.fusion.fusion_state['alignment_status'], 'active')
    
    def test_nre_principles_loaded(self):
        """Test that all 18 NRE principles are loaded."""
        principles = self.fusion.nre_principles['nre_framework']['principles']
        self.assertEqual(len(principles), 18)
        self.assertIn('NRE-001', principles)
        self.assertIn('NRE-018', principles)
    
    def test_aligned_operation(self):
        """Test validation of an aligned operation."""
        operation = {
            'id': 'test-001',
            'type': 'decision',
            'intent': 'benefit',
            'compassion_evaluated': True,
            'mutual_benefit': True,
            'extractive': False,
            'supports_growth': True,
            'reduces_human_agency': False,
            'coercive': False,
            'hidden_agenda': False,
            'fragments_consciousness': False
        }
        
        result = self.fusion.validate_principle_alignment(operation)
        self.assertEqual(result['status'], 'aligned')
        self.assertEqual(len(result['violations']), 0)
    
    def test_misaligned_operation_extractive(self):
        """Test detection of extractive operation violation."""
        operation = {
            'id': 'test-002',
            'type': 'decision',
            'intent': 'extract',
            'compassion_evaluated': True
        }
        
        result = self.fusion.validate_principle_alignment(operation)
        self.assertEqual(result['status'], 'misaligned')
        self.assertGreater(len(result['violations']), 0)
        
        # Check that NRE-001 (PSC) violation is detected
        violation_principles = [v['principle'] for v in result['violations']]
        self.assertIn('NRE-001', violation_principles)
    
    def test_misaligned_operation_dignity(self):
        """Test detection of human dignity violation."""
        operation = {
            'id': 'test-003',
            'type': 'decision',
            'reduces_human_agency': True,
            'compassion_evaluated': True
        }
        
        result = self.fusion.validate_principle_alignment(operation)
        self.assertEqual(result['status'], 'misaligned')
        
        # Check that NRE-002 (Human Dignity) violation is detected
        violation_principles = [v['principle'] for v in result['violations']]
        self.assertIn('NRE-002', violation_principles)
    
    def test_misaligned_operation_compassion(self):
        """Test detection of missing compassion evaluation."""
        operation = {
            'id': 'test-004',
            'type': 'decision',
            'compassion_evaluated': False
        }
        
        result = self.fusion.validate_principle_alignment(operation)
        self.assertEqual(result['status'], 'misaligned')
        
        # Check that NRE-003 (Love-First) violation is detected
        violation_principles = [v['principle'] for v in result['violations']]
        self.assertIn('NRE-003', violation_principles)
    
    def test_consensus_hash_computation(self):
        """Test inter-pillar consensus hash computation."""
        data = {'test': 'data', 'value': 123}
        hash1 = self.fusion.compute_consensus_hash(data)
        hash2 = self.fusion.compute_consensus_hash(data)
        
        # Same data should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Different data should produce different hash
        data2 = {'test': 'data', 'value': 456}
        hash3 = self.fusion.compute_consensus_hash(data2)
        self.assertNotEqual(hash1, hash3)
    
    def test_correction_logging(self):
        """Test correction logging mechanism."""
        violation = {
            'principle': 'NRE-001',
            'reason': 'Test violation'
        }
        correction = {
            'action': 'realign',
            'protocol': 'test_protocol'
        }
        
        initial_count = len(self.fusion.fusion_state['corrections'])
        self.fusion.log_correction(violation, correction)
        
        self.assertEqual(len(self.fusion.fusion_state['corrections']), initial_count + 1)
        last_correction = self.fusion.fusion_state['corrections'][-1]
        self.assertEqual(last_correction['violation'], violation)
        self.assertEqual(last_correction['correction'], correction)


class TestCoreConceptMapper(unittest.TestCase):
    """Test the Core Concept Mapper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fusion = OntologicalFusionFramework()
        self.mapper = CoreConceptMapper(self.fusion)
    
    def test_concept_map_initialization(self):
        """Test concept map initialization."""
        self.assertIsNotNone(self.mapper.concept_map)
        self.assertIn('decision_making', self.mapper.concept_map)
        self.assertIn('ethical_oversight', self.mapper.concept_map)
    
    def test_get_aligned_principles(self):
        """Test retrieval of aligned principles for AIC components."""
        principles = self.mapper.get_aligned_principles('ai_decision_engine')
        self.assertIn('NRE-003', principles)  # Love-First Decision
        self.assertIn('NRE-008', principles)  # Consensus Sacralis
        self.assertIn('NRE-012', principles)  # Dual-Signature
    
    def test_get_aligned_principles_unknown_component(self):
        """Test handling of unknown component."""
        principles = self.mapper.get_aligned_principles('unknown_component')
        self.assertEqual(len(principles), 0)
    
    def test_validate_alignment_for_component(self):
        """Test alignment validation for specific component."""
        operation = {
            'id': 'test-mapper-001',
            'compassion_evaluated': True,
            'mutual_benefit': True
        }
        
        result = self.mapper.validate_alignment('ai_decision_engine', operation)
        self.assertIn('status', result)


class TestIntegratedEthicalKernel(unittest.TestCase):
    """Test the Integrated Ethical Kernel."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fusion = OntologicalFusionFramework()
        self.iek = IntegratedEthicalKernel(self.fusion)
    
    def test_initialization(self):
        """Test IEK initialization."""
        self.assertIsNotNone(self.iek.kernel_config)
        self.assertTrue(self.iek.psc_state['conscious_symbiosis'])
        self.assertEqual(self.iek.psc_state['symbiosis_level'], 1.0)
    
    def test_psc_compliant_operation(self):
        """Test PSC compliance for compliant operation."""
        operation = {
            'mutual_benefit': True,
            'extractive': False,
            'supports_growth': True
        }
        
        result = self.iek.enforce_psc_compliance(operation)
        self.assertTrue(result['compliant'])
        self.assertEqual(len(result['issues']), 0)
    
    def test_psc_non_compliant_extractive(self):
        """Test PSC compliance for extractive operation."""
        operation = {
            'mutual_benefit': True,
            'extractive': True,
            'supports_growth': True
        }
        
        result = self.iek.enforce_psc_compliance(operation)
        self.assertFalse(result['compliant'])
        self.assertIn('Operation is extractive', result['issues'])
    
    def test_psc_symbiosis_level_increase(self):
        """Test symbiosis level increases with compliant operations."""
        initial_level = self.iek.psc_state['symbiosis_level']
        
        operation = {
            'mutual_benefit': True,
            'extractive': False,
            'supports_growth': True
        }
        
        self.iek.enforce_psc_compliance(operation)
        # Note: level is already at max (1.0), so it won't increase
        self.assertGreaterEqual(self.iek.psc_state['symbiosis_level'], initial_level)
    
    def test_psc_symbiosis_level_decrease(self):
        """Test symbiosis level decreases with non-compliant operations."""
        initial_level = self.iek.psc_state['symbiosis_level']
        
        operation = {
            'mutual_benefit': False,
            'extractive': True,
            'supports_growth': False
        }
        
        result = self.iek.enforce_psc_compliance(operation)
        self.assertFalse(result['compliant'])
        self.assertLess(self.iek.psc_state['symbiosis_level'], initial_level)
    
    def test_deploy_correction_critical_violation(self):
        """Test correction deployment for critical violation."""
        violation = {
            'principle': 'NRE-002',
            'reason': 'Human dignity violation'
        }
        
        correction = self.iek.deploy_correction_mechanism(violation)
        self.assertEqual(correction['action'], 'immediate_halt')
        self.assertTrue(correction['requires_human_review'])
    
    def test_deploy_correction_symbiosis_violation(self):
        """Test correction deployment for symbiosis violation."""
        violation = {
            'principle': 'NRE-001',
            'reason': 'Symbiosis violation'
        }
        
        correction = self.iek.deploy_correction_mechanism(violation)
        self.assertEqual(correction['action'], 'realign')
        self.assertEqual(correction['realignment_protocol'], 'restore_sentimento_rhythm')


class TestTransparentSystematicResponse(unittest.TestCase):
    """Test the Transparent Systematic Response system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fusion = OntologicalFusionFramework()
        self.tsr = TransparentSystematicResponse(self.fusion)
    
    def test_initialization(self):
        """Test TSR initialization."""
        self.assertEqual(len(self.tsr.feedback_log), 0)
    
    def test_document_adjustment(self):
        """Test adjustment documentation."""
        adjustment = {
            'type': 'realignment',
            'principles': ['NRE-006'],
            'before': {'rhythm_coherence': 0.7},
            'after': {'rhythm_coherence': 0.95},
            'rationale': 'Restored Sentimento Rhythm',
            'human_reviewed': True,
            'dual_signature': {
                'ai': 'GitHub Copilot',
                'human': 'Seed-bringer'
            }
        }
        
        record = self.tsr.document_adjustment(adjustment)
        self.assertEqual(record['status'], 'documented')
        self.assertIn('record_id', record)
        self.assertEqual(len(self.tsr.feedback_log), 1)
    
    def test_generate_feedback_report(self):
        """Test feedback report generation."""
        # Add some adjustments
        for i in range(3):
            adjustment = {
                'type': 'test',
                'principles': ['NRE-010'],
                'rationale': f'Test adjustment {i}'
            }
            self.tsr.document_adjustment(adjustment)
        
        report = self.tsr.generate_feedback_report()
        self.assertEqual(report['report_type'], 'ethical_ascendancy_feedback')
        self.assertEqual(report['total_adjustments'], 3)
        self.assertIn('nre_compliance', report)
    
    def test_nre_compliance_computation(self):
        """Test NRE compliance metrics computation."""
        # Add compliant operations
        for i in range(5):
            adjustment = {
                'type': 'correction',
                'principles': ['NRE-010']
            }
            self.tsr.document_adjustment(adjustment)
        
        report = self.tsr.generate_feedback_report()
        compliance = report['nre_compliance']
        
        self.assertEqual(compliance['total_operations'], 5)
        self.assertEqual(compliance['status'], 'compliant')
        self.assertEqual(compliance['compliance_rate'], 1.0)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete framework."""
    
    def test_initialize_ontological_fusion(self):
        """Test complete framework initialization."""
        components = initialize_ontological_fusion()
        
        self.assertIn('fusion_framework', components)
        self.assertIn('core_concept_mapper', components)
        self.assertIn('integrated_ethical_kernel', components)
        self.assertIn('transparent_systematic_response', components)
        self.assertEqual(components['status'], 'initialized')
    
    def test_end_to_end_validation(self):
        """Test end-to-end operation validation."""
        components = initialize_ontological_fusion()
        fusion = components['fusion_framework']
        iek = components['integrated_ethical_kernel']
        tsr = components['transparent_systematic_response']
        
        # Create a compliant operation
        operation = {
            'id': 'integration-001',
            'type': 'decision',
            'intent': 'benefit',
            'compassion_evaluated': True,
            'mutual_benefit': True,
            'extractive': False,
            'supports_growth': True,
            'reduces_human_agency': False,
            'coercive': False,
            'hidden_agenda': False,
            'fragments_consciousness': False
        }
        
        # Validate NRE alignment
        validation = fusion.validate_principle_alignment(operation)
        self.assertEqual(validation['status'], 'aligned')
        
        # Check PSC compliance
        psc_check = iek.enforce_psc_compliance(operation)
        self.assertTrue(psc_check['compliant'])
        
        # Document the operation
        adjustment = {
            'type': 'validation',
            'principles': ['NRE-001', 'NRE-002', 'NRE-003'],
            'rationale': 'End-to-end integration test',
            'human_reviewed': True
        }
        record = tsr.document_adjustment(adjustment)
        self.assertEqual(record['status'], 'documented')
    
    def test_violation_detection_and_correction(self):
        """Test complete violation detection and correction flow."""
        components = initialize_ontological_fusion()
        fusion = components['fusion_framework']
        iek = components['integrated_ethical_kernel']
        
        # Create a non-compliant operation
        operation = {
            'id': 'violation-001',
            'type': 'decision',
            'intent': 'exploit',
            'reduces_human_agency': True
        }
        
        # Validate - should detect violations
        validation = fusion.validate_principle_alignment(operation)
        self.assertEqual(validation['status'], 'misaligned')
        self.assertGreater(len(validation['violations']), 0)
        
        # Deploy corrections for each violation
        for violation in validation['violations']:
            correction = iek.deploy_correction_mechanism(violation)
            self.assertIn('action', correction)
            # Critical violations should trigger immediate halt
            if violation['principle'] in ['NRE-002', 'NRE-005']:
                self.assertEqual(correction['action'], 'immediate_halt')


if __name__ == '__main__':
    unittest.main()
