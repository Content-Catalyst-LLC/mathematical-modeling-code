# Scientific Computing for Modeling Workflows

Companion code and reproducible workflows for **“Scientific Computing for Modeling Workflows”** in the **Mathematical Modeling** knowledge series.

This folder treats scientific computing as accountable modeling infrastructure: workflow registers, code/data/configuration separation, run manifests, output hashes, reproducibility diagnostics, validation checks, review queues, and decision-support governance.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional workflow governance, validation, reproducibility, automation, and decision-support scaffolding.

## Folder structure

```text
articles/scientific-computing-for-modeling-workflows/
├── python/      # Workflow register, run manifest, output hashes, tests
├── r/           # Workflow review and reproducibility diagnostics
├── julia/       # Resource workflow and manifest summary
├── sql/         # Workflow-governance schema and diagnostic queries
├── haskell/     # Typed workflow records
├── rust/        # Strongly typed workflow component CLI
├── go/          # Lightweight reproducible workflow summary
├── cpp/         # Engineering-style resource workflow
├── fortran/     # Scientific-computing trajectory summary
├── c/           # Low-level workflow run example
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Workflow, reproducibility, validation, and ethics guides
├── data/        # Workflow register and scenario inputs
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for workflow records and scenarios
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
python3 python/scientific_computing_modeling_workflows/cli.py --output-dir outputs
```

## Modeling themes

- scientific computing as modeling infrastructure;
- reproducible inputs, configuration, environments, and outputs;
- workflow registers, run manifests, output hashes, and logs;
- code tests, validation checks, review queues, and model governance;
- multi-language companion implementations for transparent computation.

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
