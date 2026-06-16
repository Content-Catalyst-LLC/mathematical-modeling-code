# Advanced Population Dynamics Calculators

```bash
python3 python/article_calculator.py exponential --n0 100 --r 0.08 --t 40
python3 python/article_calculator.py logistic --n0 100 --r 0.08 --k 1000 --t 40
python3 python/article_calculator.py allee --n0 100 --r 0.08 --k 1000 --a 75 --t 40
python3 python/article_calculator.py harvesting --n0 100 --r 0.08 --k 1000 --h 12 --t 40
python3 python/article_calculator.py stochastic --n0 100 --r 0.08 --k 1000 --sigma 0.12 --t 40
python3 python/article_calculator.py two-patch --n1 100 --n2 400 --r 0.08 --k 1000 --m 0.04 --t 40
python3 python/article_calculator.py leslie --steps 20
python3 python/article_calculator.py capacity-warning --n 900 --k 1000 --margin 0.15
python3 python/article_calculator.py identifiability-warning --pattern short_series
```
