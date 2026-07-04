matrix_dimension <- 250

A <- matrix(0, nrow = matrix_dimension, ncol = matrix_dimension)

for (i in seq_len(matrix_dimension)) {
  A[i, i] <- 1.6
  if (i > 1) A[i, i - 1] <- -0.08
  if (i < matrix_dimension) A[i, i + 1] <- -0.08
  if (i + 7 <= matrix_dimension) {
    A[i, i + 7] <- -0.025
    A[i + 7, i] <- -0.025
  }
  if ((i - 1) %% 25 == 0 && i + 25 <= matrix_dimension) {
    A[i, i + 25] <- -0.05
    A[i + 25, i] <- -0.05
  }
}

nonzero_entries <- sum(A != 0)
density <- nonzero_entries / length(A)
dense_storage_mb <- length(A) * 8 / 1000000
coordinate_storage_mb_estimate <- nonzero_entries * (8 + 4 + 4) / 1000000
storage_reduction_factor <- dense_storage_mb / coordinate_storage_mb_estimate

row_degrees <- rowSums(A != 0) - 1
average_row_degree <- mean(row_degrees)
max_row_degree <- max(row_degrees)
isolated_rows <- sum(row_degrees == 0)

x <- seq(1.0, 2.0, length.out = matrix_dimension)
product_vector <- A %*% x

b <- rep(1, matrix_dimension)
diag_A <- diag(A)
R <- A - diag(diag_A)
estimate <- rep(0, matrix_dimension)
residuals <- numeric(61)

for (iteration in 1:60) {
  residuals[iteration] <- sqrt(sum((b - A %*% estimate)^2))
  estimate <- as.numeric((b - R %*% estimate) / diag_A)
}
residuals[61] <- sqrt(sum((b - A %*% estimate)^2))

audit_record <- data.frame(
  model_name = "synthetic_sparse_matrix_efficiency_audit",
  matrix_dimension = matrix_dimension,
  nonzero_entries = nonzero_entries,
  density = density,
  dense_storage_mb = dense_storage_mb,
  coordinate_storage_mb_estimate = coordinate_storage_mb_estimate,
  storage_reduction_factor = storage_reduction_factor,
  average_row_degree = average_row_degree,
  max_row_degree = max_row_degree,
  isolated_rows = isolated_rows,
  matrix_vector_product_norm = sqrt(sum(product_vector^2)),
  iterative_residual_initial = residuals[1],
  iterative_residual_final = residuals[length(residuals)],
  iterations = 60,
  sparsity_warning = paste(
    "Sparse efficiency depends on whether zero entries represent true absence,",
    "unknown relationships, thresholded weak values, or modeling exclusions."
  ),
  interpretation_warning = paste(
    "Sparse outputs should be interpreted through storage format, sparsity pattern,",
    "solver diagnostics, conditioning, threshold rules, and validation evidence."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_sparse_matrix_efficiency_audit.csv", row.names = FALSE)
write.csv(data.frame(iteration = seq_along(residuals) - 1, residual_norm = residuals),
          "outputs/tables/r_sparse_iterative_residual_history.csv",
          row.names = FALSE)
write.csv(data.frame(index = seq_len(25) - 1, value = as.numeric(product_vector[1:25])),
          "outputs/tables/r_sparse_matrix_vector_product_sample.csv",
          row.names = FALSE)
print(audit_record)
