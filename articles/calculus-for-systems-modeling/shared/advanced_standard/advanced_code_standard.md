# Advanced Companion Code Standard

Every future calculus article companion folder should include the basic multi-language scaffold plus an advanced layer.

## Advanced layer goals

The advanced layer should demonstrate mathematical seriousness without making the whole repository inaccessible.

It should include:

- numerical approximation methods;
- convergence analysis;
- error-order estimates;
- roundoff and conditioning review;
- domain/range/feasible-set validation;
- invariant checks;
- typed validated model records;
- generated audit reports;
- tests that check mathematical properties rather than only whether the workflow runs.

## Minimum Python advanced checks

The default Python layer should include:

- `forward_difference`;
- `central_difference`;
- `richardson_extrapolation`;
- `estimate_convergence_order`;
- `check_interval_invariant`;
- `review_roundoff_window`;
- `generate_advanced_report`.

## Minimum tests

The default advanced tests should include:

- central difference is more accurate than forward difference on a smooth function;
- Richardson extrapolation improves the central estimate;
- convergence order is positive and approximately expected;
- invalid step sizes raise errors;
- invariant checks catch boundary violations;
- generated reports exist and contain method, assumptions, and warnings.
