# Haskell Simulation Model Layer

This Haskell layer represents simulation model categories explicitly.

It helps prevent conceptual flattening:

- a state variable is not an update rule;
- a numerical method is not a validation diagnostic;
- a stochastic protocol is not an output claim;
- code should remain connected to the mathematical specification.
