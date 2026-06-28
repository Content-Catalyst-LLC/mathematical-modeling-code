# Inverse Matrices and Structural Recovery

This folder supports the article **“Inverse Matrices and Structural Recovery”** in the *Linear Algebra for Systems Modeling* series.

The examples are designed to be useful to mathematically literate engineers, applied mathematicians, systems modelers, and scientific programmers. The goal is not only to show that an inverse matrix can solve `Ax = b`, but to demonstrate when recovery is meaningful, stable, ill-conditioned, ambiguous, or better handled by least squares or pseudoinverse methods.

## Core idea

A linear system transformation is often written as:

```text
Ax = b
```

where:

- `A` is the system, measurement, mixing, or transformation matrix,
- `x` is the hidden state, input, or source vector,
- `b` is the observed output.

If `A` is square, full-rank, and well-conditioned, recovery may be written as:

```text
x = A^-1 b
```

But in engineering and applied mathematics, direct inversion is only part of the story. The serious questions are:

1. Is the transformation structurally recoverable?
2. Is the matrix full rank?
3. Is the recovery numerically stable?
4. How sensitive is the recovered state to measurement noise?
5. What happens if the system is singular, nearly singular, underdetermined, or overdetermined?
6. Should the model use solve, least squares, pseudoinverse, regularization, or a redesigned measurement system?

## Folder contents

- `python/`
  - `engineering_grade_recovery.py` — main technical demonstration with diagnostics
  - `near_singular_instability.py` — perturbation sensitivity and condition number example
  - `pseudoinverse_and_least_squares.py` — exact inverse failure and fallback recovery
  - `sensor_state_recovery.py` — applied sensor/state reconstruction example
  - `residual_error_checks.py` — residuals, relative error, and validation checks
  - `generate_outputs.py` — produces CSV summaries in `outputs/`
- `r/`
  - base R inverse and condition-number demonstration
- `julia/`
  - Julia recovery, rank, condition, and least-squares example
- `sql/`
  - matrix-style data representation and residual checks
- `c/`, `cpp/`, `fortran/`, `go/`, `rust/`, `java/`, `typescript/`
  - compact numerical recovery examples with determinant, residual, and singularity guards
- `prolog/`
  - logical conditions for invertibility, singularity, and recovery eligibility
- `docs/`
  - mathematical notes, engineering notes, validation workflow, and modeling interpretation
- `data/`
  - small system matrices, near-singular matrices, sensor matrices, and observation vectors
- `tests/`
  - lightweight Python validation tests
- `outputs/`
  - generated CSV summaries after running the Python output script

## Recommended run sequence

From this article directory:

```bash
python3 python/engineering_grade_recovery.py
python3 python/near_singular_instability.py
python3 python/pseudoinverse_and_least_squares.py
python3 python/sensor_state_recovery.py
python3 python/residual_error_checks.py
python3 python/generate_outputs.py
python3 tests/test_recovery_diagnostics.py
```

These Python scripts require NumPy. If needed:

```bash
python3 -m pip install numpy
```

## Modeling rule

An inverse matrix is not merely an algebraic object. In systems modeling, it is a claim about recoverability. If the matrix is singular, rank deficient, nearly singular, noisy, or poorly conditioned, exact recovery may be impossible or misleading.
