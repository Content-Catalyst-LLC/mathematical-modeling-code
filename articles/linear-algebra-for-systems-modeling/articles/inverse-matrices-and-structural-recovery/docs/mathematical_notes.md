# Mathematical Notes: Inverse Matrices and Structural Recovery

## Invertibility

A square matrix `A ∈ R^{n×n}` is invertible if there exists a matrix `A^{-1}` such that:

```text
A^{-1}A = I
AA^{-1} = I
```

Equivalent conditions include:

- `det(A) ≠ 0`
- `rank(A) = n`
- the columns of `A` are linearly independent
- the null space of `A` contains only the zero vector
- every `b ∈ R^n` has a unique solution to `Ax = b`

## Recovery interpretation

If `A` maps a state `x` to an observation `b`, then recovery asks whether `x` can be reconstructed from `b`.

A nonsingular matrix preserves enough dimensional structure for unique recovery. A singular matrix collapses at least one nonzero direction into zero or into a dependent direction, so different inputs can become observationally indistinguishable.

## Conditioning

Invertibility alone is not enough. A matrix can be invertible but poorly conditioned.

The condition number is:

```text
κ(A) = ||A|| ||A^{-1}||
```

For perturbations in `b`, a standard sensitivity relationship is:

```text
relative error in x ≲ κ(A) × relative error in b
```

This means near-singular matrices may produce recovered states that are mathematically exact in ideal arithmetic but unusable with noisy data.

## Direct inverse versus solve

In numerical computing, prefer solving the system directly:

```text
solve(A, b)
```

instead of explicitly computing:

```text
inv(A) @ b
```

Direct solvers are usually more stable and efficient than forming an explicit inverse.
