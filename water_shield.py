"""
Satellite Water Shield System

This module implements a satellite water shield system that uses orbital hot/cold 
cycles for radiation protection and power generation.

The system leverages the natural thermal cycling in orbit:
- Hot phase: Satellite faces the Sun (~120°C to 150°C)
- Cold phase: Satellite in Earth's shadow (~-150°C to -100°C)

Water acts as both radiation shielding and a thermal energy storage medium.
"""

import math
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class OrbitalParameters:
    """Parameters defining the satellite's orbital characteristics."""
    altitude_km: float = 400.0  # Altitude above Earth in km
    orbital_period_min: float = 92.0  # Orbital period in minutes
    eclipse_fraction: float = 0.35  # Fraction of orbit in Earth's shadow
    
    @property
    def sunlight_duration_min(self) -> float:
        """Duration of sunlight exposure per orbit (minutes)."""
        return self.orbital_period_min * (1 - self.eclipse_fraction)
    
    @property
    def eclipse_duration_min(self) -> float:
        """Duration of eclipse (shadow) per orbit (minutes)."""
        return self.orbital_period_min * self.eclipse_fraction


@dataclass
class WaterShieldConfig:
    """Configuration for the water shield system."""
    water_mass_kg: float = 1000.0  # Mass of water in kg
    shield_thickness_cm: float = 10.0  # Thickness of water shield in cm
    surface_area_m2: float = 20.0  # Surface area exposed to radiation
    
    # Thermal properties
    specific_heat_capacity: float = 4186.0  # J/(kg·K) for water
    latent_heat_fusion: float = 334000.0  # J/kg for water freezing/melting
    
    # Temperature ranges
    hot_temp_celsius: float = 50.0  # Target hot temperature (liquid water)
    cold_temp_celsius: float = -20.0  # Target cold temperature (ice)


class RadiationShield:
    """Handles radiation protection calculations."""
    
    # Radiation constants
    GCR_FLUX_MSV_DAY = 0.5  # Galactic Cosmic Rays flux (mSv/day)
    
    # Water shielding effectiveness (% reduction per cm)
    WATER_ATTENUATION_RATE = 0.15  # 15% reduction per cm
    
    def __init__(self, config: WaterShieldConfig):
        self.config = config
    
    def calculate_shielding_factor(self) -> float:
        """
        Calculate radiation shielding factor based on water thickness.
        
        Returns:
            Shielding factor (0-1, where 0 is complete shielding)
        """
        # Exponential attenuation: I = I0 * e^(-μx)
        attenuation = math.exp(-self.WATER_ATTENUATION_RATE * self.config.shield_thickness_cm)
        return attenuation
    
    def calculate_effective_dose_reduction(self, exposure_days: float = 1.0) -> Dict[str, float]:
        """
        Calculate radiation dose reduction.
        
        Args:
            exposure_days: Number of days of exposure
            
        Returns:
            Dictionary with unshielded dose, shielded dose, and reduction percentage
        """
        shielding_factor = self.calculate_shielding_factor()
        
        unshielded_dose_msv = self.GCR_FLUX_MSV_DAY * exposure_days
        shielded_dose_msv = unshielded_dose_msv * shielding_factor
        reduction_percent = (1 - shielding_factor) * 100
        
        return {
            'unshielded_dose_msv': unshielded_dose_msv,
            'shielded_dose_msv': shielded_dose_msv,
            'reduction_percent': reduction_percent,
            'shielding_factor': shielding_factor
        }


class ThermalCycleManager:
    """Manages thermal cycling and phase changes of water."""
    
    def __init__(self, config: WaterShieldConfig, orbital_params: OrbitalParameters):
        self.config = config
        self.orbital_params = orbital_params
    
    def calculate_thermal_energy_capacity(self) -> Dict[str, float]:
        """
        Calculate thermal energy storage capacity.
        
        Returns:
            Dictionary with sensible heat, latent heat, and total capacity
        """
        # Sensible heat (temperature change without phase change)
        temp_delta_k = abs(self.config.hot_temp_celsius - self.config.cold_temp_celsius)
        sensible_heat_j = (self.config.water_mass_kg * 
                          self.config.specific_heat_capacity * 
                          temp_delta_k)
        
        # Latent heat (phase change energy)
        latent_heat_j = self.config.water_mass_kg * self.config.latent_heat_fusion
        
        # Total thermal capacity
        total_capacity_j = sensible_heat_j + latent_heat_j
        
        return {
            'sensible_heat_mj': sensible_heat_j / 1e6,
            'latent_heat_mj': latent_heat_j / 1e6,
            'total_capacity_mj': total_capacity_j / 1e6,
            'total_capacity_kwh': total_capacity_j / 3.6e6
        }
    
    def calculate_heat_absorption_rate(self, solar_constant_w_m2: float = 1361.0,
                                        absorption_coefficient: float = 0.7) -> float:
        """
        Calculate heat absorption rate during sunlight phase.
        
        Args:
            solar_constant_w_m2: Solar irradiance (W/m²) - default is 1361 W/m² at Earth orbit
            absorption_coefficient: Solar absorptivity (0-1) - water surfaces typically 0.6-0.8
            
        Returns:
            Heat absorption rate in watts
            
        Note:
            Absorption coefficient varies with surface conditions:
            - Calm water: ~0.96
            - Ice/snow: ~0.1-0.5
            - Water droplets/ice mix: ~0.6-0.8 (used as conservative estimate)
        """
        heat_rate_w = solar_constant_w_m2 * self.config.surface_area_m2 * absorption_coefficient
        return heat_rate_w
    
    def calculate_heat_rejection_rate(self, space_temp_k: float = 3.0,
                                        emissivity: float = 0.95) -> float:
        """
        Calculate heat rejection rate during eclipse phase.
        
        Args:
            space_temp_k: Background temperature of space (Kelvin) - cosmic background is ~2.7K
            emissivity: Thermal emissivity (0-1) - ice/water surfaces typically 0.95-0.98
            
        Returns:
            Heat rejection rate in watts
            
        Note:
            Uses Stefan-Boltzmann law: P = ε·σ·A·(T⁴ - T_space⁴)
            Emissivity values from Incropera & DeWitt, "Fundamentals of Heat Transfer":
            - Water: 0.95-0.96
            - Ice: 0.96-0.98
        """
        stefan_boltzmann = 5.67e-8  # W/(m²·K⁴)
        avg_temp_k = (self.config.hot_temp_celsius + 273.15 + 
                      self.config.cold_temp_celsius + 273.15) / 2
        
        heat_rate_w = (emissivity * stefan_boltzmann * 
                      self.config.surface_area_m2 * 
                      (avg_temp_k**4 - space_temp_k**4))
        return heat_rate_w


class PowerGenerator:
    """Manages power generation from thermal cycles."""
    
    # Peak power factor for phase change periods
    # During phase transitions (ice melting/water freezing), energy release is concentrated
    # at the melting/freezing point, creating ~2x power peaks vs. average sensible heating
    # Based on latent heat release rates during phase change
    PEAK_POWER_MULTIPLIER = 2.0  # Empirical factor to capture peak power during phase transitions
    
    def __init__(self, thermal_manager: ThermalCycleManager, efficiency: float = 0.15):
        self.thermal_manager = thermal_manager
        self.efficiency = efficiency  # Carnot efficiency for thermoelectric conversion
    
    def calculate_power_output_per_orbit(self) -> Dict[str, float]:
        """
        Calculate electrical power generation per orbital cycle.
        
        Returns:
            Dictionary with power metrics
        """
        thermal_capacity = self.thermal_manager.calculate_thermal_energy_capacity()
        orbital_period_sec = self.thermal_manager.orbital_params.orbital_period_min * 60
        
        # Thermal energy cycled per orbit
        thermal_energy_j = thermal_capacity['total_capacity_mj'] * 1e6
        
        # Electrical energy generated (accounting for efficiency)
        electrical_energy_j = thermal_energy_j * self.efficiency
        electrical_energy_kwh = electrical_energy_j / 3.6e6
        
        # Average power output
        avg_power_w = electrical_energy_j / orbital_period_sec
        
        # Daily energy production
        orbits_per_day = 1440 / self.thermal_manager.orbital_params.orbital_period_min
        daily_energy_kwh = electrical_energy_kwh * orbits_per_day
        
        return {
            'energy_per_orbit_kwh': electrical_energy_kwh,
            'avg_power_w': avg_power_w,
            'peak_power_w': avg_power_w * self.PEAK_POWER_MULTIPLIER,
            'daily_energy_kwh': daily_energy_kwh,
            'conversion_efficiency': self.efficiency
        }


class SatelliteWaterShield:
    """Main class integrating all water shield system components."""
    
    def __init__(self, 
                 water_config: WaterShieldConfig = None,
                 orbital_params: OrbitalParameters = None,
                 power_efficiency: float = 0.15):
        """
        Initialize the satellite water shield system.
        
        Args:
            water_config: Configuration for water shield
            orbital_params: Orbital parameters
            power_efficiency: Thermoelectric conversion efficiency
        """
        self.water_config = water_config or WaterShieldConfig()
        self.orbital_params = orbital_params or OrbitalParameters()
        
        # Initialize subsystems
        self.radiation_shield = RadiationShield(self.water_config)
        self.thermal_manager = ThermalCycleManager(self.water_config, self.orbital_params)
        self.power_generator = PowerGenerator(self.thermal_manager, power_efficiency)
    
    def get_system_status(self, exposure_days: float = 30.0) -> Dict:
        """
        Get comprehensive system status.
        
        Args:
            exposure_days: Duration for radiation exposure calculation
            
        Returns:
            Dictionary with all system metrics
        """
        radiation_metrics = self.radiation_shield.calculate_effective_dose_reduction(exposure_days)
        thermal_metrics = self.thermal_manager.calculate_thermal_energy_capacity()
        power_metrics = self.power_generator.calculate_power_output_per_orbit()
        
        heat_absorption = self.thermal_manager.calculate_heat_absorption_rate()
        heat_rejection = self.thermal_manager.calculate_heat_rejection_rate()
        
        return {
            'orbital_parameters': {
                'altitude_km': self.orbital_params.altitude_km,
                'orbital_period_min': self.orbital_params.orbital_period_min,
                'sunlight_duration_min': self.orbital_params.sunlight_duration_min,
                'eclipse_duration_min': self.orbital_params.eclipse_duration_min
            },
            'water_shield': {
                'water_mass_kg': self.water_config.water_mass_kg,
                'shield_thickness_cm': self.water_config.shield_thickness_cm,
                'surface_area_m2': self.water_config.surface_area_m2
            },
            'radiation_protection': radiation_metrics,
            'thermal_capacity': thermal_metrics,
            'thermal_rates': {
                'heat_absorption_kw': heat_absorption / 1000,
                'heat_rejection_kw': heat_rejection / 1000
            },
            'power_generation': power_metrics
        }
    
    def print_system_report(self, exposure_days: float = 30.0):
        """
        Print a formatted system status report.
        
        Args:
            exposure_days: Duration for radiation exposure calculation
        """
        status = self.get_system_status(exposure_days)
        
        print("=" * 70)
        print("SATELLITE WATER SHIELD SYSTEM - STATUS REPORT")
        print("=" * 70)
        
        print("\n[ORBITAL PARAMETERS]")
        print(f"  Altitude: {status['orbital_parameters']['altitude_km']:.1f} km")
        print(f"  Orbital Period: {status['orbital_parameters']['orbital_period_min']:.1f} minutes")
        print(f"  Sunlight Phase: {status['orbital_parameters']['sunlight_duration_min']:.1f} min")
        print(f"  Eclipse Phase: {status['orbital_parameters']['eclipse_duration_min']:.1f} min")
        
        print("\n[WATER SHIELD CONFIGURATION]")
        print(f"  Water Mass: {status['water_shield']['water_mass_kg']:.0f} kg")
        print(f"  Shield Thickness: {status['water_shield']['shield_thickness_cm']:.1f} cm")
        print(f"  Surface Area: {status['water_shield']['surface_area_m2']:.1f} m²")
        
        print("\n[RADIATION PROTECTION]")
        rad = status['radiation_protection']
        print(f"  Exposure Duration: {exposure_days:.0f} days")
        print(f"  Unshielded Dose: {rad['unshielded_dose_msv']:.2f} mSv")
        print(f"  Shielded Dose: {rad['shielded_dose_msv']:.2f} mSv")
        print(f"  Dose Reduction: {rad['reduction_percent']:.1f}%")
        
        print("\n[THERMAL ENERGY STORAGE]")
        thermal = status['thermal_capacity']
        print(f"  Sensible Heat Capacity: {thermal['sensible_heat_mj']:.1f} MJ")
        print(f"  Latent Heat Capacity: {thermal['latent_heat_mj']:.1f} MJ")
        print(f"  Total Thermal Capacity: {thermal['total_capacity_mj']:.1f} MJ "
              f"({thermal['total_capacity_kwh']:.2f} kWh)")
        
        print("\n[THERMAL CYCLING RATES]")
        rates = status['thermal_rates']
        print(f"  Heat Absorption (Sunlight): {rates['heat_absorption_kw']:.2f} kW")
        print(f"  Heat Rejection (Eclipse): {rates['heat_rejection_kw']:.2f} kW")
        
        print("\n[POWER GENERATION]")
        power = status['power_generation']
        print(f"  Energy per Orbit: {power['energy_per_orbit_kwh']:.3f} kWh")
        print(f"  Average Power: {power['avg_power_w']:.1f} W")
        print(f"  Peak Power: {power['peak_power_w']:.1f} W")
        print(f"  Daily Energy Production: {power['daily_energy_kwh']:.2f} kWh")
        print(f"  Conversion Efficiency: {power['conversion_efficiency']*100:.1f}%")
        
        print("\n" + "=" * 70)
