# Continuity, Discontinuity, and Structural Breaks

Companion code and reproducible workflows for **“Continuity, Discontinuity, and Structural Breaks”** in the **Calculus for Systems Modeling** series.

This folder follows the upgraded mathematician-grade standard. It supports formal continuity concepts, discontinuity classification, piecewise model diagnostics, structural-break detection, one-sided behavior, uniform and Lipschitz continuity notes, finite-difference slope checks, invariant/boundary checks, and advanced audit reports.

## Themes

- epsilon-delta continuity;
- sequential and metric-space continuity;
- one-sided continuity and boundary behavior;
- removable, jump, infinite, and essential discontinuities;
- structural breaks as modeling events;
- piecewise models and regime changes;
- uniform, Lipschitz, absolute, and semicontinuity;
- finite-difference slope diagnostics;
- invariant checks and break flags;
- generated Markdown/JSON audit reports.

## Run smoke checks

```bash
make smoke
```

## Run advanced checks

```bash
make advanced
```

## Run all available targets

```bash
make all
```

## Principle

Continuity is not a default fact about a system. It is a representational assumption. Discontinuities and structural breaks may signal that the governing relationship has changed.
