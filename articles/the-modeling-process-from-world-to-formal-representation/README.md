# The Modeling Process: From World to Formal Representation

This companion folder supports the article **“The Modeling Process: From World to Formal Representation”** in the **Mathematical Modeling** series.

The folder is designed as a professional mathematical-modeling scaffold rather than a toy example. It demonstrates how a real-world question becomes a formal representation through framing, abstraction, boundary selection, variable design, assumptions, formulation, computation, evidence comparison, validation planning, uncertainty review, and revision.

## Folder structure

```text
articles/the-modeling-process-from-world-to-formal-representation/
python/    modeling-process audit package, CLI, smoke tests
r/         scenario review, assumption audit, and diagnostic visualization
julia/     typed numerical workflow for reservoir stock-flow scenarios
sql/       model-governance schema, scenario metadata, validation records
haskell/   typed model-process records and review-state representation
rust/      command-line process-audit scaffold
go/        scenario-summary command-line workflow
cpp/       engineering-style reservoir model class
fortran/   scientific-computing stock-flow simulation
c/         low-level deterministic scenario simulation
notebooks/ notebook-ready modeling-process walkthrough
docs/      specification, validation plan, assumption register, engineering/statistical notes
data/      scenario definitions, observed-storage sample, assumptions
outputs/   generated tables, figures, JSON, logs
canvas/    Catalyst Canvas manifest and governance metadata
schemas/   JSON schemas for model inputs and outputs
```

## Modeling themes

- Movement from real-world context to formal representation
- Model purpose and intended use
- Abstraction, boundaries, scale, and scope
- Variables, parameters, constraints, assumptions, and outputs
- Reservoir stock-flow model as a transparent worked example
- Scenario comparison and shortage-risk diagnostics
- Assumption logging and sensitivity planning
- Calibration/validation distinction
- Typed model-process governance with Haskell
- Reproducible terminal workflows for engineers, mathematicians, and statisticians

## Suggested run order

From this article folder:

```bash
make all
```

Or run selected targets:

```bash
make python
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
python3 python/modeling_process/cli.py --output-dir outputs
```

## Notes

The data are synthetic and intended for methods demonstration. The workflows are designed to be extended into professional validation, sensitivity, uncertainty quantification, statistical calibration, engineering review, and model-governance systems.

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
