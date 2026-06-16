# Condition and Scope Audit

## Initial Conditions
- **population_stock** = 10.0 state units; source: synthetic teaching baseline; uncertainty: baseline chosen for demonstration
- **time_start** = 0.0 time units; source: model convention; uncertainty: no empirical timestamp attached

## Boundary Conditions
- **left_edge** (no_flux): material does not leave through the left boundary. No-flux boundaries may overstate retention if the real system is open.
- **right_edge** (absorbing): material can leave the modeled domain. Absorbing boundaries may understate feedback from surroundings.

## Scope Records
- **temporal_scope**: 0 to 20 time units. Do not interpret as long-term forecast.
- **parameter_scope**: growth_rate between 0.1 and 0.6. Do not use outside tested parameter range without review.
- **decision_scope**: exploratory and educational use. Do not treat as direct decision prescription.
