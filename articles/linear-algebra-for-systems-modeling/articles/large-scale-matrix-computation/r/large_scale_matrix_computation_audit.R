matrix_dimension <- 200
coupling <- 0.04

A <- matrix(0, nrow = matrix_dimension, ncol = matrix_dimension)
for (i in seq_len(matrix_dimension)) {
  A[i, i] <- 1.8
  if (i > 1) A[i, i - 1] <- -coupling
  if (i < matrix_dimension) A[i, i + 1] <- -coupling
  if (i + 10 <= matrix_dimension) {
    A[i, i + 10] <- -coupling / 2
    A[i + 10, i] <- -coupling / 2
  }
}

nonzero_entries <- sum(A != 0)
density <- nonzero_entries / length(A)
dense_storage_mb <- length(A) * 8 / 1000000
sparse_storage_mb_estimate <- nonzero_entries * (8 + 4 + 4) / 1000000
storage_reduction_factor <- dense_storage_mb / sparse_storage_mb_estimate

x <- seq(1.0, 2.0, length.out = matrix_dimension)
product_vector <- A %*% x
b <- rep(1, matrix_dimension)
diag_A <- diag(A)
R <- A - diag(diag_A)
estimate <- rep(0, matrix_dimension)
residuals <- numeric(81)

for (iteration in 1:80) {
  residuals[iteration] <- sqrt(sum((b - A %*% estimate)^2))
  estimate <- as.numeric((b - R %*% estimate) / diag_A)
}
residuals[81] <- sqrt(sum((b - A %*% estimate)^2))

dominant_eigenvalue_estimate <- max(eigen(A, only.values = TRUE)$values)

audit_record <- data.frame(
  model_name = "synthetic_large_scale_matrix_computation_audit",
  matrix_dimension = matrix_dimension,
  nonzero_entries = nonzero_entries,
  density = density,
  dense_storage_mb = dense_storage_mb,
  sparse_storage_mb_estimate = sparse_storage_mb_estimate,
  storage_reduction_factor = storage_reduction_factor,
  matrix_type = "banded_sparse_like_symmetric_system",
  dominant_eigenvalue_estimate = dominant_eigenvalue_estimate,
  matrix_vector_product_norm = sqrt(sum(product_vector^2)),
  iterative_residual_initial = residuals[1],
  iterative_residual_final = residuals[length(residuals)],
  iterations = 80,
  convergence_warning = "Iterative solver output depends on matrix structure, scaling, preconditioning, stopping tolerance, residual diagnostics, and precision.",
  interpretation_warning = "Large-scale matrix outputs are computational results under storage, approximation, precision, solver, and model assumptions."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_large_scale_matrix_computation_audit.csv", row.names = FALSE)
write.csv(data.frame(iteration = seq_along(residuals) - 1, residual_norm = residuals), "outputs/tables/r_iterative_residual_history.csv", row.names = FALSE)
write.csv(data.frame(index = seq_len(25) - 1, value = as.numeric(product_vector[1:25])), "outputs/tables/r_matrix_vector_product_sample.csv", row.names = FALSE)
print(audit_record)
