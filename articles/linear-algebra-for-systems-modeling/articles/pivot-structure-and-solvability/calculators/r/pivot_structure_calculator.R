result <- data.frame(
  calculator = "pivot_structure_solvability_calculator",
  equation_count = 3,
  unknown_count = 3,
  pivot_columns = "0,1,2",
  free_columns = "none",
  coefficient_rank = 3,
  augmented_rank = 3,
  consistent = TRUE,
  solution_behavior = "unique solution",
  tolerance = 1.0e-10,
  warning = "Solvability depends on rank comparison; feasibility depends on modeling assumptions."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_pivot_structure_calculator.csv", row.names = FALSE)
print(result)
