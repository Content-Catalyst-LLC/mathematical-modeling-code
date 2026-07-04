A <- matrix(
  c(
    4.0, 1.0, 0.2,
    1.0, 3.0, 0.4,
    0.2, 0.4, 1.2,
    2.0, 1.5, 0.3
  ),
  nrow = 4,
  byrow = TRUE
)

square_block <- A[1:3, 1:3]
b <- c(1.0, 2.0, 0.5)

qr_factor <- qr(A)
svd_factor <- svd(A)
solution_block <- solve(square_block, b)
residual <- b - square_block %*% solution_block

singular_values <- svd_factor$d
tolerance <- 1e-8 * max(singular_values)
estimated_rank <- sum(singular_values > tolerance)
condition_proxy <- max(singular_values) / min(singular_values)
rank_2_error <- sqrt(sum(singular_values[3:length(singular_values)]^2))

audit_record <- data.frame(
  model_name = "decomposition_workflow_audit",
  matrix_shape = paste(dim(A), collapse = "x"),
  matrix_class = "rectangular_overdetermined_dense_demo_matrix",
  recommended_workflow = "QR_or_SVD_for_least_squares_and_rank_diagnostics",
  qr_rank = qr_factor$rank,
  estimated_rank = estimated_rank,
  condition_proxy = condition_proxy,
  singular_value_1 = singular_values[1],
  singular_value_2 = singular_values[2],
  singular_value_3 = singular_values[3],
  low_rank_reconstruction_error = rank_2_error,
  solve_residual_norm = sqrt(sum(residual^2)),
  decomposition_warning = paste(
    "Rectangular systems should generally use QR or SVD rather than normal equations",
    "when stability and rank diagnostics matter."
  ),
  interpretation_warning = paste(
    "Decomposition factors should be interpreted through matrix construction,",
    "scaling, rank tolerance, conditioning, residuals, and system meaning."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_decomposition_workflow_audit.csv", row.names = FALSE)
write.csv(
  data.frame(component = seq_along(singular_values), singular_value = singular_values),
  "outputs/tables/r_singular_value_summary.csv",
  row.names = FALSE
)
print(audit_record)
