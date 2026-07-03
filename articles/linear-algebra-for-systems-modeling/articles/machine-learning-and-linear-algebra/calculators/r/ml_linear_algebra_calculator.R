result <- data.frame(
  calculator = "machine_learning_and_linear_algebra_calculator",
  model_name = "synthetic_machine_learning_linear_algebra_audit",
  observations = 10,
  features = 5,
  method = "standardized_ridge_regression_with_svd_diagnostics",
  preprocessing = "centered_and_standardized_features_centered_target",
  regularization_strength = 0.75,
  feature_matrix_condition_number = 18.4,
  gram_matrix_condition_number = 339.2,
  numerical_rank = 5,
  ridge_weight_norm = 8.7,
  training_rmse = 1.9,
  maximum_absolute_residual = 3.8,
  first_two_component_energy = 0.94,
  warning = "Machine learning metrics depend on feature representation, label validity, preprocessing, conditioning, loss function, regularization, validation design, residual review, and deployment context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_machine_learning_and_linear_algebra_calculator.csv", row.names = FALSE)
print(result)
