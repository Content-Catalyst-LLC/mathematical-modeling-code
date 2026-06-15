# Mathematical Modeling in Ecology and Sustainability

Companion code and reproducible workflows for **“Mathematical Modeling in Ecology and Sustainability”** in the **Mathematical Modeling** knowledge series.

This folder treats ecological and sustainability modeling as stewardship evidence infrastructure: ecology model registers, renewable resource dynamics, climate stress scenarios, resilience margins, threshold diagnostics, adaptive management notes, governance artifacts, typed ecology model records, and responsible sustainability interpretation workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional ecological model registration, resource-stock simulation, resilience review, climate stress analysis, threshold diagnostics, governance scaffolding, and reproducible sustainability artifacts.

## Folder structure

```text
articles/mathematical-modeling-in-ecology-and-sustainability/
├── python/      # Ecology model register, resource scenarios, sustainability review card, tests
├── r/           # Scenario summary and resilience review
├── julia/       # Resource scenario summary
├── sql/         # Ecology and sustainability governance schema and queries
├── haskell/     # Typed ecology and sustainability records
├── rust/        # Strongly typed ecology model record CLI
├── go/          # Lightweight resource scenario summary
├── cpp/         # Engineering-style resource scenario review
├── fortran/     # Scientific-computing resource model
├── c/           # Low-level resource stock example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Ecology, resilience, sustainability, thresholds, governance, ethics
├── data/        # Ecology model register, resource scenarios, domain guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for ecology records and resource scenarios
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
python3 python/mathematical_modeling_in_ecology_and_sustainability/cli.py --output-dir outputs
```

## Modeling themes

- ecological models as dynamic sustainability representations;
- renewable resource stocks, regeneration, extraction, and thresholds;
- resilience margins, climate stress, scenario pathways, and adaptive management;
- biodiversity, network dependencies, and coupled human-natural systems;
- uncertainty, sensitivity, field evidence, and responsible use limits;
- reproducible sustainability review and ecological governance artifacts.

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
