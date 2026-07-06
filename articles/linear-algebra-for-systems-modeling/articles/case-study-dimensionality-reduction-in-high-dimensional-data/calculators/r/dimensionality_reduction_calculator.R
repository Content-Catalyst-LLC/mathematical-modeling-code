result <- data.frame(
  calculator = "case_study_dimensionality_reduction_in_high_dimensional_data_calculator",
  workflow_name = "dimensionality_reduction_audit",
  scenario_name = "synthetic_high_dimensional_sensor_feature_matrix",
  observation_count = 8,
  feature_count = 5,
  retained_components = 2,
  cumulative_explained_variance = 0.991,
  reconstruction_rmse = 0.086,
  dominant_component_feature = "latency",
  warning = "PCA and SVD components are mathematical approximations and require preprocessing, validation, leakage, stability, rare-pattern, and decision-boundary review."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_case_study_dimensionality_reduction_calculator.csv", row.names = FALSE)
print(result)
