# Article Calculators

Reusable calculator layer for **Interpretation, Assumptions, and Responsible Mathematical Modeling**.

## Python examples

```bash
python3 python/article_calculator.py purpose-fit --teaching 1 --exploratory 0 --predictive 0 --decision-support 0
python3 python/article_calculator.py assumption-risk --hidden-assumptions 2 --normative-assumptions 1 --solver-undocumented 1
python3 python/article_calculator.py claim-boundary --purpose predictive --validated 0 --uncertainty-recorded 1 --scope-recorded 1
python3 python/article_calculator.py parameter-evidence --has-unit 1 --has-source 1 --has-range 0 --has-uncertainty 0
python3 python/article_calculator.py communication-risk --overprecision 1 --scenario-confusion 1 --hidden-values 0 --audience-mismatch 1
python3 python/article_calculator.py responsibility-warning --pattern claim_boundary
```

## R examples

```bash
Rscript r/article_calculator.R assumption-risk 2 1 1
Rscript r/article_calculator.R parameter-evidence 1 1 0 0
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
