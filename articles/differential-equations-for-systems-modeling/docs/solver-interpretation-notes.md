# Solver and Interpretation Notes

## Euler's Method

Euler's method approximates a differential equation by stepping forward using the current rate of change.

It is useful for teaching because it makes the dynamic logic visible, but it can be inaccurate or unstable when:

- the time step is too large
- the system is stiff
- trajectories change rapidly
- nonlinearities are strong
- error accumulation matters

## Better Solver Practice

For real modeling work, compare numerical methods, examine convergence, inspect sensitivity to time step, and document solver settings.

## Dynamic Interpretation

A differential equation model should be interpreted as a proposed mechanism of change, not simply a fitted curve.
