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
