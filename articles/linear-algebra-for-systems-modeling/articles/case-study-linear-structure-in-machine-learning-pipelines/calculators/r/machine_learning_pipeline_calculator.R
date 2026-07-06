result <- data.frame(
  calculator = "case_study_linear_structure_in_machine_learning_pipelines_calculator",
  workflow_name = "machine_learning_linear_structure_audit",
  scenario_name = "synthetic_infrastructure_risk_pipeline",
  observation_count = 10,
  feature_count = 4,
  train_count = 7,
  test_count = 3,
  model_family = "ridge_regression_linear_baseline",
  regularization_strength = 0.25,
  test_rmse = 0.041,
  max_absolute_residual = 0.061,
  largest_weight_feature = "inspection_gap",
  warning = "Machine learning pipeline outputs require feature provenance, target validity, leakage controls, validation, residual review, monitoring, and decision boundaries."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_case_study_linear_structure_ml_pipeline_calculator.csv", row.names = FALSE)
print(result)
