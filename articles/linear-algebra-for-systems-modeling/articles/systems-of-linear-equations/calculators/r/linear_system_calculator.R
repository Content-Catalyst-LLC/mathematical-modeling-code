result <- data.frame(
  calculator = "linear_system_consistency_calculator",
  equation_count = 3,
  unknown_count = 3,
  coefficient_rank = 3,
  augmented_rank = 3,
  consistent = TRUE,
  solution_behavior = "unique solution",
  warning = "Consistency does not guarantee practical feasibility."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_linear_system_calculator.csv", row.names = FALSE)
print(result)
