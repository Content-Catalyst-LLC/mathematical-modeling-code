# Advanced Projection and Reflection Review

- **target_subspace** (required): Document what the projection subspace means.
- **residual_interpretation** (required): Explain whether residuals are noise, excluded structure, bias, or model limitation.
- **inner_product_choice** (required): State which geometry defines distance and orthogonality.
- **projection_diagnostics** (required): Check idempotence, symmetry, rank, and residual norm.
- **reflection_diagnostics** (required): Check involution, length preservation, and orientation meaning.
- **numerical_stability** (recommended): Avoid unstable normal-equation projection formulas when QR or SVD is better.
