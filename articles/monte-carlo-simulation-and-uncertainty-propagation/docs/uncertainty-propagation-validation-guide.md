# Uncertainty Propagation Validation Guide

## Verification

Verification checks whether the computational workflow is implemented correctly.

Examples:
- sampled values match intended ranges;
- random seeds reproduce outputs;
- threshold probability calculations are correct;
- quantile calculations are checked;
- output tables are reproducible.

## Validation

Validation checks whether the uncertainty model is credible.

Examples:
- input distributions are evidence-based;
- dependence assumptions are reviewed;
- thresholds match the decision context;
- output distributions are plausible;
- sensitivity analysis identifies major uncertainty drivers.

## Principle

Random sampling does not validate a model. Monte Carlo simulation propagates assumptions; it does not prove them.
