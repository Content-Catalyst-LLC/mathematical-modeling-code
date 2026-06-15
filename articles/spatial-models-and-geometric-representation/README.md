# Spatial Models and Geometric Representation

Companion code and reproducible workflows for **“Spatial Models and Geometric Representation”** in the **Mathematical Modeling** knowledge series.

This folder treats coordinate systems, geometric representations, distance metrics, accessibility measures, spatial uncertainty, boundary review, and model validation as explicit mathematical modeling objects.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model governance, validation, uncertainty, sensitivity, and spatial-review scaffolding.

## Folder structure

```text
articles/spatial-models-and-geometric-representation/
├── python/      # Spatial register, distance/accessibility diagnostics, tests
├── r/           # Spatial review and distance diagnostics
├── julia/       # Coordinate and accessibility workflow
├── sql/         # Spatial-governance schema and diagnostic queries
├── haskell/     # Typed spatial model records
├── rust/        # Strongly typed spatial component CLI
├── go/          # Lightweight distance diagnostics
├── cpp/         # Engineering-style distance/accessibility computation
├── fortran/     # Scientific-computing distance diagnostics
├── c/           # Low-level distance diagnostics
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Geometry guide, distance review, spatial ethics
├── data/        # Spatial register, locations, and component guide
├── outputs/     # Generated results, tables, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for spatial records and locations
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
python3 python/spatial_models_geometric_representation/cli.py --output-dir outputs
```

## Modeling themes

- geometry as mathematical representation;
- coordinate systems, projections, and units;
- distance metrics, buffers, accessibility, and exposure;
- scale, resolution, aggregation, and boundary review;
- spatial uncertainty and validation;
- responsible use of map-like outputs for decision support.

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
