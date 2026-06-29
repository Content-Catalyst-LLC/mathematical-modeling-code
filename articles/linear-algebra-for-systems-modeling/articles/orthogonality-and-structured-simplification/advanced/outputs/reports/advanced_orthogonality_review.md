# Advanced Orthogonality Review

- **inner_product_definition** (required): State the geometry defining orthogonality.
- **scaling_units_review** (required): Check whether units or normalization choices change dot-product meaning.
- **tolerance_policy** (required): Document numerical tolerance for near-zero dot products.
- **residual_interpretation** (required): Treat orthogonal residuals as substantive evidence, not automatic noise.
- **orthogonality_error** (required): Report ||Q^TQ-I|| or equivalent orthonormality diagnostic.
- **solver_choice** (recommended): Prefer QR or SVD over unstable normal-equation workflows when needed.
