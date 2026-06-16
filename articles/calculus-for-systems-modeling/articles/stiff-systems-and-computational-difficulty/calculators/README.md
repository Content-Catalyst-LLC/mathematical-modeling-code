# Article Calculators

Reusable calculator layer for **Stiff Systems and Computational Difficulty**.

## Python examples

```bash
python3 python/article_calculator.py explicit-amplification --step-size 0.1 --eigenvalue -50
python3 python/article_calculator.py implicit-amplification --step-size 0.1 --eigenvalue -50
python3 python/article_calculator.py stiffness-ratio --eigenvalues -1,-50
python3 python/article_calculator.py stable-explicit-step-bound --eigenvalue -50
python3 python/article_calculator.py method-comparison --step-size 0.1 --eigenvalue -50
python3 python/article_calculator.py stiffness-warning-note --symptom step_rejection
```

## R examples

```bash
Rscript r/article_calculator.R explicit-amplification 0.1 -50
Rscript r/article_calculator.R stiffness-ratio "-1,-50"
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
