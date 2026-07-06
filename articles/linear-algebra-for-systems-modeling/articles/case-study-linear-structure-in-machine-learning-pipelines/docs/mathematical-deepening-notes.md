# Mathematical Deepening Notes

## Required distinctions

- raw records versus feature matrix
- feature matrix versus design matrix
- target vector versus decision target
- preprocessing parameters versus model parameters
- training-only scaling versus leakage-prone full-data scaling
- baseline model versus final deployment model
- coefficient size versus causal importance
- prediction vector versus decision rule
- residual vector versus decision harm
- validation metric versus deployment validity

## Review checklist

- Document observations, features, target construction, missingness, encodings, scaling, train-test split, and preprocessing parameters.
- Fit scalers, imputers, feature selectors, dimensionality reduction, and thresholds only inside training or validation workflows.
- Preserve baseline model, regularization strength, coefficients, predictions, residuals, validation metrics, subgroup review, and drift monitoring plan.
- Inspect collinearity, conditioning, feature-proxy risks, target validity, calibration, distribution shift, and deployment context.
- Attach documentation, uncertainty, oversight, appeal paths, stop-use conditions, and decision boundaries to outputs.
