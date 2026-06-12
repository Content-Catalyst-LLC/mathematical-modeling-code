# Update Order and Boundary Review

Discrete models can change behavior when variables are updated in a different order.

## Review questions

- What does one step represent?
- Which state variables update first?
- Are inputs applied before or after state updates?
- Are boundary events reported before clipping?
- Does rounding occur before or after diagnostics?
- Do thresholds use current state or next state?
- Are trajectories saved, or only final states?

## Boundary-event principle

Do not only clip invalid states back into valid ranges. Report the shortage, overflow, failure, or boundary event that caused clipping.
