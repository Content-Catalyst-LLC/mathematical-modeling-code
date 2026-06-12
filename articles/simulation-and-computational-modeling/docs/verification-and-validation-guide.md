# Verification and Validation Guide

## Verification asks

- Does the code implement the intended model?
- Do equations match functions?
- Are units consistent?
- Are time steps and update order correct?
- Are boundary conditions implemented properly?
- Do known-case tests pass?
- Are invalid states caught?

## Validation asks

- Is the model credible for the intended purpose?
- Does it reproduce relevant observed patterns?
- Are scenarios meaningful?
- Are parameter values justified?
- Are uncertainty and sensitivity communicated?
- Are outputs appropriate for the decision context?

## Principle

A model can run successfully and still be wrong. Running code is not evidence that the model is valid.
