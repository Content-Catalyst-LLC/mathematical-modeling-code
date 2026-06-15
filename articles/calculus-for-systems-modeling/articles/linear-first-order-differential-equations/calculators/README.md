# Article Calculators

Reusable calculator layer for **Linear First-Order Differential Equations**.

## Python examples

```bash
python3 python/article_calculator.py linear-rate --state 20 --input-rate 12 --loss-rate 0.4
python3 python/article_calculator.py equilibrium --input-rate 12 --loss-rate 0.4
python3 python/article_calculator.py analytical-solution --time 2 --initial 20 --input-rate 12 --loss-rate 0.4
python3 python/article_calculator.py euler-step --state 20 --input-rate 12 --loss-rate 0.4 --dt 0.1
python3 python/article_calculator.py compare-euler --initial 20 --input-rate 12 --loss-rate 0.4 --dt 0.1 --steps 20
```

## R examples

```bash
Rscript r/article_calculator.R linear-rate 20 12 0.4
Rscript r/article_calculator.R equilibrium 12 0.4
Rscript r/article_calculator.R analytical-solution 2 20 12 0.4
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
