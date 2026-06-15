# Mathematical Deepening Notes

## Required distinctions

- derivative operator as a linear operator on differentiable functions;
- sum and scalar rules as linearity;
- product rule as Leibniz rule;
- quotient rule as product rule plus inverse rule;
- chain rule as composition of local linear maps;
- implicit differentiation under regularity assumptions;
- logarithmic differentiation as relative-rate decomposition;
- automatic differentiation as rule propagation through a computational graph;
- formal derivative versus model-valid derivative.

## Pathology checklist

- quotient rule unstable near zero denominators;
- chain rule fails when a link is not differentiable;
- product-rule decomposition is structural but not necessarily causal;
- symbolic differentiation may exceed the model domain;
- implicit differentiation requires nonzero constraint derivative;
- automatic differentiation differentiates code, not necessarily the intended system.
