# Article Calculators

Reusable calculator layer for **Approximation Error, Truncation, and Local Validity**.

These calculators are self-contained, command-line runnable, and designed to become a computational source layer for future website widgets.

## Python examples

```bash
python3 python/article_calculator.py approximation-error --true-value 2.718281828 --approximation 2.716666667
python3 python/article_calculator.py relative-error --true-value 2.718281828 --approximation 2.716666667
python3 python/article_calculator.py taylor-exp --x 1 --order 10
python3 python/article_calculator.py truncation-sweep --x 1 --max-order 12
python3 python/article_calculator.py derivative-step --x 2 --h 0.01
python3 python/article_calculator.py integral-step --a 0 --b 1 --steps 100
python3 python/article_calculator.py euler --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py rk4 --x0 1 --rate 0.5 --dt 0.1 --steps 10
python3 python/article_calculator.py logistic --initial 10 --carrying-capacity 100 --rate 0.25 --steps 20
python3 python/article_calculator.py finite-diff --values 1,2,4,7,11
python3 python/article_calculator.py sensitivity --parameter-min 0.1 --parameter-max 1.0 --samples 10
```

## R examples

```bash
Rscript r/article_calculator.R approximation-error 2.718281828 2.716666667
Rscript r/article_calculator.R taylor-exp 1 10
Rscript r/article_calculator.R logistic 10 100 0.25 20
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
