feature_names <- c(
  "energy_load",
  "network_delay",
  "maintenance_backlog",
  "weather_stress",
  "demand_variability"
)

X_raw <- matrix(
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

colnames(X_raw) <- feature_names
y_raw <- c(42, 40, 51, 58, 61, 47, 55, 50, 68, 45)

X <- scale(X_raw, center = TRUE, scale = TRUE)
y <- y_raw - mean(y_raw)
lambda <- 0.75

objective <- function(X, y, w, lambda) {
  residuals <- X %*% w - y
  mean(residuals^2) + lambda * sum(w^2)
}

gradient <- function(X, y, w, lambda) {
  n <- nrow(X)
  (2 / n) * t(X) %*% (X %*% w - y) + 2 * lambda * w
}

w <- rep(0, ncol(X))
step_size <- 0.05
history <- numeric(501)

for (i in 1:500) {
  history[i] <- objective(X, y, w, lambda)
  w <- w - step_size * as.numeric(gradient(X, y, w, lambda))
}
history[501] <- objective(X, y, w, lambda)

H <- (2 / nrow(X)) * t(X) %*% X + 2 * lambda * diag(ncol(X))
closed_form <- solve((t(X) %*% X) / nrow(X) + lambda * diag(ncol(X)),
                     (t(X) %*% y) / nrow(X))

residuals <- X %*% w - y
grad_final <- gradient(X, y, w, lambda)

audit_record <- data.frame(
  model_name = "synthetic_optimization_gradient_matrix_audit",
  observations = nrow(X),
  features = ncol(X),
  objective = "mean_squared_error_plus_l2_regularization",
  solver = "fixed_step_gradient_descent_compared_with_closed_form_ridge_solution",
  regularization_strength = lambda,
  feature_matrix_condition_number = kappa(X),
  hessian_condition_number = kappa(H),
  gradient_norm_final = sqrt(sum(grad_final^2)),
  objective_initial = history[1],
  objective_final = history[length(history)],
  closed_form_gap_norm = sqrt(sum((w - as.numeric(closed_form))^2)),
  training_rmse = sqrt(mean(residuals^2)),
  convergence_warning = paste(
    "Gradient descent depends on step size, scaling, conditioning,",
    "stopping rules, and objective curvature."
  ),
  interpretation_warning = paste(
    "The optimized vector solves a chosen objective under assumptions,",
    "not automatic causal evidence or a complete system policy."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_optimization_matrix_audit.csv", row.names = FALSE)
write.csv(data.frame(feature = feature_names,
                     gradient_descent_weight = w,
                     closed_form_weight = as.numeric(closed_form)),
          "outputs/tables/r_optimized_weights.csv",
          row.names = FALSE)
write.csv(data.frame(iteration = seq_along(history) - 1,
                     objective_value = history),
          "outputs/tables/r_objective_history.csv",
          row.names = FALSE)
print(audit_record)
