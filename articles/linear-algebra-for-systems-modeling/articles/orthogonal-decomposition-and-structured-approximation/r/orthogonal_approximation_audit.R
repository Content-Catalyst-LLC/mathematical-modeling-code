A <- matrix(
  c(
    1, 0, 1.0,
    1, 1, 1.5,
    1, 2, 2.1,
    1, 3, 2.9,
    1, 4, 4.2,
    1, 5, 5.1
  ),
  nrow = 6,
  byrow = TRUE
)

b <- c(2.0, 2.9, 3.7, 5.1, 6.2, 6.9)

qr_model <- qr(A)
coefficients <- qr.coef(qr_model, b)
fitted <- as.vector(A %*% coefficients)
residual <- b - fitted
Q <- qr.Q(qr_model)
orthogonality_error <- max(abs(t(Q) %*% residual))
residual_norm <- sqrt(sum(residual^2))
relative_residual_norm <- residual_norm / sqrt(sum(b^2))

audit_record <- data.frame(
  model_name = "synthetic_orthogonal_approximation_audit",
  rows = nrow(A),
  columns = ncol(A),
  numerical_rank = qr_model$rank,
  condition_number = kappa(A),
  residual_norm = residual_norm,
  relative_residual_norm = relative_residual_norm,
  orthogonality_error = orthogonality_error,
  coefficient_norm = sqrt(sum(coefficients^2)),
  method = "qr_least_squares",
  interpretation_warning = paste(
    "Orthogonal approximation results depend on subspace choice, scaling, rank tolerance,",
    "conditioning, solver method, residual interpretation, data provenance, and validation context."
  )
)

coefficient_table <- data.frame(coefficient_index = seq_along(coefficients) - 1, value = as.numeric(coefficients))
fit_residual_table <- data.frame(row_index = seq_along(b) - 1, fitted = fitted, residual = residual)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_orthogonal_approximation_audit.csv", row.names = FALSE)
write.csv(coefficient_table, "outputs/tables/r_coefficients.csv", row.names = FALSE)
write.csv(fit_residual_table, "outputs/tables/r_fit_residual_table.csv", row.names = FALSE)
print(audit_record)
