# Urban Dynamics and Congestion Calculators

Reusable calculator layer for **Urban Dynamics and Congestion**.

## Python examples

```bash
python3 python/article_calculator.py traffic-flow --density 35 --free-flow-speed 60 --jam-density 140
python3 python/article_calculator.py critical-density --jam-density 140
python3 python/article_calculator.py queue-step --queue 0 --arrival-rate 2300 --service-rate 2000 --dt 0.01
python3 python/article_calculator.py bpr-travel-time --free-flow-time 20 --volume 2300 --capacity 2000
python3 python/article_calculator.py accessibility --opportunities 1000,500,250 --travel-times 10,25,45 --theta 0.08
python3 python/article_calculator.py induced-demand-step --volume 2300 --target-volume 2600 --adjustment-rate 0.15 --dt 1
python3 python/article_calculator.py distributional-delay --delays 10,20,35 --weights 1,1.5,2
python3 python/article_calculator.py governance-warning --context equity
```

## R examples

```bash
Rscript r/article_calculator.R traffic-flow 35 60 140
Rscript r/article_calculator.R bpr-travel-time 20 2300 2000
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
