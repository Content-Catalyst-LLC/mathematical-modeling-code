result <- data.frame(
  calculator = "orthogonal_decomposition_structured_approximation_calculator",
  model_name = "synthetic_orthogonal_approximation_audit",
  rows = 6,
  columns = 3,
  numerical_rank = 3,
  condition_number = 58.0,
  residual_norm = 0.346410,
  relative_residual_norm = 0.032100,
  orthogonality_error = 0.0,
  coefficient_norm = 2.513000,
  method = "qr_least_squares",
  warning = "Approximation metrics depend on subspace choice, scaling, rank tolerance, conditioning, solver method, residual interpretation, data provenance, and validation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_orthogonal_decomposition_structured_approximation_calculator.csv", row.names = FALSE)
print(result)
