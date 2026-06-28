# Conceptual Notes: Inverse Matrices and Structural Recovery

An inverse matrix represents reversibility. If a matrix transforms an original state into an observed output, the inverse asks whether that original state can be reconstructed.

In modeling terms:

- `A` represents the system transformation.
- `x` represents the original state or input.
- `b` represents the observed output.
- `A^-1` represents structural recovery.

A matrix is invertible when:

- its determinant is nonzero,
- its columns are linearly independent,
- it has full rank,
- its null space contains only the zero vector,
- every output corresponds to exactly one input.

A non-invertible matrix means information has been lost. Different inputs may produce the same output, so exact recovery is not possible without extra assumptions.
