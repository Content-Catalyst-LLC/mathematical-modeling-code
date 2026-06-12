# Recurrence Validation Guide

## Validation should examine stepwise behavior

A recurrence model should not be validated only by final values. It should be evaluated by trajectory shape, boundary events, threshold crossings, oscillation, fixed points, and response to scenario changes.

## Review questions

- Does the update rule reflect a plausible mechanism?
- Does one step match the actual decision or observation interval?
- Are initial conditions credible?
- Do recurrence outputs remain in valid domains?
- Do parameters or thresholds drive qualitative behavior?
- Are uncertainty and scenario dependence communicated?
