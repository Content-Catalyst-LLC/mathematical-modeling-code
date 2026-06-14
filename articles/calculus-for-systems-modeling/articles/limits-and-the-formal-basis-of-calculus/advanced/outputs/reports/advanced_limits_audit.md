# Advanced Mathematical Audit: Limits and the Formal Basis of Calculus

## Formal topics included

- Epsilon-delta limits
- Sequential characterization
- Metric-space limits
- Pointwise versus uniform convergence
- Noncommuting limits and operations
- Boundary/pathology review

## Numerical methods included

- Forward difference
- Central difference
- Richardson extrapolation
- Convergence-order estimation
- Roundoff and cancellation review
- Invariant interval review

## Median estimated convergence orders

{'central_difference': 2.0000845328362873, 'forward_difference': 1.0090639159649584, 'richardson_central': 4.000984967303182}

## Invariant failures

[{'value': -0.05, 'lower': 0.0, 'upper': 1.0, 'inside': False, 'issue': 'value outside invariant interval'}, {'value': 1.1, 'lower': 0.0, 'upper': 1.0, 'inside': False, 'issue': 'value outside invariant interval'}]

## Mathematical warnings

- A numerical convergence table is not a proof of a mathematical limit.
- A mathematical limit can be formally correct while remaining empirically irrelevant to a model.
- Pointwise convergence is insufficient for many preservation claims.
- Interchanging limits with integrals, derivatives, expectations, or optimization requires explicit justification.
- Boundary behavior should be analyzed separately from interior behavior.

## Modeling implication

A limit statement should specify the domain, codomain, topology or metric, convergence mode, and operation being preserved.
