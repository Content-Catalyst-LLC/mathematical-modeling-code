# State Variables and System Representation

Companion code and reproducible workflows for **“State Variables and System Representation”** in the **Mathematical Modeling** knowledge series.

This folder treats state variables, system representation, state-space forms, observability, hidden state, feedback, and representation adequacy as explicit model design objects. It supports state-variable registers, role tables, representation comparisons, condition-aware dynamic models, alternative state specifications, and reproducible computational workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and representation-review scaffolding.

## Folder structure

```text
articles/state-variables-and-system-representation/
├── python/      # State register, representation scenarios, CLI, tests
├── r/           # State diagnostics and representation review
├── julia/       # Numerical state-representation scenario workflow
├── sql/         # State-governance schema and diagnostic queries
├── haskell/     # Typed state representations
├── rust/        # Strongly typed variable-role review CLI
├── go/          # Lightweight state-representation workflow
├── cpp/         # Engineering-style state model
├── fortran/     # Scientific-computing state simulation
├── c/           # Low-level deterministic state simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # State registers, observability, state-space, ethics
├── data/        # State-variable registers and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for state variables and scenarios
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
python3 python/state_variables_system_representation/cli.py --output-dir outputs
```

## Modeling themes

- state variables as system memory;
- state, input, output, parameter, decision, and diagnostic roles;
- state-space representation;
- observability and hidden state;
- storage-only, adaptive-demand, and condition-aware representations;
- state adequacy, representation sensitivity, and governance.

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
