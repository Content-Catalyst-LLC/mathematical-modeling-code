# Mathematical Deepening Notes

ODE solver workflows connect numerical integration, initial value problems, consistency, stability, convergence, local error estimation, adaptive step-size control, tolerances, stiffness detection, solver diagnostics, and reproducible computational governance.

## Required distinctions

- equation structure versus solver workflow
- fixed-step solver versus adaptive solver
- solver step size versus output sampling interval
- tolerance settings versus empirical uncertainty
- local numerical error versus model error
- stiffness versus ordinary instability
- solver completion versus validated result
- benchmark accuracy versus real-world validity

## Review checklist

- Document state variables, rate functions, parameters, units, and assumptions.
- Document initial conditions, time horizon, solver method, and software version.
- Record step sizes, tolerances, event logic, and output times.
- Preserve solver status, warnings, and diagnostic metadata.
- Compare step sizes, tolerances, or alternative solvers.
- Use analytic benchmarks or invariants when available.
- Review stiffness, positivity, conservation, and bounds.
