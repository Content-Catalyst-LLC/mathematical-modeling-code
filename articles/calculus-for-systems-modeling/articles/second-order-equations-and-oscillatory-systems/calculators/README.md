# Article Calculators

Reusable calculator layer for **Second-Order Equations and Oscillatory Systems**.

## Python examples

```bash
python3 python/article_calculator.py damping-classification --damping-ratio 0.2
python3 python/article_calculator.py period --natural-frequency 1.0
python3 python/article_calculator.py acceleration --position 1 --velocity 0 --time 0 --damping-ratio 0.2 --natural-frequency 1 --forcing-amplitude 0 --forcing-frequency 1
python3 python/article_calculator.py euler-step --position 1 --velocity 0 --dt 0.02 --damping-ratio 0.2 --natural-frequency 1 --forcing-amplitude 0 --forcing-frequency 1
python3 python/article_calculator.py simulate-oscillator --scenario underdamped --position 1 --velocity 0 --damping-ratio 0.2 --natural-frequency 1 --forcing-amplitude 0 --forcing-frequency 1 --dt 0.02 --steps 50
```

## R examples

```bash
Rscript r/article_calculator.R damping-classification 0.2
Rscript r/article_calculator.R period 1
Rscript r/article_calculator.R acceleration 1 0 0 0.2 1 0 1
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
