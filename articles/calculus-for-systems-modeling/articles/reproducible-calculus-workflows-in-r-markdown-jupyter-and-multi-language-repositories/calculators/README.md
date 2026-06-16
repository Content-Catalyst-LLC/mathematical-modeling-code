# Article Calculators

Reusable calculator layer for **Reproducible Calculus Workflows in R Markdown, Jupyter, and Multi-Language Repositories**.

## Python examples

```bash
python3 python/article_calculator.py artifact-count --source 2 --generated 4
python3 python/article_calculator.py clean-run-status --expected 6 --found 6
python3 python/article_calculator.py output-register-score --documented 6 --total 6
python3 python/article_calculator.py notebook-drift-risk --executed-out-of-order true
python3 python/article_calculator.py governance-queue-count --warnings 3
python3 python/article_calculator.py reproducibility-warning --pattern validity
```

## R examples

```bash
Rscript r/article_calculator.R artifact-count 2 4
Rscript r/article_calculator.R clean-run-status 6 6
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
