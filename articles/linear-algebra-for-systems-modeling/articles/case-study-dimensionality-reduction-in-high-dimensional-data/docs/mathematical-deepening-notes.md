# Mathematical Deepening Notes

## Required distinctions

- feature matrix versus reduced representation
- centering versus scaling
- covariance-based PCA versus correlation-based PCA
- projection score versus original feature value
- explained variance versus meaning
- component loading versus causal importance
- low-rank approximation versus complete data preservation
- reconstruction error versus decision loss
- visualization evidence versus validated cluster structure
- training-fold reduction versus leakage-prone global reduction

## Review checklist

- Document observation definitions, feature provenance, missingness, units, transformations, scaling, and centering.
- Preserve preprocessing parameters, component count, explained variance, loadings, reconstruction error, validation outputs, and leakage controls.
- Inspect reconstruction error overall, by feature, by observation, by subgroup, and by downstream task.
- Test stability across samples, perturbations, time windows, feature sets, and scaling choices.
- State interpretation boundaries for PCA/SVD components, visual clusters, reduced embeddings, and decision use.
