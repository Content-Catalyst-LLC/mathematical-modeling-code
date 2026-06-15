# Mathematical Modeling in an Age of Complexity

Companion code and reproducible workflows for **“Mathematical Modeling in an Age of Complexity”** in the **Mathematical Modeling** knowledge series.

This folder treats complexity modeling as a governed comparison process: model portfolios, scenario libraries, fragility scores, robust-value comparison, adaptive trigger flags, interdependence review, equity review, uncertainty communication, and responsible complexity modeling artifacts.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional complexity model registration, scenario review, fragility scoring, robustness comparison, adaptive trigger review, and governance-ready outputs.

## Folder structure

```text
articles/mathematical-modeling-in-an-age-of-complexity/
├── python/      # Complexity model register, scenario review, governance card, tests
├── r/           # Complexity scenario summary and robustness review
├── julia/       # Complexity scenario fragility and robust-value summary
├── sql/         # Complexity governance schema and queries
├── haskell/     # Typed complexity model records
├── rust/        # Strongly typed complexity record CLI
├── go/          # Lightweight complexity scenario summary
├── cpp/         # Scenario fragility scoring example
├── fortran/     # Scientific-computing fragility scoring
├── c/           # Low-level scenario scoring
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Complexity, uncertainty, plural modeling, scenarios, governance
├── data/        # Model register, scenarios, domain guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for complexity models and scenarios
```

## Run everything available

```bash
make all
```

## Dependency-light smoke test

```bash
make smoke
```

## Selected targets

```bash
make python
make test
make r
make sql
make julia
make haskell
make rust
make go
make cpp
make fortran
make c
```

## Minimal Python run

```bash
python3 python/mathematical_modeling_in_an_age_of_complexity/cli.py --output-dir outputs
```

## Modeling themes

- nonlinear dynamics, feedback loops, thresholds, emergence, and adaptation;
- interdependence, cascading risk, systemic fragility, and resilience;
- deep uncertainty, scenario reasoning, robust-value comparison, and adaptive triggers;
- model pluralism, participatory interpretation, use limits, monitoring, and accountability.

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
