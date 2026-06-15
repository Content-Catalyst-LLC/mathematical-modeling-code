# Agent-Based Models and Emergent Behavior

Companion code and reproducible workflows for **“Agent-Based Models and Emergent Behavior”** in the **Mathematical Modeling** knowledge series.

This folder treats agents, states, local rules, interaction structures, environments, schedules, stochastic replications, ensemble diagnostics, emergence review, and model governance as explicit mathematical modeling objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and ABM review scaffolding.

## Folder structure

```text
articles/agent-based-models-and-emergent-behavior/
├── python/      # ABM register, adoption simulation, ensemble diagnostics, tests
├── r/           # Simulation review and ensemble diagnostics
├── julia/       # Adoption simulation workflow
├── sql/         # ABM-governance schema and diagnostic queries
├── haskell/     # Typed ABM records
├── rust/        # Strongly typed ABM component CLI
├── go/          # Lightweight adoption simulation
├── cpp/         # Engineering-style adoption simulation
├── fortran/     # Scientific-computing simulation summary
├── c/           # Low-level adoption simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Rule codebook, emergence review, validation, ethics
├── data/        # ABM register and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for ABM records and scenarios
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
python3 python/agent_based_models_emergent_behavior/cli.py --output-dir outputs
```

## Modeling themes

- agents as formal model objects;
- states, rules, interactions, environments, and schedules;
- emergence as traceable bottom-up model output;
- ensemble simulation rather than single-run storytelling;
- calibration, pattern-oriented validation, and sensitivity review;
- responsible use of ABM outputs for decision support.

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
