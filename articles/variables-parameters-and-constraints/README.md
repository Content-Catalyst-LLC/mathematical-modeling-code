# Variables, Parameters, and Constraints

Companion code and reproducible workflows for **“Variables, Parameters, and Constraints”** in the **Mathematical Modeling** knowledge series.

This folder treats variables, parameters, and constraints as explicit, reviewable model components. It supports component registers, variable-role review, parameter audits, constraint diagnostics, unit/domain checks, resource stock-flow scenarios, validation planning, and reproducible computational workflows.

## Included layers

- Python package and tests
- R diagnostics
- Julia numerical workflow
- SQL governance schema and queries
- Haskell typed component records
- Rust typed review CLI
- Go, C++, Fortran, and C constrained simulations
- docs, data, outputs, notebooks, schemas, and Canvas metadata

## Run

```bash
make smoke
make all
```

## Minimal Python run

```bash
python3 python/variables_parameters_constraints/cli.py --output-dir outputs
```

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
