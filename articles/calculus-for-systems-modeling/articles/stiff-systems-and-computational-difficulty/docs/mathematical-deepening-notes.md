# Mathematical Deepening Notes

Stiff systems and computational difficulty connect eigenvalue separation, stability regions, implicit integration, Jacobians, Newton iteration, adaptive step-size control, local truncation error, stiffness ratios, singular perturbation, quasi-steady approximations, conditioning, scaling, and solver governance.

## Required distinctions

- real system stiffness versus solver artifact
- model stability versus numerical stability
- explicit step-size restriction versus accuracy requirement
- implicit stability versus final accuracy
- time-scale separation versus poor scaling
- solver warning versus model failure
- computational difficulty versus empirical validity

## Review checklist

- Preserve method, tolerances, step-size histories, and warnings.
- Compare explicit and implicit methods on benchmark problems.
- Inspect local rates, Jacobian eigenvalues, or stiffness ratios when available.
- Document variable scaling, units, and nondimensionalization choices.
- Record solver failures, step rejections, and nonlinear iteration status.
- Separate computational difficulty from substantive model claims.
