# AI-Assisted Modeling and Human Judgment

Companion code and reproducible workflows for **“AI-Assisted Modeling and Human Judgment”** in the **Mathematical Modeling** knowledge series.

This folder treats AI-assisted modeling as a governed workflow: AI assistance registers, human judgment review, automation-bias risk scoring, provenance tracking, validation checkpoints, escalation rules, use-limit statements, and accountable decision ownership.

## Quality standard

This article folder follows the upgraded Mathematical Modeling repository standard:

- article-level `README.md`;
- article-level `Makefile`;
- `article-metadata.yml`;
- WordPress GitHub embed snippet;
- Python, R, Julia, SQL, Haskell, Rust, Go, C++, Fortran, and C;
- notebooks, documentation, data, outputs, schemas, and Canvas metadata;
- generated tables, figures, JSON outputs, logs, and smoke checks;
- professional AI assistance registration, human judgment risk review, provenance review, automation-bias scoring, escalation rules, use limits, and model governance artifacts.

## Folder structure

```text
articles/ai-assisted-modeling-and-human-judgment/
├── python/      # AI assistance register, judgment review, governance card, tests
├── r/           # AI-assisted modeling oversight summary
├── julia/       # Human judgment risk and escalation summary
├── sql/         # AI-assisted modeling governance schema and queries
├── haskell/     # Typed AI assistance records
├── rust/        # Strongly typed AI assistance record CLI
├── go/          # Lightweight judgment risk summary
├── cpp/         # Judgment risk scoring example
├── fortran/     # Scientific-computing oversight scoring
├── c/           # Low-level judgment risk scoring
├── notebooks/   # Notebook-ready walkthrough
├── docs/        # AI assistance, human judgment, provenance, validation, governance
├── data/        # AI assistance register, judgment cases, domain guide
├── outputs/     # Generated results, figures, JSON, logs, backups
├── canvas/      # Catalyst Canvas companion metadata
└── schemas/     # JSON schemas for AI assistance and human judgment records
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
python3 python/ai_assisted_modeling_and_human_judgment/cli.py --output-dir outputs
```

## Modeling themes

- AI as modeling assistant, not modeling authority;
- human judgment for purpose, evidence, interpretation, values, and consequences;
- provenance, prompt logs, assumption records, validation checkpoints, and audit trails;
- automation bias, false authority, use limits, escalation, and decision ownership.

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
