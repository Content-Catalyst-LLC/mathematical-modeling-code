# Energy Balance Model Audit

## Scenario Records
- **baseline_one_layer** (one_layer): final temperature=3.083, equilibrium=3.083, adjustment time=8.333. one-layer model approaches equilibrium according to heat capacity and feedback.
- **stronger_feedback** (one_layer): final temperature=2.056, equilibrium=2.056, adjustment time=5.556. stronger feedback reduces equilibrium response and shortens adjustment time.
- **larger_heat_capacity** (one_layer): final temperature=3.049, equilibrium=3.083, adjustment time=33.333. larger heat capacity slows transient response.
- **two_layer_heat_uptake** (two_layer): final temperature=2.465, equilibrium=3.083, adjustment time=8.333. two-layer model stores heat in a slower reservoir; deep layer final temperature=1.443.

## Diagnostic Records
- **absorbed_solar_example**: value=238.175 W m^-2. Solar input requires albedo and geometry assumptions.
- **surface_storage_residual_example**: value=40.000 W m^-2. Omitted surface energy terms change storage interpretation.
- **building_temperature_step_example**: value=20.110 degrees. Building thermal balance requires occupancy, weather, controls, and material assumptions.
