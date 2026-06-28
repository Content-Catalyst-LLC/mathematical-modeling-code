# Inverse Matrices and Structural Recovery

This folder supports the article **“Inverse Matrices and Structural Recovery”** in the *Linear Algebra for Systems Modeling* series.

The examples show how an invertible matrix can recover an original system state from transformed observations, and why singular or nearly singular matrices create structural recovery problems.

## Core idea

If a system transformation is written as:

```text
Ax = b
```

and the matrix `A` is invertible, then the original state can be recovered as:

```text
x = A^-1 b
```

In systems modeling, this is not just an algebraic operation. It represents recovery of inputs, hidden states, signals, or structural causes from observed outputs.

## Folder contents

- `python/` — inverse matrix and recovery demonstration
- `r/` — base R recovery example
- `julia/` — Julia recovery example
- `sql/` — matrix-style recovery tables
- `c/`, `cpp/`, `fortran/`, `go/`, `rust/`, `java/`, `typescript/` — small 2x2 inverse demonstrations
- `prolog/` — logical facts for invertibility and recovery
- `docs/` — conceptual explanation
- `data/` — simple matrix and vector data
- `outputs/` — placeholder for generated outputs

## Modeling warning

An inverse matrix exists only when the transformation preserves enough independent information. If the matrix collapses dimensions or contains dependent columns, structural recovery becomes ambiguous or impossible.
