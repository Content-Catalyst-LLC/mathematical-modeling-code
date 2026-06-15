# Probability for Systems Modeling

This article folder supports reproducible examples for probability-based systems modeling.

## Topics

- probability distributions
- random variables
- expectation and variance
- Monte Carlo simulation
- Bayesian updating
- Markov chains
- stochastic transition models
- reliability analysis
- rare-event simulation
- uncertainty analysis
- probabilistic sensitivity analysis
- responsible uncertainty interpretation

## Folder Structure

- `python/` — Monte Carlo, Bayesian updating, Markov chains, reliability, rare events
- `r/` — random sampling, Monte Carlo, probabilistic summaries, Bayesian updating
- `julia/` — compact probability simulation examples
- `sql/` — probabilistic model metadata, parameters, simulation runs, outputs, and assumptions
- `c/`, `cpp/`, `fortran/`, `rust/`, `go/` — compact numerical probability examples
- `docs/` — modeling notes and interpretation guidance
- `data/` — synthetic teaching inputs and probability parameters
- `outputs/` — generated outputs
- `notebooks/` — notebook placeholders

## Modeling Warning

These examples are educational. Real probabilistic modeling should evaluate distributional assumptions, dependence, data quality, calibration, rare-event behavior, tail sensitivity, simulation uncertainty, and the interpretation of probabilities in context.

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
