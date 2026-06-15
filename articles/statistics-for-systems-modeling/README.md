# Statistics for Systems Modeling

This article folder supports reproducible examples for statistics-based systems modeling.

## Topics

- descriptive statistics
- estimation
- confidence intervals
- regression
- uncertainty
- bootstrap resampling
- model diagnostics
- prediction error
- simulation-based inference
- responsible statistical interpretation

## Folder Structure

- `python/` — regression, bootstrap, diagnostics, and prediction error
- `r/` — estimation, uncertainty, diagnostics, and visualization
- `julia/` — compact statistical computing examples
- `sql/` — statistical model metadata and results records
- `c/`, `cpp/`, `fortran/`, `rust/`, `go/` — compact numerical examples
- `docs/` — modeling notes
- `data/` — synthetic input data
- `outputs/` — generated outputs
- `notebooks/` — notebook placeholders

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
