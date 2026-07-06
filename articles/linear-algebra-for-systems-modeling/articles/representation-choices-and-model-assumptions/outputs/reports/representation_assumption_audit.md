# Representation Assumption Audit

- Workflow: representation_assumption_audit
- Matrix shape: 3x2
- Row meaning: infrastructure_zones
- Column meaning: annual_demand_and_outage_exposure
- Value meaning: mixed_units_before_standardization
- Zero meaning: zero_would_mean_measured_absence_not_missingness
- Representation warning: Standardization improves comparability but changes interpretation from original units to relative position.

Representation choices define what the model can compare, reveal, and hide. Rows, columns, units, zeros, scaling, missingness, and boundaries should be documented before computation.
