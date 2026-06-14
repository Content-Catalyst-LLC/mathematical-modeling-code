# Advanced Mathematical Audit: Differentiability and Local Behavior

## Formal topics included

- Derivative as limit
- Differentiability as local linear approximation
- Differentiability implies continuity
- One-sided derivatives
- Partial and directional derivatives
- Fréchet and Gâteaux differentiability
- Jacobian as local linear map
- Nonsmooth behavior and generalized-tool warnings

## Diagnostics included

- Local linearization error
- Forward/backward/central finite differences
- One-sided derivative gap
- Kink detection
- Boundary saturation review
- Invariant interval review

## Flagged kink or boundary records

[{'function_name': 'kink_abs_response', 'x0': 0.0, 'h': 1.0, 'forward': 1.0, 'backward': -1.0, 'central': 0.0, 'one_sided_gap': 2.0, 'kink_flag': True}, {'function_name': 'kink_abs_response', 'x0': 0.0, 'h': 0.5, 'forward': 1.0, 'backward': -1.0, 'central': 0.0, 'one_sided_gap': 2.0, 'kink_flag': True}, {'function_name': 'kink_abs_response', 'x0': 0.0, 'h': 0.25, 'forward': 1.0, 'backward': -1.0, 'central': 0.0, 'one_sided_gap': 2.0, 'kink_flag': True}, {'function_name': 'kink_abs_response', 'x0': 0.0, 'h': 0.125, 'forward': 1.0, 'backward': -1.0, 'central': 0.0, 'one_sided_gap': 2.0, 'kink_flag': True}, {'function_name': 'kink_abs_response', 'x0': 0.0, 'h': 0.0625, 'forward': 1.0, 'backward': -1.0, 'central': 0.0, 'one_sided_gap': 2.0, 'kink_flag': True}, {'function_name': 'saturation_response_boundary', 'x0': 1.0, 'h': 1.0, 'forward': 0.0, 'backward': 1.0, 'central': 0.5, 'one_sided_gap': 1.0, 'kink_flag': True}, {'function_name': 'saturation_response_boundary', 'x0': 1.0, 'h': 0.5, 'forward': 0.0, 'backward': 1.0, 'central': 0.5, 'one_sided_gap': 1.0, 'kink_flag': True}, {'function_name': 'saturation_response_boundary', 'x0': 1.0, 'h': 0.25, 'forward': 0.0, 'backward': 1.0, 'central': 0.5, 'one_sided_gap': 1.0, 'kink_flag': True}, {'function_name': 'saturation_response_boundary', 'x0': 1.0, 'h': 0.125, 'forward': 0.0, 'backward': 1.0, 'central': 0.5, 'one_sided_gap': 1.0, 'kink_flag': True}, {'function_name': 'saturation_response_boundary', 'x0': 1.0, 'h': 0.0625, 'forward': 0.0, 'backward': 1.0, 'central': 0.5, 'one_sided_gap': 1.0, 'kink_flag': True}]

## Invariant failures

[{'value': -0.05, 'lower': 0.0, 'upper': 1.0, 'inside': False, 'issue': 'value outside invariant interval'}, {'value': 1.2, 'lower': 0.0, 'upper': 1.0, 'inside': False, 'issue': 'value outside invariant interval'}]

## Mathematical warnings

- A derivative is a local approximation object, not a global model.
- Continuity does not imply differentiability.
- Existence of partial derivatives does not imply full differentiability.
- Directional derivatives can exist without a Fréchet derivative.
- Numerical derivative estimates depend on step size, noise, and hidden nonsmoothness.

## Modeling implication

Derivative-based claims should specify the domain, operating point, perturbation directions, smoothness assumptions, and numerical diagnostics supporting local approximation.
