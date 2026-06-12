# Verification, Validation, and Uncertainty Quantification Notes

## Verification

Verification asks whether the model was implemented correctly.

Recommended checks:

- unit tests for model equations;
- checks for invalid parameter values;
- comparison of Euler and RK4 integration;
- convergence testing as the time step decreases;
- output schema validation;
- reproducibility checks for deterministic seeds.

## Validation

Validation asks whether the model is adequate for a specific purpose.

For this demonstration, validation is limited to synthetic observations. In a real project, validation may include:

- comparison with experimental data;
- comparison with independent field observations;
- benchmark tests;
- expert elicitation;
- residual analysis;
- out-of-sample predictive checks;
- stress tests under extreme but plausible conditions.

## Uncertainty quantification

The scaffold includes a simple Monte Carlo routine for uncertainty propagation. Professional extensions can add:

- probabilistic parameter priors;
- Bayesian updating;
- bootstrap intervals;
- global sensitivity analysis;
- Sobol indices;
- polynomial chaos;
- emulator/surrogate modeling;
- ensemble diagnostics.

## Adequacy statement

A model should be declared adequate only relative to:

- a stated purpose;
- specified assumptions;
- stated data conditions;
- a defined domain of applicability;
- uncertainty and sensitivity results;
- known limitations.
