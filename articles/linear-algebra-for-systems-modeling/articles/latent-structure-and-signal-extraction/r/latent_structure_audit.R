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

scores <- svd_result$u[, 1:retained_rank, drop = FALSE] %*%
  diag(svd_result$d[1:retained_rank], retained_rank, retained_rank)

reconstructed <- scores %*% t(svd_result$v[, 1:retained_rank, drop = FALSE])
residuals <- scaled_X - reconstructed

retained_signal_ratio <- sum(svd_result$d[1:retained_rank]^2) / sum(svd_result$d^2)
relative_reconstruction_error <- sqrt(sum(residuals^2)) / sqrt(sum(scaled_X^2))
observation_residuals <- sqrt(rowSums(residuals^2))

audit_record <- data.frame(
  model_name = "synthetic_latent_structure_signal_extraction_audit",
  observations = nrow(X),
  variables = ncol(X),
  method = "svd_low_rank_signal_extraction",
  preprocessing = "centered_and_standardized",
  retained_rank = retained_rank,
  retained_signal_ratio = retained_signal_ratio,
  relative_reconstruction_error = relative_reconstruction_error,
  maximum_observation_residual = max(observation_residuals),
  highest_residual_observation = which.max(observation_residuals) - 1,
  signal_definition_warning = paste(
    "The retained low-rank structure is treated as signal only under the chosen method,",
    "preprocessing, retained rank, scaling, and validation assumptions."
  ),
  interpretation_warning = paste(
    "Latent components are inferred mathematical structures, not automatic causes, categories,",
    "mechanisms, or complete system truths."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_latent_structure_audit.csv", row.names = FALSE)
write.csv(scores, "outputs/tables/r_latent_scores.csv")
write.csv(data.frame(observation_index = seq_along(observation_residuals) - 1, residual_norm = observation_residuals),
          "outputs/tables/r_residual_diagnostics.csv", row.names = FALSE)
print(audit_record)
