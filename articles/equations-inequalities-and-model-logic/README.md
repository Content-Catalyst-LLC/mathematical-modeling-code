# Equations, Inequalities, and Model Logic

Companion code and reproducible workflows for **“Equations, Inequalities, and Model Logic”** in the **Mathematical Modeling** knowledge series.

This folder treats equations, inequalities, domains, feasible sets, and conditional logic as explicit model design objects. It supports equation registers, inequality audits, formal statement review, domain checks, resource-model logic diagnostics, conditional rules, transformation review, and reproducible computational workflows.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and logic-review scaffolding.

## Folder structure

```text
articles/equations-inequalities-and-model-logic/
├── python/      # Formal statement register, logic diagnostics, CLI, tests
├── r/           # Constraint and logic review workflow
├── julia/       # Numerical equation/inequality scenario workflow
├── sql/         # Formal logic governance schema and diagnostic queries
├── haskell/     # Typed formal model logic
├── rust/        # Strongly typed statement-review CLI
├── go/          # Lightweight logic scenario workflow
├── cpp/         # Engineering-style constrained logic model
├── fortran/     # Scientific-computing constrained simulation
├── c/           # Low-level deterministic constrained simulation
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Equation status, inequality status, logic, transformations
├── data/        # Formal statement registers and scenario inputs
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for statements and scenarios
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
python3 python/equations_inequalities_model_logic/cli.py --output-dir outputs
```

## Modeling themes

- equations as definitions, identities, balances, updates, fitted relationships, and equilibrium conditions;
- inequalities as domains, bounds, thresholds, constraints, and feasible-set definitions;
- formal model logic through if-then rules, domains, transformations, and solver behavior;
- resource model logic with shortage, overflow, capacity, and threshold rules;
- validation of domain, constraint, and logic activation;
- typed model governance and reproducibility.
