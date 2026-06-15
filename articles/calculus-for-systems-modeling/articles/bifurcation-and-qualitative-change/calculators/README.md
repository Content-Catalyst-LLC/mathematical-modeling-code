# Article Calculators

Reusable calculator layer for **Bifurcation and Qualitative Change**.

## Python examples

```bash
python3 python/article_calculator.py saddle-node-equilibria --mu 4
python3 python/article_calculator.py transcritical-equilibria --mu 2
python3 python/article_calculator.py pitchfork-equilibria --mu 4
python3 python/article_calculator.py classify-derivative --derivative-value -2
python3 python/article_calculator.py saddle-node-sweep --mu-min -2 --mu-max 4 --mu-step 0.5
```

## R examples

```bash
Rscript r/article_calculator.R saddle-node-equilibria 4
Rscript r/article_calculator.R transcritical-equilibria 2
Rscript r/article_calculator.R pitchfork-equilibria 4
Rscript r/article_calculator.R classify-derivative -2
```

## Smoke test

```bash
bash run_calculator_smoke_tests.sh
```
