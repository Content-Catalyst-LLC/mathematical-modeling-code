# Article Calculators

Reusable calculator layer for **Forced Systems and External Shock**.

## Python examples

```bash
python3 python/article_calculator.py impulse-shock --time 10 --shock-time 10 --shock-magnitude -30
python3 python/article_calculator.py step-forcing --time 12 --start-time 10 --level 5
python3 python/article_calculator.py periodic-forcing --time 1.57079632679 --amplitude 2 --angular-frequency 1 --phase 0
python3 python/article_calculator.py forced-recovery --initial-state 100 --equilibrium 100 --recovery-rate 0.15 --shock-time 10 --shock-magnitude -30 --dt 0.1 --steps 300
```

## R examples

```bash
Rscript r/article_calculator.R impulse-shock 10 10 -30
Rscript r/article_calculator.R step-forcing 12 10 5
Rscript r/article_calculator.R forced-recovery 100 100 0.15 10 -30 0.1 300
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
