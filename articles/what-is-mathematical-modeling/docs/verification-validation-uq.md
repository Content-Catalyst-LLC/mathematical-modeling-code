# Verification, Validation, and Uncertainty Quantification

## Verification

Verification asks whether the model was implemented correctly.

Recommended checks:

- unit tests for invalid parameters;
- comparison of Euler and RK4 integration;
- nonnegative state enforcement;
- output schema checks;
- reproducibility under fixed seeds;
- smoke checks in every available language.

## Validation

Validation asks whether the model is adequate for a specific purpose.

The current scaffold uses synthetic observations only. Before empirical use, validation should include:

- independent observations;
- domain review;
- calibration/validation split;
- residual diagnostics;
- out-of-sample checks;
- model comparison;
- uncertainty intervals;
- adequacy statement.

## Uncertainty quantification

Current scaffold includes Monte Carlo parameter uncertainty. Professional extensions can add:

- Bayesian calibration;
- posterior predictive checks;
- global sensitivity analysis;
- Sobol indices;
- stochastic process noise;
- structural model ensembles;
- uncertainty-aware decision support.

## Adequacy statement

A model should be described as adequate only relative to:

- stated purpose;
- known assumptions;
- available evidence;
- domain of applicability;
- uncertainty and sensitivity results;
- consequences of error.
