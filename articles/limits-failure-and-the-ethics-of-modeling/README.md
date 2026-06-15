# Limits, Failure, and the Ethics of Modeling

Companion code and reproducible workflows for **“Limits, Failure, and the Ethics of Modeling”** in the **Mathematical Modeling** knowledge series.

This folder treats model limits and ethics as a reproducible governance workflow: model failure registers, ethics risk scoring, uncertainty and false-precision diagnostics, equity and accountability scoring, use-limit statements, governance queues, typed model ethics records, and responsible modeling artifacts.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional model failure registration, ethics risk scoring, governance review, use-limit documentation, accountability review, and reproducible decision-support artifacts.

## Folder structure

```text
articles/limits-failure-and-the-ethics-of-modeling/
├── python/      # Model failure register, ethics risk review, governance card, tests
├── r/           # Failure-mode summary and governance queue
├── julia/       # Model ethics risk summary
├── sql/         # Model ethics governance schema and queries
├── haskell/     # Typed model ethics records
├── rust/        # Strongly typed model ethics record CLI
├── go/          # Lightweight ethics risk summary
├── cpp/         # Governance scoring example
├── fortran/     # Scientific-computing ethics risk scoring
├── c/           # Low-level ethics risk scoring
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # Limits, failure modes, uncertainty, equity, governance, accountability
├── data/        # Model failure register, risk cases, ethics guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for model failure records and ethics risk cases
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
python3 python/limits_failure_and_the_ethics_of_modeling/cli.py --output-dir outputs
```

## Modeling themes

- models as partial representations with use limits;
- failure modes across framing, data, design, validation, communication, deployment, monitoring, and governance;
- uncertainty, false precision, bias, misuse, scope creep, and accountability gaps;
- ethical risk scoring across severity, likelihood, detectability, uncertainty, equity, and accountability;
- use-limit statements, human decision ownership, governance queues, and model retirement criteria.

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
