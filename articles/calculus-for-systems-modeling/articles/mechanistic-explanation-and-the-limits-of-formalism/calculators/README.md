# Article Calculators

Reusable calculator layer for **Mechanistic Explanation and the Limits of Formalism**.

## Python examples

```bash
python3 python/article_calculator.py mechanism-score --entities 1 --activities 1 --relations 1 --evidence 0 --scope 1
python3 python/article_calculator.py formalism-risk --parameter-meaning 0 --evidence-link 0 --validation-scope 1 --claim-boundary 0
python3 python/article_calculator.py claim-type --mechanism-evidence 1 --validation-data 0 --scenario-only 0
python3 python/article_calculator.py parameter-interpretation --source calibrated --has-unit 1 --has-range 1
python3 python/article_calculator.py black-box-risk --opaque-steps 2 --hidden-parameters 1 --missing-diagnostics 1
python3 python/article_calculator.py explanation-warning --pattern formal_precision
```

## R examples

```bash
Rscript r/article_calculator.R mechanism-score 1 1 1 0 1
Rscript r/article_calculator.R formalism-risk 0 0 1 0
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
