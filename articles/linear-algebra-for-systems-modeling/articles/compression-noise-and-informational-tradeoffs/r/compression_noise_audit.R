X <- matrix(
  c(
    82, 71, 18, 22, 41, 3.2,
    79, 69, 17, 20, 39, 3.0,
    85, 73, 20, 25, 43, 3.5,
    48, 52, 35, 40, 62, 6.1,
    51, 54, 38, 42, 64, 6.4,
    46, 50, 34, 39, 60, 5.9,
    68, 61, 27, 31, 52, 4.8,
    70, 63, 29, 33, 54, 5.0,
    90, 78, 42, 47, 71, 7.8
  ),
  nrow = 9,
  byrow = TRUE
)

retained_rank <- 2
scaled_X <- scale(X, center = TRUE, scale = TRUE)
svd_result <- svd(scaled_X)

U_k <- svd_result$u[, 1:retained_rank, drop = FALSE]
S_k <- diag(svd_result$d[1:retained_rank], retained_rank, retained_rank)
V_k_t <- t(svd_result$v[, 1:retained_rank, drop = FALSE])

reconstructed <- U_k %*% S_k %*% V_k_t
residuals <- scaled_X - reconstructed

retained_energy_ratio <- sum(svd_result$d[1:retained_rank]^2) / sum(svd_result$d^2)
discarded_energy_ratio <- 1 - retained_energy_ratio
relative_reconstruction_error <- sqrt(sum(residuals^2)) / sqrt(sum(scaled_X^2))
row_residuals <- sqrt(rowSums(residuals^2))
original_storage <- nrow(scaled_X) * ncol(scaled_X)
compressed_storage <- retained_rank * (nrow(scaled_X) + ncol(scaled_X) + 1)
compression_ratio <- original_storage / compressed_storage

audit_record <- data.frame(
  model_name = "synthetic_compression_noise_audit",
  rows = nrow(X),
  columns = ncol(X),
  method = "svd_low_rank_compression",
  preprocessing = "centered_and_standardized",
  retained_rank = retained_rank,
  retained_energy_ratio = retained_energy_ratio,
  discarded_energy_ratio = discarded_energy_ratio,
  compression_ratio = compression_ratio,
  relative_reconstruction_error = relative_reconstruction_error,
  maximum_row_residual = max(row_residuals),
  highest_residual_row = which.max(row_residuals) - 1,
  noise_warning = paste(
    "Discarded components are not automatically noise. They may contain weak signals,",
    "localized structure, subgroup patterns, anomalies, or early warning behavior."
  ),
  interpretation_warning = "Compression preserves selected structure while losing or distorting other information."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_compression_noise_audit.csv", row.names = FALSE)
write.csv(data.frame(index = seq_along(svd_result$d), singular_value = svd_result$d, energy_share = svd_result$d^2 / sum(svd_result$d^2)),
          "outputs/tables/r_singular_value_energy.csv", row.names = FALSE)
write.csv(data.frame(row_index = seq_along(row_residuals) - 1, residual_norm = row_residuals),
          "outputs/tables/r_row_residuals.csv", row.names = FALSE)
print(audit_record)
