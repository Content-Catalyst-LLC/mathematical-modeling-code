# Advanced Mathematical Audit: Continuity, Discontinuity, and Structural Breaks

## Formal topics included

- Epsilon-delta continuity
- Sequential and metric-space continuity
- Topological continuity
- Subspace continuity
- One-sided continuity
- Uniform continuity
- Lipschitz continuity
- Absolute continuity
- Semicontinuity
- Structural breaks and piecewise models

## Diagnostics included

- Level-jump detection
- Slope-break detection
- Piecewise-model review
- Invariant interval review
- Regularity example registry

## Flagged break candidates

[{'x': 4.75, 'y': 4.375, 'left_slope': 0.5, 'right_slope': 6.5, 'slope_change': 6.0, 'level_jump': 0.125, 'flag': 'possible_slope_break'}, {'x': 5.0, 'y': 6.0, 'left_slope': 6.5, 'right_slope': 1.3999999999999986, 'slope_change': 5.100000000000001, 'level_jump': 1.625, 'flag': 'level_and_slope_break'}]

## Invariant failures

[{'value': -0.1, 'lower': 0.0, 'upper': 1.0, 'inside': False, 'issue': 'value outside invariant interval'}, {'value': 1.2, 'lower': 0.0, 'upper': 1.0, 'inside': False, 'issue': 'value outside invariant interval'}]

## Mathematical warnings

- Continuity is a representational assumption, not a default property of reality.
- Discontinuity can represent real thresholds, but it can also be created by noise or sampling.
- Differentiability implies continuity, but continuity does not imply differentiability.
- Pointwise convergence of continuous functions does not necessarily preserve continuity.
- Structural breaks can occur in level, slope, variance, parameters, governing equations, or mechanism.

## Modeling implication

A model should state its regularity assumptions: continuous, uniformly continuous, Lipschitz, differentiable, smooth, absolutely continuous, semicontinuous, piecewise continuous, or discontinuous.
