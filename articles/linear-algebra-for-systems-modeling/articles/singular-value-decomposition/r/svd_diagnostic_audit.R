A <- matrix(
  c(
    5.0, 4.8, 1.2, 1.1,
    4.9, 4.7, 1.1, 1.0,
    5.2, 5.0, 1.4, 1.2,
    1.0, 1.2, 4.8, 4.6,
    1.1, 1.3, 5.0, 4.7,
    0.9, 1.1, 4.7, 4.5
  ),
  nrow = 6,
  byrow = TRUE
)

rank_tolerance <- 1e-10
retained_rank <- 2
svd_result <- svd(A)
singular_values <- svd_result$d
numerical_rank <- sum(singular_values > rank_tolerance)
condition_number <- max(singular_values) / min(singular_values)

Uk <- svd_result$u[, 1:retained_rank, drop = FALSE]
Sk <- diag(singular_values[1:retained_rank], retained_rank, retained_rank)
Vk_t <- t(svd_result$v[, 1:retained_rank, drop = FALSE])
A_reconstructed <- Uk %*% Sk %*% Vk_t

relative_reconstruction_error <- sqrt(sum((A - A_reconstructed)^2)) / sqrt(sum(A^2))
explained_energy_retained <- sum(singular_values[1:retained_rank]^2) / sum(singular_values^2)

audit_record <- data.frame(
  model_name = "synthetic_svd_diagnostic_audit",
  rows = nrow(A),
  columns = ncol(A),
  singular_values = paste(signif(singular_values, 12), collapse = ";"),
  numerical_rank = numerical_rank,
  rank_tolerance = rank_tolerance,
  condition_number = condition_number,
  retained_rank = retained_rank,
  explained_energy_retained = explained_energy_retained,
  relative_reconstruction_error = relative_reconstruction_error,
  pseudoinverse_warning = paste(
    "Small singular values can amplify noise when inverted; use rank tolerance,",
    "truncated SVD, or regularization when conditioning is poor."
  ),
  interpretation_warning = paste(
    "SVD components depend on matrix construction, preprocessing, scaling, centering,",
    "rank tolerance, retained-rank choice, numerical method, and domain interpretation."
  )
)

singular_value_table <- data.frame(
  index = seq_along(singular_values),
  singular_value = singular_values
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_svd_diagnostic_audit.csv", row.names = FALSE)
write.csv(singular_value_table, "outputs/tables/r_singular_values.csv", row.names = FALSE)
print(audit_record)
