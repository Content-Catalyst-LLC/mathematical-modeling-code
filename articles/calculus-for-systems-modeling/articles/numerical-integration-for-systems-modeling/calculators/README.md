# Article Calculators

Reusable calculator layer for **Numerical Integration for Systems Modeling**.

```bash
python3 python/article_calculator.py left-rectangle --rate-left 3.2 --h 0.25
python3 python/article_calculator.py trapezoid-step --rate-left 3 --rate-right 4 --h 0.25
python3 python/article_calculator.py simpson-one-third --f0 2 --f1 3 --f2 2 --h 0.5
python3 python/article_calculator.py benchmark-audit --start 0 --stop 10 --h 0.1
python3 python/article_calculator.py conservation-check --initial-stock 100 --final-stock 130 --integrated-inflow 50 --integrated-outflow 20
bash run_calculator_smoke_tests.sh
```
