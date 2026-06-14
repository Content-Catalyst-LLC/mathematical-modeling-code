# Functions, Variables, and Mathematical Representation

Companion code and reproducible workflows for **“Functions, Variables, and Mathematical Representation”** in the **Calculus for Systems Modeling** series.

This folder demonstrates how functions, variables, parameters, domains, functional forms, and model registries support calculus-based systems modeling.

## Themes

- functions as modeled relationships;
- variables as interpreted quantities with units and roles;
- parameters as documented assumptions;
- functional forms as system-behavior claims;
- typed model records in Haskell;
- structured registries in SQL;
- computational comparison of linear, exponential, logistic, and threshold representations;
- reproducible outputs for review and interpretation.

## Folder structure

```text
python/      # Package-style functional-form comparison workflow
r/           # Base R functional-form comparison
julia/       # Lightweight Julia representation workflow
sql/         # Functional model registry and parameters
haskell/     # Typed variables, parameters, and outputs
c/           # C functional-form comparison
cpp/         # C++ functional-form comparison
fortran/     # Fortran functional-form comparison
rust/        # Rust representation summary
go/          # Go representation summary
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

Mathematical representation is part of the model, not a pre-modeling formality. Variables, functional forms, parameters, and boundaries should be explicit, documented, and reviewable.
