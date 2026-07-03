result <- data.frame(
  calculator = "singular_value_decomposition_calculator",
  model_name = "synthetic_svd_diagnostic_audit",
  rows = 6,
  columns = 4,
  singular_values = "14.35;8.16;0.19;0.04",
  numerical_rank = 4,
  rank_tolerance = 1e-10,
  condition_number = 358.75,
  retained_rank = 2,
  explained_energy_retained = 0.9992,
  relative_reconstruction_error = 0.0283,
  warning = "SVD metrics depend on matrix construction, preprocessing, scaling, centering, rank tolerance, retained rank, pseudoinverse thresholds, and validation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_singular_value_decomposition_calculator.csv", row.names = FALSE)
print(result)
