"""
Unit tests for the Satellite Water Shield System
"""

import unittest
from water_shield import (
    SatelliteWaterShield,
    WaterShieldConfig,
    OrbitalParameters,
    RadiationShield,
    ThermalCycleManager,
    PowerGenerator
)


class TestOrbitalParameters(unittest.TestCase):
    """Test orbital parameter calculations."""
    
    def test_default_parameters(self):
        """Test default orbital parameters."""
        params = OrbitalParameters()
        self.assertEqual(params.altitude_km, 400.0)
        self.assertEqual(params.orbital_period_min, 92.0)
        self.assertEqual(params.eclipse_fraction, 0.35)
    
    def test_duration_calculations(self):
        """Test sunlight and eclipse duration calculations."""
        params = OrbitalParameters(orbital_period_min=90.0, eclipse_fraction=0.4)
        self.assertAlmostEqual(params.sunlight_duration_min, 54.0, places=1)
        self.assertAlmostEqual(params.eclipse_duration_min, 36.0, places=1)
    
    def test_total_orbit_time(self):
        """Test that sunlight + eclipse equals orbital period."""
        params = OrbitalParameters()
        total = params.sunlight_duration_min + params.eclipse_duration_min
        self.assertAlmostEqual(total, params.orbital_period_min, places=2)


class TestWaterShieldConfig(unittest.TestCase):
    """Test water shield configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = WaterShieldConfig()
        self.assertEqual(config.water_mass_kg, 1000.0)
        self.assertEqual(config.shield_thickness_cm, 10.0)
        self.assertEqual(config.surface_area_m2, 20.0)
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = WaterShieldConfig(
            water_mass_kg=500.0,
            shield_thickness_cm=5.0,
            surface_area_m2=10.0
        )
        self.assertEqual(config.water_mass_kg, 500.0)
        self.assertEqual(config.shield_thickness_cm, 5.0)


class TestRadiationShield(unittest.TestCase):
    """Test radiation shielding calculations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = WaterShieldConfig(shield_thickness_cm=10.0)
        self.shield = RadiationShield(self.config)
    
    def test_shielding_factor(self):
        """Test shielding factor calculation."""
        factor = self.shield.calculate_shielding_factor()
        self.assertGreater(factor, 0.0)
        self.assertLess(factor, 1.0)
        # 10 cm should provide significant shielding
        self.assertLess(factor, 0.3)
    
    def test_thicker_shield_better_protection(self):
        """Test that thicker shields provide better protection."""
        thin_config = WaterShieldConfig(shield_thickness_cm=5.0)
        thick_config = WaterShieldConfig(shield_thickness_cm=15.0)
        
        thin_shield = RadiationShield(thin_config)
        thick_shield = RadiationShield(thick_config)
        
        thin_factor = thin_shield.calculate_shielding_factor()
        thick_factor = thick_shield.calculate_shielding_factor()
        
        self.assertGreater(thin_factor, thick_factor)
    
    def test_dose_reduction(self):
        """Test radiation dose reduction calculations."""
        result = self.shield.calculate_effective_dose_reduction(exposure_days=30)
        
        self.assertIn('unshielded_dose_msv', result)
        self.assertIn('shielded_dose_msv', result)
        self.assertIn('reduction_percent', result)
        
        # Shielded dose should be less than unshielded
        self.assertLess(result['shielded_dose_msv'], result['unshielded_dose_msv'])
        
        # Reduction should be positive and less than 100%
        self.assertGreater(result['reduction_percent'], 0)
        self.assertLess(result['reduction_percent'], 100)


class TestThermalCycleManager(unittest.TestCase):
    """Test thermal cycle management."""
    
    # Test constants
    # Maximum heat rate based on solar constant (1361 W/m²) × max reasonable surface area (30 m²)
    # × max absorption coefficient (0.8) ≈ 32.7 kW, rounded up to 50 kW for safety margin
    MAX_REASONABLE_HEAT_RATE_W = 50000
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = WaterShieldConfig()
        self.orbital_params = OrbitalParameters()
        self.manager = ThermalCycleManager(self.config, self.orbital_params)
    
    def test_thermal_capacity(self):
        """Test thermal energy capacity calculations."""
        capacity = self.manager.calculate_thermal_energy_capacity()
        
        self.assertIn('sensible_heat_mj', capacity)
        self.assertIn('latent_heat_mj', capacity)
        self.assertIn('total_capacity_mj', capacity)
        
        # All values should be positive
        self.assertGreater(capacity['sensible_heat_mj'], 0)
        self.assertGreater(capacity['latent_heat_mj'], 0)
        self.assertGreater(capacity['total_capacity_mj'], 0)
        
        # Total should equal sum of components
        total = capacity['sensible_heat_mj'] + capacity['latent_heat_mj']
        self.assertAlmostEqual(total, capacity['total_capacity_mj'], places=1)
    
    def test_heat_absorption_rate(self):
        """Test heat absorption rate calculation."""
        rate = self.manager.calculate_heat_absorption_rate()
        self.assertGreater(rate, 0)
        # Should be reasonable for the given surface area
        self.assertLess(rate, self.MAX_REASONABLE_HEAT_RATE_W)
    
    def test_heat_rejection_rate(self):
        """Test heat rejection rate calculation."""
        rate = self.manager.calculate_heat_rejection_rate()
        self.assertGreater(rate, 0)


class TestPowerGenerator(unittest.TestCase):
    """Test power generation calculations."""
    
    def setUp(self):
        """Set up test fixtures."""
        config = WaterShieldConfig()
        orbital_params = OrbitalParameters()
        thermal_manager = ThermalCycleManager(config, orbital_params)
        self.generator = PowerGenerator(thermal_manager, efficiency=0.15)
    
    def test_power_output(self):
        """Test power output calculations."""
        output = self.generator.calculate_power_output_per_orbit()
        
        self.assertIn('energy_per_orbit_kwh', output)
        self.assertIn('avg_power_w', output)
        self.assertIn('daily_energy_kwh', output)
        
        # All values should be positive
        self.assertGreater(output['energy_per_orbit_kwh'], 0)
        self.assertGreater(output['avg_power_w'], 0)
        self.assertGreater(output['daily_energy_kwh'], 0)
    
    def test_higher_efficiency_more_power(self):
        """Test that higher efficiency produces more power."""
        config = WaterShieldConfig()
        orbital_params = OrbitalParameters()
        thermal_manager = ThermalCycleManager(config, orbital_params)
        
        low_eff = PowerGenerator(thermal_manager, efficiency=0.10)
        high_eff = PowerGenerator(thermal_manager, efficiency=0.20)
        
        low_power = low_eff.calculate_power_output_per_orbit()
        high_power = high_eff.calculate_power_output_per_orbit()
        
        self.assertGreater(high_power['avg_power_w'], low_power['avg_power_w'])


class TestSatelliteWaterShield(unittest.TestCase):
    """Test integrated satellite water shield system."""
    
    def test_default_initialization(self):
        """Test default system initialization."""
        system = SatelliteWaterShield()
        self.assertIsNotNone(system.radiation_shield)
        self.assertIsNotNone(system.thermal_manager)
        self.assertIsNotNone(system.power_generator)
    
    def test_custom_initialization(self):
        """Test system with custom parameters."""
        config = WaterShieldConfig(water_mass_kg=500.0)
        params = OrbitalParameters(altitude_km=500.0)
        system = SatelliteWaterShield(
            water_config=config,
            orbital_params=params,
            power_efficiency=0.20
        )
        self.assertEqual(system.water_config.water_mass_kg, 500.0)
        self.assertEqual(system.orbital_params.altitude_km, 500.0)
    
    def test_system_status(self):
        """Test comprehensive system status."""
        system = SatelliteWaterShield()
        status = system.get_system_status(exposure_days=30)
        
        # Check all major sections are present
        self.assertIn('orbital_parameters', status)
        self.assertIn('water_shield', status)
        self.assertIn('radiation_protection', status)
        self.assertIn('thermal_capacity', status)
        self.assertIn('thermal_rates', status)
        self.assertIn('power_generation', status)
        
        # Verify some key values
        self.assertEqual(status['orbital_parameters']['altitude_km'], 400.0)
        self.assertEqual(status['water_shield']['water_mass_kg'], 1000.0)
        self.assertGreater(status['radiation_protection']['reduction_percent'], 0)
        self.assertGreater(status['power_generation']['avg_power_w'], 0)
    
    def test_print_system_report(self):
        """Test that system report prints without errors."""
        system = SatelliteWaterShield()
        # This should not raise any exceptions
        try:
            system.print_system_report(exposure_days=7)
            success = True
        except Exception:
            success = False
        self.assertTrue(success)


class TestPhysicalConstraints(unittest.TestCase):
    """Test physical constraints and edge cases."""
    
    # Physical constraint constants
    MIN_THERMAL_CAPACITY_MJ = 300  # Minimum expected thermal capacity
    MAX_THERMAL_CAPACITY_MJ = 1000  # Maximum expected thermal capacity
    MIN_POWER_W = 1  # Minimum power output
    MAX_POWER_W = 100000  # Maximum power output (100 kW)
    
    def test_energy_conservation(self):
        """Test that energy values are physically reasonable."""
        config = WaterShieldConfig(water_mass_kg=1000.0)
        orbital_params = OrbitalParameters()
        thermal_manager = ThermalCycleManager(config, orbital_params)
        
        capacity = thermal_manager.calculate_thermal_energy_capacity()
        
        # Water's specific heat is 4.186 kJ/(kg·K)
        # Latent heat is 334 kJ/kg
        # Values should be in expected ranges
        self.assertGreater(capacity['total_capacity_mj'], self.MIN_THERMAL_CAPACITY_MJ)
        self.assertLess(capacity['total_capacity_mj'], self.MAX_THERMAL_CAPACITY_MJ)
    
    def test_power_limits(self):
        """Test that power generation is within physical limits."""
        system = SatelliteWaterShield()
        status = system.get_system_status()
        
        # Average power should be reasonable (not gigawatts!)
        avg_power = status['power_generation']['avg_power_w']
        self.assertGreater(avg_power, self.MIN_POWER_W)
        self.assertLess(avg_power, self.MAX_POWER_W)


def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestOrbitalParameters))
    suite.addTests(loader.loadTestsFromTestCase(TestWaterShieldConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestRadiationShield))
    suite.addTests(loader.loadTestsFromTestCase(TestThermalCycleManager))
    suite.addTests(loader.loadTestsFromTestCase(TestPowerGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestSatelliteWaterShield))
    suite.addTests(loader.loadTestsFromTestCase(TestPhysicalConstraints))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
