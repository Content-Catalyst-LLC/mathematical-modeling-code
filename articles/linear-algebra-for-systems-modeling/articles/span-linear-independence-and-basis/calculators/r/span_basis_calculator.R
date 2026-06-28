matrix_values <- matrix(
  c(
    1.0, 0.0, 0.5,
    0.0, 1.0, 0.5,
    0.0, 0.0, 1.0
  ),
  nrow = 3,
  byrow = TRUE
)

ambient_dimension <- nrow(matrix_values)
vector_count <- ncol(matrix_values)
rank_value <- qr(matrix_values)$rank

result <- data.frame(
  calculator = "span_basis_calculator",
  ambient_dimension = ambient_dimension,
  vector_count = vector_count,
  rank = rank_value,
  spans_ambient_space = rank_value == ambient_dimension,
  linearly_independent = rank_value == vector_count,
  is_basis_for_ambient_space = rank_value == ambient_dimension && rank_value == vector_count,
  warning = "Basis claims are relative to the chosen representation."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_span_basis_calculator.csv", row.names = FALSE)
print(result)
