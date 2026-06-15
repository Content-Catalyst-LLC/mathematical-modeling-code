# Scientific Computing for Systems Modeling

This article folder supports reproducible examples for scientific computing in systems modeling.

## Topics

- numerical integration
- root finding
- finite differences
- dynamic simulation
- parameter sweeps
- sensitivity analysis
- Monte Carlo simulation
- optimization
- data pipelines
- structured outputs
- SQL model-run metadata
- reproducible workflow design
- responsible computational interpretation

## Folder Structure

- `python/` — numerical methods, simulations, parameter sweeps, Monte Carlo, pipelines
- `r/` — reproducible simulation, sensitivity, visualization-ready outputs
- `julia/` — compact scientific-computing examples
- `sql/` — model run metadata, parameters, outputs, diagnostics
- `c/`, `cpp/`, `fortran/`, `rust/`, `go/` — compact numerical examples
- `docs/` — modeling notes and workflow guidance
- `data/` — synthetic teaching data and parameter grids
- `outputs/` — generated outputs
- `notebooks/` — notebook placeholders

## Modeling Warning

These examples are educational. Real scientific computing workflows should evaluate numerical stability, convergence, solver settings, data provenance, parameter credibility, sensitivity, uncertainty, reproducibility, and validation against empirical evidence.

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
