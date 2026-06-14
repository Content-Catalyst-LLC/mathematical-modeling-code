# Infinity, Infinitesimals, and the Historical Problem of Change

Companion code and reproducible workflows for **“Infinity, Infinitesimals, and the Historical Problem of Change”** in the **Calculus for Systems Modeling** series.

This folder demonstrates difference quotients, small-interval approximations, convergence records, concept registries, and typed approximation steps as a bridge between the history of calculus and systems modeling practice.

## Themes

- infinity and infinite subdivision;
- infinitesimals as intuition for local change;
- difference quotients and limiting behavior;
- convergence as a modeling diagnostic;
- finite computation as approximation of continuous mathematics;
- typed approximation records in Haskell;
- concept registries in SQL;
- reproducible outputs for review.

## Run smoke checks

```bash
make smoke
```

## Run all available targets

```bash
make all
```

## Principle

Continuous mathematics is a representation. Difference quotients, limits, numerical steps, and convergence checks should be documented before local rates or accumulated effects are interpreted.

## Advanced mathematical layer

This folder now includes an `advanced/` layer for mathematician-grade companion work.

Run:

```bash
make -C advanced smoke
```

The advanced layer adds formal mathematical-deepening templates, central-difference and Richardson extrapolation checks, convergence-order estimates, roundoff review, invariant/domain checks, generated Markdown/JSON audit reports, and tests beyond basic smoke checks.
