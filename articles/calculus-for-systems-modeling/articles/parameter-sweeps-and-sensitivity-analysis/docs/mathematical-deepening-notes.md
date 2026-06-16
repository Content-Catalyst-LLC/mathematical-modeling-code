# Mathematical Deepening Notes

Parameter sweeps and sensitivity analysis connect derivatives, finite differences, response surfaces, elasticity, local and global sensitivity, variance decomposition, uncertainty propagation, Monte Carlo sampling, Sobol-style indices, Morris screening, identifiability, calibration, robustness analysis, and model governance.

## Required distinctions

- sensitivity analysis versus uncertainty analysis
- local sensitivity versus global sensitivity
- one-at-a-time sweeps versus interaction-aware sweeps
- range selection versus probability distribution
- robustness within tested ranges versus general truth
- parameter uncertainty versus model structural uncertainty
- numerical sensitivity versus substantive model sensitivity

## Review checklist

- Preserve parameter names, units, baselines, ranges, and sources.
- Document sweep design, sampling method, solver settings, and output metric.
- Record local sensitivities, elasticity estimates, and response-surface summaries.
- Identify thresholds, fragile regions, dominant parameters, and interactions.
- Keep generated tables behind figures.
- Separate robust conclusions from conditional or fragile claims.
