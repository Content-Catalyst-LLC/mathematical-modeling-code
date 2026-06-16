# Infrastructure Flow and Capacity Dynamics Calculators

Reusable calculator layer for **Infrastructure Flow and Capacity Dynamics**.

## Python examples

```bash
python3 python/article_calculator.py utilization --arrival 95 --capacity 100
python3 python/article_calculator.py delay --utilization 0.95
python3 python/article_calculator.py queue-step --queue 20 --arrival 95 --service 100 --dt 1
python3 python/article_calculator.py bottleneck --capacities 140,120,90,130
python3 python/article_calculator.py buffer --inflow 120 --outflow 100 --capacity 300 --time 24
python3 python/article_calculator.py capacity-decay --initial-capacity 100 --maintenance 1.5 --decay-rate 0.03 --years 20
python3 python/article_calculator.py resilience --delivered 80 --required 100
python3 python/article_calculator.py governance-warning --context nominal_capacity
```

## R examples

```bash
Rscript r/article_calculator.R utilization 95 100
Rscript r/article_calculator.R delay 0.95
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
