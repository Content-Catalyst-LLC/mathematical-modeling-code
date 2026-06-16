# Advanced Population Dynamics Audit

## Scenarios
- **exponential_baseline** (exponential): final value 2453.25. unconstrained baseline.
- **logistic_capacity_limited** (logistic): final value 731.60. capacity-limited baseline.
- **allee_threshold** (allee_effect): final value 1000.00. low-population threshold.
- **harvesting_pressure** (harvesting): final value 0.00. external removal pressure.
- **stochastic_logistic_path** (stochastic): final value 656.25. one stochastic path.
- **two_patch_total** (metapopulation): final value 1768.31. two connected patches.
- **structured_total** (leslie_matrix): final value 3767.56. stage-structured projection.
- **spatial_grid_total** (diffusion_step): final value 419.88. one spatial diffusion update.

## Identifiability Warnings
- **short_series_r_k_tradeoff**: Do not infer carrying capacity from short early-growth data alone. Response: Use profile likelihood, grid search, or longer time series.
- **threshold_parameter_A**: Threshold claims need evidence near the threshold. Response: Run threshold scenarios and state uncertainty.
- **stochastic_sigma**: A single stochastic path is not a distribution. Response: Summarize ensembles, quantiles, and extinction probability.
