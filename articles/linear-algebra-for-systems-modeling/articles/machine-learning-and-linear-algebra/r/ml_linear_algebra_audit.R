feature_names <- c(
  "energy_load",
  "network_delay",
  "maintenance_backlog",
  "weather_stress",
  "demand_variability"
)

X <- matrix(
  c(
    82, 12, 4, 31, 7.2,
    79, 11, 5, 29, 6.8,
    91, 18, 7, 37, 8.1,
    63, 24, 12, 42, 9.5,
    58, 28, 14, 45, 10.1,
    76, 16, 8, 34, 7.9,
    88, 21, 11, 39, 8.8,
    69, 19, 10, 36, 8.4,
    95, 30, 15, 48, 10.9,
    72, 14, 6, 33, 7.5
  ),
  nrow = 10,
  byrow = TRUE
)

colnames(X) <- feature_names
y <- c(42, 40, 51, 58, 61, 47, 55, 50, 68, 45)

lambda <- 0.75
Xs <- scale(X, center = TRUE, scale = TRUE)
yc <- y - mean(y)

gram <- t(Xs) %*% Xs
weights <- solve(gram + lambda * diag(ncol(Xs)), t(Xs) %*% yc)
predictions <- Xs %*% weights + mean(y)
residuals <- y - predictions

svd_result <- svd(Xs)
energy_share <- svd_result$d^2 / sum(svd_result$d^2)

audit_record <- data.frame(
  model_name = "synthetic_machine_learning_linear_algebra_audit",
  observations = nrow(X),
  features = ncol(X),
  method = "standardized_ridge_regression_with_svd_diagnostics",
  preprocessing = "centered_and_standardized_features_centered_target",
  regularization_strength = lambda,
  feature_matrix_condition_number = kappa(Xs),
  gram_matrix_condition_number = kappa(gram),
  numerical_rank = qr(Xs)$rank,
  ridge_weight_norm = sqrt(sum(weights^2)),
  training_rmse = sqrt(mean(residuals^2)),
  maximum_absolute_residual = max(abs(residuals)),
  first_two_component_energy = sum(energy_share[1:2]),
  validation_warning = paste(
    "Training error is not generalization evidence. Use validation data,",
    "time splits, cross-validation, residual review, and distribution-shift checks."
  ),
  interpretation_warning = paste(
    "Weights, components, embeddings, and model scores are learned artifacts,",
    "not automatic causes or truths."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_ml_linear_algebra_audit.csv", row.names = FALSE)
write.csv(data.frame(feature = feature_names, weight = as.numeric(weights)),
          "outputs/tables/r_ridge_weights.csv",
          row.names = FALSE)
write.csv(data.frame(observation = seq_along(residuals) - 1, residual = as.numeric(residuals)),
          "outputs/tables/r_residual_diagnostics.csv",
          row.names = FALSE)
write.csv(data.frame(component = seq_along(svd_result$d),
                     singular_value = svd_result$d,
                     energy_share = energy_share),
          "outputs/tables/r_singular_value_diagnostics.csv",
          row.names = FALSE)
print(audit_record)
