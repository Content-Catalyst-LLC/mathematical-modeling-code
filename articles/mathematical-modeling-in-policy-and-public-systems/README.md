# Mathematical Modeling in Policy and Public Systems

Companion code and reproducible workflows for **“Mathematical Modeling in Policy and Public Systems”** in the **Mathematical Modeling** knowledge series.

This folder treats policy modeling as public evidence infrastructure: policy model registers, public-system option review, budget and equity constraints, risk summaries, scenario reasoning, governance artifacts, typed policy model records, and responsible public decision-support workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional policy model registration, option review, budget/equity/risk diagnostics, governance scaffolding, and reproducible decision-support artifacts.

## Folder structure

```text
articles/mathematical-modeling-in-policy-and-public-systems/
├── python/      # Policy model register, option review, public-system evidence card, tests
├── r/           # Policy option summary and equity review
├── julia/       # Policy option score summary
├── sql/         # Policy modeling governance schema and queries
├── haskell/     # Typed policy model records
├── rust/        # Strongly typed policy model record CLI
├── go/          # Lightweight policy option summary
├── cpp/         # Engineering-style public option review
├── fortran/     # Scientific-computing policy option model
├── c/           # Low-level public option example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Public systems, policy options, equity, governance, ethics
├── data/        # Policy model register, options, domain guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for policy model records and policy options
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
python3 python/mathematical_modeling_in_policy_and_public_systems/cli.py --output-dir outputs
```

## Modeling themes

- policy models as structured public reasoning tools;
- problem boundaries, populations, public outcomes, and institutions;
- policy option comparison under budget, risk, feasibility, uncertainty, and equity constraints;
- scenario reasoning and robustness under deep uncertainty;
- public communication, use limits, governance, and accountability;
- reproducible public-system decision-support artifacts.

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
