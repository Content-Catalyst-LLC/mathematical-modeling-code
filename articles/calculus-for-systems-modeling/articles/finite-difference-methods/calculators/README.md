# Article Calculators

Reusable calculator layer for **Finite Difference Methods**.

```bash
python3 python/article_calculator.py diffusion-ratio --diffusivity 0.08 --dt 0.2 --dx 1
python3 python/article_calculator.py forward-difference --f-current 1 --f-next 1.2 --dx 0.1
python3 python/article_calculator.py central-difference --f-previous 1 --f-next 1.2 --dx 0.1
python3 python/article_calculator.py second-central-difference --f-previous 1 --f-current 1.2 --f-next 1.4 --dx 0.1
python3 python/article_calculator.py explicit-diffusion-step --left 0 --center 1 --right 0 --ratio 0.016
python3 python/article_calculator.py stability-check --diffusivity 0.08 --dt 0.2 --dx 1
python3 python/article_calculator.py diffusion-simulation --grid-points 61 --diffusivity 0.08 --dx 1 --dt 0.2 --steps 120
bash run_calculator_smoke_tests.sh
```
