# Mathematical Deepening Notes

Runge–Kutta methods connect Taylor expansion, slope-stage averaging, quadrature-like weighting, method order, local truncation error, global error, stability regions, adaptive error control, and solver design.

## Required distinctions

- Euler slope versus Runge–Kutta stage slopes
- midpoint method versus classical RK4
- stage formula versus slope weight
- method order versus empirical validity
- local error versus global error
- stability versus stiffness
- fixed-step RK versus adaptive solver
- benchmark accuracy versus model adequacy

## Review checklist

- Document the rate function and parameters.
- Document initial conditions and simulation horizon.
- Record step size and solver order.
- Record stage formulas and slope weights.
- Compare with Euler or a refined solution.
- Compare multiple step sizes.
- Review stiffness and stability risks.
- Preserve trajectory, error, stage, and governance metadata.
