# Advanced Machine Learning Pipeline Review

- **observation_definition** (required): Document sampling process, inclusion rules, time period, unit of analysis, missing records, and measurement context.
- **feature_definition** (required): Record units, provenance, transformations, proxies, missingness, and known limitations.
- **target_definition** (required): Document label source, timing, measurement process, subjectivity, delay, and relationship to the decision.
- **preprocessing** (required): Document scaling, centering, imputation, encoding, normalization, projection, feature selection, and fitted parameters.
- **leakage_control** (required): Fit preprocessing, feature selection, dimensionality reduction, model parameters, and thresholds inside training or validation workflows only.
- **baseline_model** (required): Train transparent baselines and compare complex models against them using the same evaluation protocol.
- **evaluation** (required): Report overall metrics, residuals, calibration, threshold sensitivity, subgroup error, rare-event performance, and temporal validation.
- **monitoring** (required): Monitor feature drift, label shift, concept drift, embedding drift, residual drift, data pipeline changes, and retraining triggers.
- **interpretability_and_bias** (required): Review coefficients, importances, embeddings, proxies, subgroup errors, and institutional context before making claims.
- **decision_boundary** (required): Attach documentation, uncertainty, validation status, threshold rationale, oversight, appeals, and stop-use conditions to outputs.
