# Resource Depletion and Regeneration Calculators

Reusable calculator layer for **Resource Depletion and Regeneration**.

## Python examples

```bash
python3 python/article_calculator.py logistic-regeneration --stock 500 --r 0.18 --k 1000
python3 python/article_calculator.py msy --r 0.18 --k 1000
python3 python/article_calculator.py depletion-condition --regeneration 35 --harvest 45 --loss 5
python3 python/article_calculator.py simulate-renewable --stock0 600 --harvest 35 --steps 800
python3 python/article_calculator.py simulate-nonrenewable --stock0 600 --extraction-rate 30 --steps 800
python3 python/article_calculator.py threshold-risk --stock 150 --threshold 180
python3 python/article_calculator.py efficiency-rebound --demand 60 --efficiency-gain 0.15 --rebound-factor 0.6
python3 python/article_calculator.py governance-warning --context msy
```

## R examples

```bash
Rscript r/article_calculator.R logistic-regeneration 500 0.18 1000
Rscript r/article_calculator.R msy 0.18 1000
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
