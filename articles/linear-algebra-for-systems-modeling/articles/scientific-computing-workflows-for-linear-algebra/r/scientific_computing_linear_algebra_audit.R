A <- matrix(
  c(
    4.0, 1.0, 0.5,
    1.0, 3.0, 0.25,
    0.5, 0.25, 2.5
  ),
  nrow = 3,
  byrow = TRUE
)

x_probe <- c(1.0, -1.0, 2.0)
b <- c(6.0, 5.0, 2.0)
tolerance <- 1e-10

y <- A %*% x_probe
solution <- solve(A, b)
residual <- b - A %*% solution

residual_norm <- sqrt(sum(residual^2))
relative_residual <- residual_norm / max(sqrt(sum(b^2)), 1e-15)
condition_number <- kappa(A, exact = TRUE)

reproducibility_status <- ifelse(
  relative_residual <= tolerance,
  "pass_residual_tolerance",
  "review_required"
)

audit_record <- data.frame(
  model_name = "scientific_computing_linear_algebra_audit",
  workflow_stage = "matrix_construction_solve_diagnostics_metadata",
  matrix_shape = paste(dim(A), collapse = "x"),
  representation = "dense_base_r_matrix",
  precision = "double_precision_numeric",
  solver_choice = "base_R_solve",
  tolerance = tolerance,
  determinant = det(A),
  condition_number = condition_number,
  matrix_vector_norm = sqrt(sum(y^2)),
  solution_norm = sqrt(sum(solution^2)),
  residual_norm = residual_norm,
  relative_residual = relative_residual,
  reproducibility_status = reproducibility_status,
  r_version = paste(R.version$major, R.version$minor, sep = "."),
  interpretation_warning = paste(
    "Scientific computing outputs should be interpreted with matrix construction,",
    "precision, solver choice, tolerances, residuals, conditioning, environment",
    "metadata, validation checks, and model assumptions."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_scientific_computing_linear_algebra_audit.csv", row.names = FALSE)
print(audit_record)
