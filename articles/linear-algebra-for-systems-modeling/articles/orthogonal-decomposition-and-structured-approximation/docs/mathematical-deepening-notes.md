# Mathematical Deepening Notes

## Required distinctions

- exact representation versus approximation
- modeled component versus residual component
- subspace choice versus data truth
- projection method versus interpretation
- arbitrary basis versus orthonormal basis
- normal equations versus QR and SVD workflows
- residual as noise versus residual as unmodeled structure
- algebraic rank versus numerical rank
- low-rank simplification versus loss of rare or local patterns
- numerical stability versus model validity

## Review checklist

- Define the target vector, model matrix, and modeled subspace.
- Document scaling, centering, and feature construction.
- Use QR or SVD when stability matters.
- Report residual norm, relative residual, orthogonality error, rank, and condition number.
- Avoid forming normal equations for ill-conditioned systems.
- Review residuals before treating them as noise.
- Validate approximation quality against the systems question.
