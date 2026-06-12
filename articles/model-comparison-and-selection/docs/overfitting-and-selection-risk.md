# Overfitting and Selection Risk

A model with excellent calibration performance may fail on validation evidence.

## Warning signs

- low calibration error and high validation error;
- flexible model with many parameters;
- performance depends on a convenient metric;
- no baseline comparison;
- validation data used repeatedly for tuning;
- model selected after inspecting many alternatives without adjustment.

## Responsible practice

- report calibration and validation error separately;
- preserve overfit-gap diagnostics;
- compare against baselines;
- use cross-validation or holdout testing when appropriate;
- document selection criteria before choosing a winner.
