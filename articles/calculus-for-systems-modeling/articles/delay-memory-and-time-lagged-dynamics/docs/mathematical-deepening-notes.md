# Mathematical Deepening Notes

## Required distinctions

- instantaneous response versus delayed response
- lagged variable versus hidden state
- fixed delay versus distributed delay
- delay length versus model time step
- history function versus single initial condition
- memory kernel versus simple lag
- overshoot versus random fluctuation
- oscillation from delayed feedback versus observed cycles
- fitted lag versus causal delay
- stress-test timing versus forecast timing

## Review checklist

- Define the physical, biological, informational, institutional, or behavioral source of delay.
- Document delay length and units.
- Record history-function assumptions for the pre-simulation interval.
- Define lagged variables and memory kernels.
- Save both current and delayed states in generated audit tables.
- Record time step, interpolation method, solver choice, and delay lookup method.
- Run delay sweeps and feedback-strength sensitivity tests.
- Compare delayed and non-delayed model variants.
- Avoid interpreting a fitted lag as causal without evidence.
