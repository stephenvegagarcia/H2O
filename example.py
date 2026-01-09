"""
Example usage of the Satellite Water Shield System

This script demonstrates the capabilities of the H2O satellite water shield
system, including radiation protection and power generation from orbital
thermal cycles.
"""

from water_shield import (
    SatelliteWaterShield,
    WaterShieldConfig,
    OrbitalParameters
)


def main():
    """Run examples demonstrating the water shield system."""
    
    print("\n" + "=" * 70)
    print("H2O: SATELLITE WATER SHIELD SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Example 1: Default configuration (ISS-like orbit)
    print("\n\n### EXAMPLE 1: Default Configuration (ISS-like orbit at 400 km) ###\n")
    default_system = SatelliteWaterShield()
    default_system.print_system_report(exposure_days=30)
    
    # Example 2: Enhanced system with more water mass
    print("\n\n### EXAMPLE 2: Enhanced System (2000 kg water, 15 cm shield) ###\n")
    enhanced_config = WaterShieldConfig(
        water_mass_kg=2000.0,
        shield_thickness_cm=15.0,
        surface_area_m2=30.0,
        hot_temp_celsius=60.0,
        cold_temp_celsius=-30.0
    )
    enhanced_system = SatelliteWaterShield(
        water_config=enhanced_config,
        power_efficiency=0.18
    )
    enhanced_system.print_system_report(exposure_days=180)
    
    # Example 3: Higher orbit (geostationary-like)
    print("\n\n### EXAMPLE 3: Higher Orbit Configuration (MEO - 20,000 km) ###\n")
    high_orbit_params = OrbitalParameters(
        altitude_km=20000.0,
        orbital_period_min=718.0,  # ~12 hour orbit
        eclipse_fraction=0.20
    )
    high_orbit_config = WaterShieldConfig(
        water_mass_kg=1500.0,
        shield_thickness_cm=12.0,
        surface_area_m2=25.0
    )
    high_orbit_system = SatelliteWaterShield(
        water_config=high_orbit_config,
        orbital_params=high_orbit_params,
        power_efficiency=0.20
    )
    high_orbit_system.print_system_report(exposure_days=365)
    
    # Example 4: Compact system for CubeSat-scale
    print("\n\n### EXAMPLE 4: Compact System (CubeSat-scale) ###\n")
    compact_config = WaterShieldConfig(
        water_mass_kg=100.0,
        shield_thickness_cm=5.0,
        surface_area_m2=2.0,
        hot_temp_celsius=40.0,
        cold_temp_celsius=-10.0
    )
    compact_system = SatelliteWaterShield(
        water_config=compact_config,
        power_efficiency=0.12
    )
    compact_system.print_system_report(exposure_days=7)
    
    # Comparative analysis
    print("\n\n### COMPARATIVE ANALYSIS ###\n")
    print("-" * 70)
    print(f"{'System':<20} {'Radiation Reduction':<25} {'Daily Power (kWh)':<20}")
    print("-" * 70)
    
    systems = [
        ("Default (ISS)", default_system),
        ("Enhanced", enhanced_system),
        ("High Orbit (MEO)", high_orbit_system),
        ("Compact (CubeSat)", compact_system)
    ]
    
    for name, system in systems:
        status = system.get_system_status(exposure_days=30)
        rad_reduction = status['radiation_protection']['reduction_percent']
        daily_power = status['power_generation']['daily_energy_kwh']
        print(f"{name:<20} {rad_reduction:>6.1f}%{'':<18} {daily_power:>8.2f}")
    
    print("-" * 70)
    
    print("\n\n### KEY BENEFITS OF THE H2O SYSTEM ###\n")
    print("1. RADIATION PROTECTION:")
    print("   - Water provides effective shielding against cosmic rays and solar particles")
    print("   - 10 cm of water reduces radiation dose by ~75-80%")
    print("   - Essential for long-duration space missions and crew safety")
    
    print("\n2. THERMAL ENERGY STORAGE:")
    print("   - Leverages natural orbital hot/cold cycles")
    print("   - Water's high specific heat and phase change energy")
    print("   - Passive thermal regulation without active cooling systems")
    
    print("\n3. POWER GENERATION:")
    print("   - Converts thermal cycles into electrical energy")
    print("   - Thermoelectric generators harvest temperature gradients")
    print("   - Continuous power production throughout orbit")
    
    print("\n4. DUAL-PURPOSE DESIGN:")
    print("   - Single system serves both protection and power needs")
    print("   - Reduces overall satellite mass and complexity")
    print("   - Water can be used for life support if needed")
    
    print("\n5. SCALABILITY:")
    print("   - Adaptable from CubeSats to large space stations")
    print("   - Configurable for different orbital parameters")
    print("   - Modular design allows incremental deployment")
    
    print("\n" + "=" * 70)
    print("END OF DEMONSTRATION")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
