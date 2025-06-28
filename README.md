# energy_models
Energy Modelling Tool Kit

A comprehensive Python package for energy modeling, featuring performance curves, schedulers, and various fan models based on EnergyPlus components.

## 📦 Modules Overview

### 🕒 Scheduler
Python-based schedule system that mimics EnergyPlus's schedule behavior for controlling system operations over time.
- **Features**: Weekday/weekend/holiday schedules, hourly/sub-hourly resolution, linear interpolation
- **Documentation**: [Scheduler README](energy_models/scheduler/README.md)

### 📈 Curves
EnergyPlus performance curves implementation for modeling HVAC and plant component performance.
- **Features**: Linear, quadratic, cubic, biquadratic, and other curve types with mathematical formulas
- **Documentation**: [Curves README](energy_models/curves/README.md)

### 🌪️ Fans
Collection of fan models based on EnergyPlus fan objects with different control strategies and power models.

#### Fan Models Available:

- **Component Model Fan** - Physics-based detailed fan modeling
  - **Type**: Fully flexible (modulating + cycling)
  - **Features**: Variable flow based on pressure, curve-based pressure rise, physics-based power model
  - **Documentation**: [ComponentModel README](energy_models/fans/component_model/README.md)

- **Constant Volume Fan** - Simple constant flow fan
  - **Type**: Constant flow operation
  - **Features**: Fixed design flow, user-specified pressure rise, simple power model
  - **Documentation**: [ConstantVolume README](energy_models/fans/constant_volume/README.md)

- **Variable Volume Fan** - Modulating fan with curve-based power
  - **Type**: Modulating (0-1) control
  - **Features**: Variable flow with load, curve-based power model, availability + flow fraction scheduling
  - **Documentation**: [VariableVolume README](energy_models/fans/variable_volume/README.md)

- **On/Off Fan** - Binary operation fan
  - **Type**: Binary (On/Off) control
  - **Features**: 0 or design flow operation, simple power model, thermostat/logic control
  - **Documentation**: [OnOff README](energy_models/fans/on_off/README.md)

- **Night Ventilation Fan** - Night cooling exhaust fan
  - **Type**: Performance modifier for night operation
  - **Features**: Alternate flow fraction at night, availability manager control, alternate pressure rise
  - **Documentation**: [NightVentilation README](energy_models/fans/night_ventilation/README.md)

- **Zone Exhaust Fan** - Zone-level exhaust fan
  - **Type**: Zone exhaust with schedule control
  - **Features**: Flow fraction scheduling, modulating control, zone-specific exhaust
  - **Documentation**: [ZoneExhaust README](energy_models/fans/zone_exhaust/README.md)

## 🚀 Getting Started

This package provides Python implementations of EnergyPlus components for energy modeling applications. Each module includes detailed documentation and examples for integration into larger simulation workflows.

## 📚 References

All implementations are based on EnergyPlus documentation and formulas. Specific references are provided in each module's README file.
