# What Is Calculus for Systems Modeling?

Companion code and reproducible workflows for **“What Is Calculus for Systems Modeling?”**

This nested article folder demonstrates calculus as a systems-modeling language for rates, accumulation, dynamic simulation, sensitivity analysis, and typed model representation.

## Folder structure

```text
python/      # Package-style Python workflow and tests
r/           # Base R sensitivity workflow
julia/       # Lightweight Julia dynamic simulation
sql/         # Scenario schema and model-run tables
haskell/     # Typed state and parameter model
c/           # C implementation of a simple dynamic model
cpp/         # C++ implementation of a simple dynamic model
fortran/     # Fortran implementation of a simple dynamic model
rust/        # Rust CLI-style simulation summary
go/          # Go simulation summary
notebooks/   # Notebook-ready walkthrough
docs/        # Modeling notes and governance guidance
data/        # Synthetic teaching data
outputs/     # Generated tables, JSON, logs, figures
schemas/     # JSON schemas
canvas/      # Canvas-ready metadata
```

## Run smoke checks

```bash
make smoke
```

## Run all available targets

```bash
make all
```

## Principle

Calculus supports interpretation. It does not replace model assumptions, uncertainty analysis, validation, or responsible systems thinking.
