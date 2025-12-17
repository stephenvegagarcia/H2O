# H2O: Satellite Water Shield System

A comprehensive Python implementation of a satellite water shield system that leverages orbital hot/cold cycles for dual-purpose radiation protection and power generation.

## Overview

The H2O system uses water as a multi-functional resource in space:
- **Radiation Shielding**: Protects against cosmic rays and solar particle events
- **Thermal Energy Storage**: Exploits natural orbital temperature cycling
- **Power Generation**: Converts thermal cycles into electrical energy via thermoelectric generators
- **Life Support Reserve**: Water can serve as emergency life support resource

## Key Features

### 🛡️ Radiation Protection
- Exponential attenuation of harmful radiation
- Typical 75-80% dose reduction with 10 cm water shield
- Essential for long-duration missions and crew safety
- Configurable shield thickness for mission requirements

### 🌡️ Thermal Management
- Passive thermal regulation using orbital cycles
- Hot phase: ~50-150°C (sunlight exposure)
- Cold phase: ~-150°C to -20°C (Earth's shadow)
- Utilizes both sensible and latent heat capacity

### ⚡ Power Generation
- Continuous power from temperature gradients
- Thermoelectric conversion (10-20% efficiency)
- Scalable from CubeSats to space stations
- No moving parts - solid-state energy harvesting

### 🔄 Dual-Purpose Design
- Single system serves multiple critical functions
- Reduces overall satellite mass and complexity
- Cost-effective compared to separate systems
- Adaptable to various orbital parameters

## Installation

No external dependencies required! The system uses only Python standard library.

```bash
git clone https://github.com/stephenvegagarcia/H2O.git
cd H2O
```

## Quick Start

### Basic Usage

```python
from water_shield import SatelliteWaterShield

# Create a default system (ISS-like orbit)
system = SatelliteWaterShield()

# Print comprehensive status report
system.print_system_report(exposure_days=30)
```

### Custom Configuration

```python
from water_shield import SatelliteWaterShield, WaterShieldConfig, OrbitalParameters

# Configure water shield
config = WaterShieldConfig(
    water_mass_kg=2000.0,      # 2000 kg of water
    shield_thickness_cm=15.0,   # 15 cm thick shield
    surface_area_m2=30.0,       # 30 m² surface area
    hot_temp_celsius=60.0,      # Hot phase temperature
    cold_temp_celsius=-30.0     # Cold phase temperature
)

# Configure orbital parameters
orbit = OrbitalParameters(
    altitude_km=400.0,          # 400 km altitude
    orbital_period_min=92.0,    # 92 minute orbit
    eclipse_fraction=0.35       # 35% in shadow
)

# Create system with custom parameters
system = SatelliteWaterShield(
    water_config=config,
    orbital_params=orbit,
    power_efficiency=0.18       # 18% conversion efficiency
)

# Get detailed metrics
status = system.get_system_status(exposure_days=180)
print(f"Radiation reduction: {status['radiation_protection']['reduction_percent']:.1f}%")
print(f"Daily power: {status['power_generation']['daily_energy_kwh']:.2f} kWh")
```

## Examples

Run the comprehensive demonstration:

```bash
python example.py
```

This will show:
- Default configuration (ISS-like orbit)
- Enhanced system with increased water mass
- Higher orbit configuration (MEO)
- Compact CubeSat-scale system
- Comparative analysis of all configurations

## Testing

Run the test suite to validate the implementation:

```bash
python test_water_shield.py
```

Tests cover:
- Orbital parameter calculations
- Radiation shielding effectiveness
- Thermal energy storage
- Power generation metrics
- Physical constraints validation
- Integration testing

## System Components

### 1. OrbitalParameters
Defines satellite orbital characteristics:
- Altitude above Earth
- Orbital period
- Eclipse fraction (time in shadow)

### 2. WaterShieldConfig
Configuration for the water shield:
- Water mass and shield thickness
- Surface area and temperature ranges
- Thermal properties

### 3. RadiationShield
Calculates radiation protection:
- Shielding factor based on water thickness
- Dose reduction for cosmic rays
- Protection against solar particle events

### 4. ThermalCycleManager
Manages thermal cycling:
- Calculates energy storage capacity
- Heat absorption during sunlight
- Heat rejection during eclipse
- Phase change energy (ice ↔ water)

### 5. PowerGenerator
Power generation from thermal cycles:
- Energy per orbit calculation
- Average and peak power output
- Daily energy production
- Thermoelectric conversion efficiency

### 6. SatelliteWaterShield
Integrated system combining all components:
- Comprehensive status reporting
- Multi-metric analysis
- Easy configuration and customization

## Use Cases

### Space Stations (ISS, Gateway, etc.)
- 1000-5000 kg water shield
- 10-20 cm thickness
- ~80% radiation reduction
- 5-50 kW power generation

### Deep Space Missions
- Enhanced shielding for long durations
- Critical for Mars missions
- Sustained power in various orbits
- Emergency water reserve

### CubeSats and Small Satellites
- 50-200 kg water shield
- 3-7 cm thickness
- Compact power generation
- Cost-effective protection

### Lunar/Mars Surface Habitats
- Adaptable to surface environments
- Day/night thermal cycling
- Multi-year mission support
- Integrated life support

## Technical Specifications

### Radiation Protection
- **Shielding**: 15% attenuation per cm of water
- **Dose Reduction**: 75-85% with 10-15 cm shield
- **Protection**: GCR, SPE, trapped radiation

### Thermal Properties
- **Specific Heat**: 4186 J/(kg·K)
- **Latent Heat**: 334 kJ/kg (fusion)
- **Temperature Range**: -150°C to +150°C
- **Phase Change**: Ice ↔ Liquid Water

### Power Generation
- **Efficiency**: 10-20% (thermoelectric)
- **Output**: 10 W to 50 kW (scalable)
- **Technology**: Solid-state TEG
- **Reliability**: No moving parts

### Orbital Parameters
- **Altitude**: 200-36,000 km
- **Period**: 90 min to 24 hours
- **Eclipse**: 0-50% of orbit
- **Applications**: LEO, MEO, GEO

## Physics Background

### Radiation Shielding
Water is an excellent radiation shield due to:
- High hydrogen content (proton-rich)
- Effective neutron moderation
- Secondary radiation absorption
- Cost-effective compared to lead or polyethylene

### Thermal Cycling
Orbital environment provides natural cycling:
- **Sunlight**: ~1361 W/m² solar irradiance
- **Shadow**: ~3K space background temperature
- **Cycle Time**: Proportional to orbital period
- **Energy Storage**: Sensible + latent heat

### Thermoelectric Generation
Temperature gradients drive power generation:
- **Seebeck Effect**: Voltage from temperature difference
- **Hot Side**: Solar-heated water (60-150°C)
- **Cold Side**: Radiatively-cooled ice (-150 to -20°C)
- **Materials**: Bismuth telluride, skutterudites

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

Areas for enhancement:
- Additional orbital mechanics
- Advanced thermal modeling
- Real-world mission scenarios
- Visualization and plotting
- Integration with satellite simulators

## License

MIT License - see LICENSE file for details

## References

- NASA Space Radiation Element: Human Health and Performance
- International Space Station Environmental Control Systems
- Thermoelectric Generator Technology for Space Applications
- Water as a Radiation Shield in Space

## Author

Stephen Vega Garcia

## Acknowledgments

This project implements theoretical concepts from:
- Space radiation physics
- Orbital mechanics
- Thermodynamics and heat transfer
- Thermoelectric energy conversion
