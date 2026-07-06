features <- c("asset_age", "load_index", "inspection_gap", "temperature_stress")

X <- matrix(
  c(
    12.0, 0.72, 18.0, 0.41,
    18.0, 0.81, 24.0, 0.52,
    7.0, 0.55, 12.0, 0.30,
    25.0, 0.93, 30.0, 0.68,
    20.0, 0.88, 28.0, 0.61,
    9.0, 0.60, 14.0, 0.33,
    15.0, 0.76, 20.0, 0.48,
    30.0, 0.98, 35.0, 0.75,
    11.0, 0.66, 16.0, 0.37,
    22.0, 0.90, 29.0, 0.64
  ),
  ncol = length(features),
  byrow = TRUE
)

colnames(X) <- features
y <- c(0.34, 0.48, 0.24, 0.72, 0.63, 0.29, 0.42, 0.82, 0.33, 0.67)

train_indices <- c(1, 2, 3, 4, 5, 6, 7)
test_indices <- c(8, 9, 10)

X_train <- X[train_indices, , drop = FALSE]
X_test <- X[test_indices, , drop = FALSE]
y_train <- y[train_indices]
y_test <- y[test_indices]

train_means <- colMeans(X_train)
train_scales <- apply(X_train, 2, sd)

X_train_scaled <- scale(X_train, center = train_means, scale = train_scales)
X_test_scaled <- scale(X_test, center = train_means, scale = train_scales)

design_train <- cbind(intercept = 1.0, X_train_scaled)
design_test <- cbind(intercept = 1.0, X_test_scaled)

ridge_lambda <- 0.25
penalty <- diag(ncol(design_train))
penalty[1, 1] <- 0.0

beta <- solve(t(design_train) %*% design_train + ridge_lambda * penalty) %*% t(design_train) %*% y_train
predictions <- design_test %*% beta
residuals <- y_test - predictions

feature_weights <- beta[-1, , drop = FALSE]
largest_weight_feature <- rownames(feature_weights)[which.max(abs(feature_weights[, 1]))]

audit_record <- data.frame(
  workflow_name = "machine_learning_linear_structure_audit",
  scenario_name = "synthetic_infrastructure_risk_pipeline",
  observation_count = nrow(X),
  feature_count = ncol(X),
  train_count = length(train_indices),
  test_count = length(test_indices),
  model_family = "ridge_regression_linear_baseline",
  regularization_strength = ridge_lambda,
  test_rmse = sqrt(mean(residuals^2)),
  max_absolute_residual = max(abs(residuals)),
  largest_weight_feature = largest_weight_feature,
  preprocessing_summary = "Training means and scales were fit on training rows only and then applied to test rows.",
  leakage_warning = paste(
    "Scaling, imputation, feature selection, dimensionality reduction, and threshold tuning",
    "must be fit inside the training process."
  ),
  interpretation_warning = paste(
    "Linear pipeline outputs depend on feature definitions, target validity, preprocessing,",
    "train-test separation, regularization, residual structure, subgroup performance, drift monitoring,",
    "and deployment context."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_machine_learning_linear_structure_audit.csv", row.names = FALSE)
print(audit_record)
