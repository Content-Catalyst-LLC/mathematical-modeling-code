# Article Calculators

Reusable calculator layer for **Visualization of Continuous Models**.

## Python examples

```bash
python3 python/article_calculator.py logistic-point --time 10 --x0 10 --growth-rate 0.35 --carrying-capacity 100
python3 python/article_calculator.py trajectory-series --x0 10 --growth-rate 0.35 --carrying-capacity 100
python3 python/article_calculator.py scenario-comparison
python3 python/article_calculator.py figure-audit-record --visual-type trajectory_plot
python3 python/article_calculator.py visualization-risk-score --axis-risk 2 --uncertainty-risk 3 --smoothing-risk 1 --metadata-risk 2
python3 python/article_calculator.py uncertainty-band-note --band-type scenario_range
```

## R examples

```bash
Rscript r/article_calculator.R logistic-point 10 10 0.35 100
Rscript r/article_calculator.R visualization-risk-score 2 3 1 2
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
