# Calibration Design Guide

## Article

**Calibration, Estimation, and Parameter Fitting**

## Central claim

Calibration connects model structure to evidence by estimating parameter values, but fitted values remain conditional on data quality, objective functions, model form, parameter bounds, numerical method, and validation review.

## Required records

| Record | Purpose |
|---|---|
| calibration_data | Documents evidence used for fitting |
| objective_function | Defines model-data mismatch |
| parameter_bounds | Specifies allowed parameter values |
| candidate_scores | Preserves fitted alternatives |
| residual_diagnostics | Reviews post-fit error patterns |
| parameter_uncertainty | Reports confidence, sensitivity, or plausible ranges |
| validation_plan | Checks credibility beyond calibration data |
| use_limits | Prevents decision overreach |
