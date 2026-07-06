# Advanced Dimensionality Reduction Review

- **observation_definition** (required): Define what rows represent and what ethical or domain-specific stakes they carry.
- **feature_definition** (required): Record units, measurement sources, proxies, missingness, transformations, and feature provenance.
- **preprocessing** (required): Document centering, scaling, imputation, transformation, filtering, and outlier handling.
- **leakage_control** (required): Fit scaling and dimensionality reduction only on training folds or training data in predictive workflows.
- **component_selection** (required): Record explained variance, reconstruction error, stability evidence, downstream validation, and domain justification.
- **reconstruction_review** (required): Inspect total, per-feature, per-observation, subgroup, and task-specific reconstruction error.
- **rare_pattern_preservation** (required): Check whether rare, minority, local, or high-stakes structure is lost in reduction.
- **stability_review** (required): Test component and downstream stability across samples, perturbations, time windows, and feature sets.
- **interpretability_review** (required): Review loadings, component labels, visual clusters, and domain evidence before naming dimensions.
- **decision_boundary** (required): Attach preprocessing choices, component count, uncertainty notes, validation status, and stop-use conditions to outputs.
