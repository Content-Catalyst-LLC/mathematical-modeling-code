# Haskell State Representation Layer

This Haskell layer represents state variables, inputs, outputs, parameters, derived diagnostics, and latent states explicitly.

It helps prevent conceptual flattening:

- a state variable is not just any variable;
- an output is not necessarily state;
- a latent condition requires observability review;
- a derived diagnostic should not be mistaken for a directly updated state.
