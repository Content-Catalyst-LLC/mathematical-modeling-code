matrix_values <- matrix(
  c(
    1.0, 1.0, 0.0, 0.0,
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 1.0
  ),
  nrow = 3,
  byrow = TRUE
)

variable_count <- ncol(matrix_values)
equation_count <- nrow(matrix_values)
rank_value <- qr(matrix_values)$rank
nullity_value <- variable_count - rank_value

result <- data.frame(
  calculator = "rank_nullity_calculator",
  variable_count = variable_count,
  equation_count = equation_count,
  rank = rank_value,
  nullity = nullity_value,
  likely_solution_structure = ifelse(nullity_value > 0, "positive_dimensional_if_consistent", "unique_if_consistent"),
  warning = "Rank-nullity describes mathematical freedom, not feasibility or adequacy."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_rank_nullity_calculator.csv", row.names = FALSE)
print(result)
