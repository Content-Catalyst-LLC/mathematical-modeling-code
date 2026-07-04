# Advanced Decomposition Workflow Review

- **matrix_structure** (required): Review shape, symmetry, sparsity, rank, scaling, definiteness, conditioning, and data source before factorization.
- **decomposition_choice** (required): Match LU, QR, Cholesky, eigen, Schur, SVD, sparse, or low-rank workflow to task and matrix structure.
- **pivoting_and_ordering** (required): Document row and column permutations used for stability, sparsity preservation, or fill-in reduction.
- **rank_tolerance** (required): State tolerance used for rank estimates, pseudoinverses, and low-rank approximation.
- **reconstruction_error** (required): Report factorization reconstruction error, approximation error, and solve residuals where relevant.
- **conditioning** (required): Report condition estimates or singular spectra for sensitive computations.
- **component_interpretation** (required): Interpret factors, modes, and components through domain review rather than treating them as automatic causes.
- **responsible_use** (required): Communicate factorization limits, approximation loss, diagnostics, and assumption boundaries.
