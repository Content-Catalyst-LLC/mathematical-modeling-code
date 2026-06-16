# Energy Balance Models Calculators

Reusable calculator layer for **Energy Balance Models**.

## Python examples

```bash
python3 python/article_calculator.py equilibrium-temperature --forcing 3.7 --feedback 1.2
python3 python/article_calculator.py adjustment-time --heat-capacity 10 --feedback 1.2
python3 python/article_calculator.py absorbed-solar --solar-constant 1361 --albedo 0.30
python3 python/article_calculator.py one-layer-step --temperature 0 --forcing 3.7 --feedback 1.2 --heat-capacity 10
python3 python/article_calculator.py surface-partition --net-radiation 500 --sensible 120 --latent 300 --ground 40
python3 python/article_calculator.py building-step --temperature 20 --heat-capacity 1000 --q-heat 300 --q-solar 150 --q-internal 80 --q-loss 420
python3 python/article_calculator.py governance-warning --context boundary
```

## R examples

```bash
Rscript r/article_calculator.R equilibrium-temperature 3.7 1.2
Rscript r/article_calculator.R adjustment-time 10 1.2
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
