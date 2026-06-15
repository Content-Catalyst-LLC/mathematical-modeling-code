# Article Calculators

Reusable calculator layer for **Equilibrium, Stability, and Local Dynamics**.

## Python examples

```bash
python3 python/article_calculator.py classify-derivative --derivative-value -0.6
python3 python/article_calculator.py logistic-stability --equilibrium 100 --growth-rate 0.6 --carrying-capacity 100
python3 python/article_calculator.py bistable-stability --equilibrium 0.4 --threshold 0.4
python3 python/article_calculator.py numerical-derivative --model bistable --state 0.4 --threshold 0.4
python3 python/article_calculator.py equilibrium-table --growth-rate 0.6 --carrying-capacity 100 --threshold 0.4
```

## R examples

```bash
Rscript r/article_calculator.R classify-derivative -0.6
Rscript r/article_calculator.R logistic-stability 100 0.6 100
Rscript r/article_calculator.R bistable-stability 0.4 0.4
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
