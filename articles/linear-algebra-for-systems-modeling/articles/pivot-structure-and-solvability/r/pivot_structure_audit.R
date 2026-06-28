A <- matrix(
  c(
    1, 1, 0,
    0, 1, 1,
    1, 0, 1
  ),
  nrow = 3,
  byrow = TRUE
)

b <- c(100, 80, 90)

augmented <- cbind(A, b)

rank_A <- qr(A)$rank
rank_augmented <- qr(augmented)$rank
unknown_count <- ncol(A)

consistent <- rank_A == rank_augmented

solution_behavior <- if (!consistent) {
  "no solution"
} else if (rank_A == unknown_count) {
  "unique solution"
} else {
  "infinitely many solutions"
}

free_variable_count <- unknown_count - rank_A

audit_record <- data.frame(
  system_name = "three_constraint_resource_balance_system",
  equation_count = nrow(A),
  unknown_count = unknown_count,
  coefficient_rank = rank_A,
  augmented_rank = rank_augmented,
  consistent = consistent,
  solution_behavior = solution_behavior,
  free_variable_count = free_variable_count,
  interpretation_warning = paste(
    "Pivot and rank diagnostics reveal algebraic solvability;",
    "practical feasibility depends on model meaning, units, and constraints."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_pivot_structure_audit.csv", row.names = FALSE)
print(audit_record)
