# Mathematical Deepening Notes

Stability, error, and convergence in numerical modeling connect discretization, truncation error, local and global error, consistency, stability regions, eigenvalues, stiffness, conditioning, residuals, refinement studies, manufactured solutions, and reproducible solver governance.

## Required distinctions

- numerical accuracy versus empirical validity
- local error versus global error
- truncation error versus round-off error
- stability of the method versus stability of the model
- convergence under refinement versus truth of assumptions
- solver completion versus validated result
- visual smoothness versus numerical reliability

## Review checklist

- Preserve solver method, order, step size, and tolerances.
- Compare results across step sizes or solver tolerances.
- Benchmark against analytic, manufactured, or highly refined reference cases.
- Inspect stability warnings, stiffness indicators, and constraint violations.
- Preserve residuals, solver status, and diagnostic metadata.
- Separate numerical confidence from real-world claims.
