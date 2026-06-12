# What Is Mathematical Modeling?

Companion code and reproducible workflows for the article **“What Is Mathematical Modeling?”** in the Mathematical Modeling knowledge series.

This folder treats mathematical modeling as a professional workflow rather than a single equation. It includes examples for mathematicians, engineers, statisticians, scientific programmers, and decision-support analysts.

## Repository contents

```text
articles/what-is-mathematical-modeling/
├── python/      # Core reproducible modeling package, CLI, tests
├── r/           # Scenario diagnostics and visualization workflow
├── julia/       # Numerical modeling and parameter sweep workflow
├── sql/         # Modeling metadata, scenario, validation, and run schema
├── c/           # Low-level deterministic simulation example
├── cpp/         # Engineering-style model class and diagnostics
├── fortran/     # Scientific-computing style numerical simulation
├── rust/        # Strongly typed modeling workflow
├── go/          # Concurrent-style scenario workflow
├── haskell/     # Functional modeling workflow
├── notebooks/   # Notebook-ready computational demonstrations
├── docs/        # Modeling assumptions, V&V, UQ, engineering/statistical notes
├── data/        # Synthetic parameters, observations, scenarios
├── outputs/     # Generated results, tables, figures, JSON, logs
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for inputs and outputs
```

## Professional modeling coverage

This scaffold includes:

- continuous-time and discrete-time logistic modeling;
- Euler and RK4 numerical integration;
- scenario comparison;
- calibration against synthetic observations;
- residual diagnostics;
- one-at-a-time sensitivity analysis;
- Monte Carlo uncertainty propagation;
- validation and adequacy reporting;
- dimensional-consistency notes;
- SQL tables for model governance and reproducibility;
- multi-language implementations for engineering/scientific computing contexts;
- notebook-ready materials for exposition, experimentation, and teaching.

## Minimal smoke test

From this article folder:

```bash
python3 python/what_is_mathematical_modeling/cli.py --steps 96 --output-dir outputs/smoke
```

The top-level population script also runs available language checks automatically.
