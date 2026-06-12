# Haskell Boundary and Scope Layer

This Haskell layer represents boundary type, scale level, and scope status as explicit types.

It helps prevent conceptual flattening:

- a temporal boundary is not a population boundary;
- a supported use is not a prohibited use;
- scale level is distinct from boundary type;
- a model output should not travel beyond its validated scope.
