# Article Calculators

Reusable calculator layer for **Separable Equations and Simple Dynamic Laws**.

```bash
python3 python/article_calculator.py exponential-solution --time 2 --initial 10 --growth-rate 0.25
python3 python/article_calculator.py exponential-rate --state 10 --growth-rate 0.25
python3 python/article_calculator.py logistic-solution --time 2 --initial 10 --growth-rate 0.25 --capacity 100
python3 python/article_calculator.py logistic-rate --state 10 --growth-rate 0.25 --capacity 100
python3 python/article_calculator.py compare-euler --model logistic --initial 10 --growth-rate 0.25 --capacity 100 --dt 0.1 --steps 20
bash run_calculator_smoke_tests.sh
```
