# Differentiability and Local Behavior

Companion code and reproducible workflows for **“Differentiability and Local Behavior”** in the **Calculus for Systems Modeling** series.

This folder follows the upgraded mathematician-grade standard. It supports formal derivative concepts, local linearization, one-sided derivative comparison, kink/nonsmooth diagnostics, partial and directional derivative interpretation, Jacobian-oriented local maps, Fréchet/Gâteaux differentiability notes, finite-difference stability checks, invariant/boundary checks, and advanced audit reports.

## Themes

- derivative as a limit;
- differentiability as first-order local approximation;
- differentiability versus continuity;
- one-sided derivatives and boundaries;
- partial and directional derivatives;
- gradients and Jacobians;
- Fréchet and Gâteaux differentiability;
- nonsmooth local behavior;
- finite-difference diagnostics;
- local linearization error;
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

A derivative is a local approximation tool. It should not be treated as a global model or as evidence that the real system is smooth everywhere.
