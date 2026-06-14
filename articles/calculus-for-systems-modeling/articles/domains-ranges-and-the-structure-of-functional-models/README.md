# Domains, Ranges, and the Structure of Functional Models

Companion code and reproducible workflows for **“Domains, Ranges, and the Structure of Functional Models”** in the **Calculus for Systems Modeling** series.

This folder demonstrates how domain rules, output ranges, constraints, feasible regions, parameter spaces, state spaces, and validation logic support responsible calculus-based systems modeling.

## Themes

- domains as model boundaries;
- ranges as interpretable output spaces;
- feasible regions and constraints;
- valid parameter and scenario spaces;
- state-space checks for dynamic models;
- computational validation before interpretation;
- typed validated scenarios in Haskell;
- SQL registries for domain rules and scenario review.

## Run smoke checks

```bash
make smoke
```

## Principle

A model output should not be interpreted merely because it was computed. Inputs, outputs, parameters, and trajectories should be checked against the model’s valid domain, meaningful range, and intended use.
