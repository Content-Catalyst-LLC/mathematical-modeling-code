# Article Calculators

Reusable calculator layer for **Model Calibration Using Calculus-Based Methods**.

## Python examples

```bash
python3 python/article_calculator.py residual --observed 17.5 --predicted 17.2
python3 python/article_calculator.py squared-loss --residuals "1.0,-0.5,0.25"
python3 python/article_calculator.py logistic-prediction --time 8 --growth-rate 0.34 --carrying-capacity 105
python3 python/article_calculator.py candidate-loss --growth-rate 0.34 --carrying-capacity 105
python3 python/article_calculator.py grid-search
python3 python/article_calculator.py calibration-warning --pattern validation
```

## R examples

```bash
Rscript r/article_calculator.R residual 17.5 17.2
Rscript r/article_calculator.R candidate-loss 0.34 105
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
