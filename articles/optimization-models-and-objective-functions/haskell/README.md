# Haskell Optimization Model Layer

This Haskell layer represents optimization model categories explicitly.

It helps prevent conceptual flattening:

- a decision variable is not an objective function;
- a constraint is not a parameter;
- solver settings affect interpretation;
- validation diagnostics should not be confused with optimality.
