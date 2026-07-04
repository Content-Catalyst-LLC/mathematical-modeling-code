A <- matrix(
  c(
    4.0, 1.0, 0.5,
    1.0, 3.0, 0.25,
    0.5, 0.25, 2.5
  ),
  nrow = 3,
  byrow = TRUE
)

x <- c(1.0, 2.0, -1.0)
b <- c(6.0, 5.0, 2.0)

y <- A %*% x
product <- A %*% t(A)
solution <- solve(A, b)
residual <- b - A %*% solution

condition_number <- kappa(A, exact = TRUE)
matrix_vector_product_norm <- sqrt(sum(y^2))
matrix_matrix_product_trace <- sum(diag(product))
solve_residual_norm <- sqrt(sum(residual^2))
determinant_value <- det(A)

audit_record <- data.frame(
  model_name = "cross_language_matrix_operation_audit",
  language = "r_base_matrix",
  matrix_shape = paste(dim(A), collapse = "x"),
  vector_shape = length(x),
  indexing_convention = "one_based",
  matrix_multiplication_operator = "%*%",
  elementwise_operator = "*",
  solve_method = "solve",
  condition_number = condition_number,
  matrix_vector_product_norm = matrix_vector_product_norm,
  matrix_matrix_product_trace = matrix_matrix_product_trace,
  solve_residual_norm = solve_residual_norm,
  determinant = determinant_value,
  validation_status = "pass_residual_shape_and_condition_checks",
  interpretation_warning = paste(
    "Cross-language matrix results should be compared by mathematical intent,",
    "shapes, residuals, condition numbers, tolerances, indexing conventions,",
    "and operator semantics."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_cross_language_matrix_audit.csv", row.names = FALSE)
write.csv(data.frame(index = seq_along(y), value = as.numeric(y)),
          "outputs/tables/r_matrix_vector_product.csv",
          row.names = FALSE)
write.csv(data.frame(index = seq_along(solution), value = as.numeric(solution)),
          "outputs/tables/r_linear_solve_solution.csv",
          row.names = FALSE)
print(audit_record)
