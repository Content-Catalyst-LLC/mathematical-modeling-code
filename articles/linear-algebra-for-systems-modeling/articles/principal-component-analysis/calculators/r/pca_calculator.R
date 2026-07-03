result <- data.frame(
  calculator = "principal_component_analysis_calculator",
  model_name = "synthetic_pca_diagnostic_audit",
  observations = 8,
  variables = 5,
  preprocessing = "centered_and_standardized",
  retained_components = 2,
  explained_variance_ratio = "0.946;0.044;0.007;0.002;0.001",
  cumulative_explained_variance = 0.990,
  relative_reconstruction_error = 0.100,
  largest_loading_variable_pc1 = "transport_delay",
  largest_loading_variable_pc2 = "water_demand",
  warning = "PCA metrics depend on matrix construction, centering, scaling, retained components, explained-variance criteria, residual review, outlier handling, and validation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_principal_component_analysis_calculator.csv", row.names = FALSE)
print(result)
