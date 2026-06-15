# Calculus for Systems Modeling

Companion repository folder for the **Calculus for Systems Modeling** article map and nested article-level workflows.

This folder supports calculus-based systems modeling across functions, domains, limits, continuity, differentiability, derivatives, integration, improper integrals, accumulation, exposure, flow-to-stock reasoning, sequences, series, convergence, convergence tests, infinite approximation, numerical methods, and responsible mathematical interpretation.

## Nested article folders

Article-specific code lives under:

```text
articles/calculus-for-systems-modeling/articles/
```

Current active folders include:

```text
articles/sequences-series-and-the-logic-of-convergence/
articles/convergence-tests-and-the-discipline-of-infinite-approximation/
```

## Advanced mathematical standard

Each active article folder should include an `advanced/` layer with formal definitions, propositions, counterexamples, numerical checks, invariant/domain review, generated audit reports, and tests beyond smoke checks.

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
