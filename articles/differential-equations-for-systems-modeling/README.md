# Differential Equations for Systems Modeling

This article folder supports reproducible examples for differential-equation-based systems modeling.

## Topics

- ordinary differential equations
- initial value problems
- rates of change
- logistic growth
- coupled systems
- predator-prey dynamics
- SIR epidemiological modeling
- phase behavior
- equilibrium and stability
- numerical approximation
- Euler simulation
- Runge-Kutta-style solver concepts
- sensitivity analysis
- parameter sweeps
- responsible model interpretation

## Folder Structure

- `python/` — ODE simulation, phase behavior, sensitivity sweeps, predator-prey, and SIR examples
- `r/` — dynamic simulation, visualization-ready outputs, sensitivity analysis
- `julia/` — compact scientific-computing examples
- `sql/` — model metadata, parameters, simulation runs, outputs, and assumptions
- `c/`, `cpp/`, `fortran/`, `rust/`, `go/` — compact numerical examples
- `docs/` — modeling notes and interpretation guidance
- `data/` — synthetic teaching data and parameter grids
- `outputs/` — generated outputs
- `notebooks/` — notebook placeholders

## Modeling Warning

These examples are educational. Real differential equation modeling should evaluate units, scale, parameter credibility, initial conditions, solver choice, step-size dependence, uncertainty, sensitivity, and validation against empirical evidence.
