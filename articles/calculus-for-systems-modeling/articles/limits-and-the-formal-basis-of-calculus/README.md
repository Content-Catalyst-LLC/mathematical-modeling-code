# Limits and the Formal Basis of Calculus

Companion code and reproducible workflows for **“Limits and the Formal Basis of Calculus”** in the **Calculus for Systems Modeling** series.

This folder follows the upgraded mathematician-grade standard. It supports epsilon-delta reasoning, sequential/topological limit interpretation, one-sided and infinite limits, continuity, derivatives and integrals as limits, pointwise and uniform convergence, counterexamples, numerical convergence, and advanced audit reports.

## Themes

- epsilon-delta limits;
- sequential and topological formulations;
- one-sided and infinite limits;
- continuity as limit preservation;
- derivative and integral definitions;
- pointwise versus uniform convergence;
- noncommuting limits;
- numerical convergence-order studies;
- central differences and Richardson extrapolation;
- roundoff and cancellation review;
- invariant/domain-preservation checks.

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

A mathematical limit is a formal claim about convergence under specified assumptions. A numerical approximation is finite evidence toward that claim, not the claim itself.
