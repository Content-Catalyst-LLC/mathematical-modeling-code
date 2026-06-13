# Overfitting Diagnostics

Overfitting occurs when a model learns noise, quirks, or accidental patterns in the fitting data.

## Warning signs

- very low training error;
- much higher validation error;
- many parameters relative to evidence;
- unstable estimates across samples;
- excellent fit with weak mechanism;
- poor stress performance;
- large overfit gap.

## Responsible practice

- separate training, validation, and test evidence;
- compare with simple baselines;
- use regularization or constraints;
- inspect residuals;
- report overfit gaps;
- preserve model-selection alternatives.
