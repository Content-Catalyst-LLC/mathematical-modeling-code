# Machine Learning Linear Structure Audit

- Workflow: machine_learning_linear_structure_audit
- Scenario: synthetic_infrastructure_risk_pipeline
- Observation count: 10
- Feature count: 4
- Train count: 7
- Test count: 3
- Model family: ridge_regression_linear_baseline
- Regularization strength: 0.25
- Test RMSE: 0.015409544078
- Max absolute residual: 0.024430206696
- Largest weight feature: temperature_stress

Training means and scales were fit on training rows only and then applied to test rows.

Scaling, imputation, feature selection, dimensionality reduction, and threshold tuning must be fit inside the training process. Full-data preprocessing can leak evaluation information into the model.

Linear pipeline outputs depend on feature definitions, target validity, preprocessing, train-test separation, regularization, residual structure, subgroup performance, drift monitoring, and deployment context. Coefficients and predictions are not automatic causal explanations or decision rules.
