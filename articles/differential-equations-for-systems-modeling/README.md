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

## Self-contained calculators

This article folder includes a reusable calculator layer in `calculators/` for quick command-line exploration of derivatives, definite integrals, finite differences, ODE solvers, logistic dynamics, and parameter sensitivity. The scripts are intentionally self-contained so they can be run without installing article-specific dependencies.

Example commands:

```bash
cd calculators
python3 python/model_calculator.py derivative --expr "sin(x)*exp(-x)" --x 1.5
python3 python/model_calculator.py integral --expr "x*x + sin(x)" --a 0 --b 10 --method simpson
python3 python/model_calculator.py rk4 --ode "0.2*y*(1-y/100)" --y0 10 --dt 0.1 --steps 50
bash run_calculator_smoke_tests.sh
```
