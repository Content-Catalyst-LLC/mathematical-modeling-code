# Error Metrics and Limits

Metrics compress model error. They are useful, but incomplete.

## Metrics

- mean error;
- mean absolute error;
- root mean squared error;
- median absolute error;
- maximum absolute error;
- threshold disagreement count;
- subgroup mean absolute error.

## Limits

- positive and negative errors can cancel;
- average error can hide threshold failure;
- RMSE can be dominated by outliers;
- percentage errors can behave poorly near zero;
- summary metrics can hide subgroup error.

## Principle

A diagnostic report should pair metrics with residual plots, subgroup summaries, threshold review, and use-limit statements.
