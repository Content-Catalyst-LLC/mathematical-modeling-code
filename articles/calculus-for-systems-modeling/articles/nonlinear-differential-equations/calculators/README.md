# Article Calculators

Reusable calculator layer for **Nonlinear Differential Equations**.

## Python examples

```bash
python3 python/article_calculator.py logistic-rate --state 10 --growth-rate 0.6 --carrying-capacity 100
python3 python/article_calculator.py logistic-equilibria --carrying-capacity 100
python3 python/article_calculator.py bistable-rate --state 0.35 --threshold 0.4
python3 python/article_calculator.py bistable-equilibria --threshold 0.4
python3 python/article_calculator.py euler-step --model logistic --state 10 --growth-rate 0.6 --carrying-capacity 100 --dt 0.05
python3 python/article_calculator.py simulate --model logistic --state 10 --growth-rate 0.6 --carrying-capacity 100 --dt 0.05 --steps 100
```

## R examples

```bash
Rscript r/article_calculator.R logistic-rate 10 0.6 100
Rscript r/article_calculator.R logistic-equilibria 100
Rscript r/article_calculator.R bistable-rate 0.35 0.4
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
