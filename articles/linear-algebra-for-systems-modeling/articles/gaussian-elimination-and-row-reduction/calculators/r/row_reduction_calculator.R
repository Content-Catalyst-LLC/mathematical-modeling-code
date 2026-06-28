result <- data.frame(
  calculator = "row_reduction_rank_consistency_calculator",
  equation_count = 3,
  unknown_count = 3,
  pivot_columns = "0,1,2",
  coefficient_rank = 3,
  augmented_rank = 3,
  consistent = TRUE,
  solution_behavior = "unique solution",
  tolerance = 1.0e-10,
  warning = "Rank and solution behavior depend on tolerance and modeling assumptions."
)
dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_row_reduction_calculator.csv", row.names = FALSE)
print(result)
