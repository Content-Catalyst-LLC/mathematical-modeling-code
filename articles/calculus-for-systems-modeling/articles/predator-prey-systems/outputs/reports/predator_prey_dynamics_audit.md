# Predator-Prey Dynamics Model Audit

## Scenario Records
- **classic_lotka_volterra** (lotka_volterra): prey=116.39, predator=10.26. baseline mass-action predator-prey interaction.
- **logistic_prey_limit** (logistic_prey): prey=50.20, predator=29.94. prey growth limited by carrying capacity.
- **type_ii_functional_response** (saturating_predation): prey=49.44, predator=4.93. predation saturates due to handling time.
- **harvesting_pressure** (harvesting): prey=0.00, predator=0.00. external removal shifts dynamics and risk.
- **stochastic_lotka_volterra_path** (stochastic): prey=28.63, predator=10.19. one stochastic path under environmental variability.

## Stability Records
- **lotka_volterra_coexistence**: trace=0.0000, determinant=0.3000, status=center_or_neutral_linearization. Classic Lotka-Volterra neutral-cycle behavior depends on ideal assumptions.

Predator-prey model outputs depend on interaction assumptions, functional response, parameter evidence, stochasticity, spatial structure, and claim boundaries.
