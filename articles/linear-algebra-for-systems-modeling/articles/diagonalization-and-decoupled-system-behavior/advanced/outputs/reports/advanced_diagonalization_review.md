# Advanced Diagonalization and Decoupled Behavior Review

- **matrix_definition** (required): Document what the matrix represents, including units, weights, and time step.
- **eigenvector_basis** (required): Confirm enough independent eigenvectors exist for full diagonalization.
- **reconstruction_error** (required): Report ||A - P D P^{-1}|| for computed diagonalization.
- **condition_number_P** (required): Estimate cond(P) before interpreting modal coordinates.
- **modal_translation** (required): Translate modal coordinates back into system-specific meaning.
- **fallback_decomposition** (recommended): Use Schur, SVD, or Jordan analysis when diagonalization is fragile or invalid.
