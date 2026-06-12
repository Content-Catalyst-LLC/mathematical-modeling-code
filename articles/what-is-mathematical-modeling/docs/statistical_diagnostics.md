# Statistical Diagnostics Notes

## Calibration

The Python workflow includes grid-search calibration against synthetic observations. This is intentionally transparent and dependency-light.

Professional extensions may include:

- nonlinear least squares;
- maximum likelihood;
- Bayesian inference;
- MCMC;
- approximate Bayesian computation;
- hierarchical models;
- state-space models;
- measurement-error models.

## Diagnostics

Recommended diagnostics include:

- residual plots;
- residual summary statistics;
- RMSE and MAE;
- coverage of uncertainty intervals;
- out-of-sample checks;
- parameter identifiability review;
- posterior predictive checks when Bayesian methods are used.

## Warning

Good fit does not prove model adequacy. A model can fit data and still fail because of structural uncertainty, omitted mechanisms, extrapolation beyond data, poor boundary choice, or changing regimes.
