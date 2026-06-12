# Haskell Recurrence Model Layer

This Haskell layer represents recurrence model categories explicitly.

It helps prevent conceptual flattening:

- a state variable is not an update rule;
- an initial condition is not a parameter;
- a boundary rule is part of model logic;
- an output diagnostic can reveal what boundary clipping hides.
