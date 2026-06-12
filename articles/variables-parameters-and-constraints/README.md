# Variables, Parameters, and Constraints

Companion code and reproducible workflows for **“Variables, Parameters, and Constraints”** in the **Mathematical Modeling** knowledge series.

This folder treats variables, parameters, and constraints as explicit, reviewable model components. It supports component registers, variable-role review, parameter audits, constraint diagnostics, unit/domain checks, resource stock-flow scenarios, validation planning, and reproducible computational workflows.

## Included layers

- Python package and tests
- R diagnostics
- Julia numerical workflow
- SQL governance schema and queries
- Haskell typed component records
- Rust typed review CLI
- Go, C++, Fortran, and C constrained simulations
- docs, data, outputs, notebooks, schemas, and Canvas metadata

## Run

```bash
make smoke
make all
```

## Minimal Python run

```bash
python3 python/variables_parameters_constraints/cli.py --output-dir outputs
```
