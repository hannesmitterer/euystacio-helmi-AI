"""
Tests for Transmission Equation of Resonance Module
Lex Amoris Framework Testing
"""

import unittest
import numpy as np
from resonance_transmission import (
    lex_amoris_function,
    calculate_resonance
)


class TestLexAmorisFunction(unittest.TestCase):
    """Test cases for Lex Amoris function"""
    
    def test_single_time_value(self):
        """Test Lex Amoris function with single time value"""
        t = 0.0
        result = lex_amoris_function(t)
        self.assertIsInstance(result, (float, np.floating))
        self.assertEqual(result, 0.0)  # sin(0) = 0
    
    def test_array_input(self):
        """Test Lex Amoris function with array input"""
        t = np.array([0.0, np.pi/(2*0.432), np.pi/0.432])
        result = lex_amoris_function(t)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), 3)
    
    def test_periodicity(self):
        """Test that function exhibits periodic behavior"""
        period = 2 * np.pi / 0.432
        t1 = 5.0
        t2 = t1 + period
        
        val1 = lex_amoris_function(t1)
        val2 = lex_amoris_function(t2)
        
        # Should be approximately equal due to periodicity
        self.assertAlmostEqual(val1, val2, places=5)
    
    def test_bounded_output(self):
        """Test that output is bounded between -1 and 1"""
        t = np.linspace(0, 100, 1000)
        result = lex_amoris_function(t)
        
        self.assertTrue(np.all(result >= -1.0))
        self.assertTrue(np.all(result <= 1.0))


class TestCalculateResonance(unittest.TestCase):
    """Test cases for resonance calculation"""
    
    def test_basic_calculation(self):
        """Test basic resonance calculation"""
        phi_res = calculate_resonance(0, 100)
        
        self.assertIsInstance(phi_res, (float, np.floating))
        self.assertGreater(phi_res, 0)  # Magnitude should be positive
    
    def test_default_parameters(self):
        """Test resonance with default parameters"""
        phi_res = calculate_resonance(0, 100)
        
        # Should complete without error and return valid result
        self.assertIsNotNone(phi_res)
        self.assertFalse(np.isnan(phi_res))
        self.assertFalse(np.isinf(phi_res))
    
    def test_custom_s_roi(self):
        """Test resonance with custom S-ROI value"""
        phi_res_default = calculate_resonance(0, 100, s_roi=1.450)
        phi_res_custom = calculate_resonance(0, 100, s_roi=2.0)
        
        # Different S-ROI should yield different results
        self.assertNotEqual(phi_res_default, phi_res_custom)
        
        # Higher S-ROI should reduce resonance magnitude
        self.assertGreater(phi_res_default, phi_res_custom)
    
    def test_custom_omega(self):
        """Test resonance with custom omega value"""
        phi_res_default = calculate_resonance(0, 100, omega=0.432)
        phi_res_custom = calculate_resonance(0, 100, omega=0.5)
        
        # Different omega should yield different results
        self.assertNotEqual(phi_res_default, phi_res_custom)
    
    def test_time_range_effect(self):
        """Test effect of integration time range"""
        phi_res_short = calculate_resonance(0, 50)
        phi_res_long = calculate_resonance(0, 100)
        
        # Different time ranges should yield different results
        self.assertNotEqual(phi_res_short, phi_res_long)
    
    def test_zero_time_range(self):
        """Test resonance with zero time range"""
        phi_res = calculate_resonance(0, 0)
        
        # Should be zero or very small
        self.assertAlmostEqual(phi_res, 0.0, places=5)
    
    def test_numerical_stability(self):
        """Test numerical stability across different ranges"""
        # Should not produce NaN or Inf for reasonable inputs
        phi_res = calculate_resonance(0, 1000, s_roi=1.450, omega=0.432)
        
        self.assertFalse(np.isnan(phi_res))
        self.assertFalse(np.isinf(phi_res))
    
    def test_parameter_validation(self):
        """Test that function handles edge case parameters"""
        # Very small S-ROI
        phi_res_small = calculate_resonance(0, 100, s_roi=0.1)
        self.assertGreater(phi_res_small, 0)
        
        # Large S-ROI
        phi_res_large = calculate_resonance(0, 100, s_roi=10.0)
        self.assertGreater(phi_res_large, 0)
        
        # Small S-ROI should give larger resonance
        self.assertGreater(phi_res_small, phi_res_large)


class TestResonanceProperties(unittest.TestCase):
    """Test mathematical properties of resonance calculation"""
    
    def test_positive_magnitude(self):
        """Test that resonance magnitude is always non-negative"""
        for t_inf in [10, 50, 100, 200]:
            phi_res = calculate_resonance(0, t_inf)
            self.assertGreaterEqual(phi_res, 0)
    
    def test_s_roi_scaling(self):
        """Test that S-ROI scales resonance inversely"""
        s_roi_values = [0.5, 1.0, 1.450, 2.0, 5.0]
        results = [calculate_resonance(0, 100, s_roi=s) for s in s_roi_values]
        
        # Results should generally decrease with increasing S-ROI
        for i in range(len(results) - 1):
            self.assertGreater(results[i], results[i + 1])
    
    def test_frequency_alignment(self):
        """Test biological oscillator frequency alignment"""
        omega_bio = 0.432  # Hz
        phi_res = calculate_resonance(0, 100, omega=omega_bio)
        
        # Should produce valid resonance at biological frequency
        self.assertGreater(phi_res, 0)
        self.assertFalse(np.isnan(phi_res))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete resonance system"""
    
    def test_full_calculation_pipeline(self):
        """Test complete resonance calculation pipeline"""
        t0 = 0
        t_infinity = 100
        s_roi = 1.450
        omega = 0.432
        
        phi_res = calculate_resonance(t0, t_infinity, s_roi, omega)
        
        # Verify result is valid
        self.assertIsInstance(phi_res, (float, np.floating))
        self.assertGreater(phi_res, 0)
        self.assertFalse(np.isnan(phi_res))
        self.assertFalse(np.isinf(phi_res))
    
    def test_jitter_elimination_property(self):
        """Test that repeated calculations show jitter elimination"""
        # The j → 0 limit should give consistent results
        results = [calculate_resonance(0, 100) for _ in range(5)]
        
        # All results should be identical (no jitter)
        for result in results[1:]:
            self.assertEqual(results[0], result)
    
    def test_lex_amoris_integration(self):
        """Test integration of Lex Amoris function"""
        # Verify that Lex Amoris function integrates properly
        t = np.linspace(0, 100, 1000)
        lex_values = lex_amoris_function(t)
        
        # Should have both positive and negative values (oscillation)
        self.assertTrue(np.any(lex_values > 0))
        self.assertTrue(np.any(lex_values < 0))


if __name__ == '__main__':
    print("Running Transmission Equation of Resonance Tests")
    print("=" * 60)
    print("Lex Amoris Framework - Resonance Protocol")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)
