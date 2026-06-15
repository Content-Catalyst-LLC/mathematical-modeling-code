# Article Calculators

Reusable calculator layer for **Change of Variables in Multidimensional Systems**.

## Python examples

```bash
python3 python/article_calculator.py polar-jacobian --radius 3
python3 python/article_calculator.py polar-area-element --radius 3 --dr 0.1 --dtheta 0.05
python3 python/article_calculator.py circular-area --radius 3
python3 python/article_calculator.py polar-density-total --density 2 --radius 3
python3 python/article_calculator.py cylindrical-volume --radius 3 --height 4
python3 python/article_calculator.py spherical-volume --radius 3
python3 python/article_calculator.py linear-det --a 2 --b 1 --c 0 --d 3
python3 python/article_calculator.py orientation-check --determinant -2
python3 python/article_calculator.py singularity-check --determinant 0.000001
python3 python/article_calculator.py polar-audit --radius 3 --dr 0.25 --dtheta 0.0654498469
```

## R examples

```bash
Rscript r/article_calculator.R polar-jacobian 3
Rscript r/article_calculator.R circular-area 3
Rscript r/article_calculator.R linear-det 2 1 0 3
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
