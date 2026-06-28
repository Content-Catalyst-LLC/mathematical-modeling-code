coefficient_matrix <- matrix(
  c(
    1.0, 1.0, 0.0, 0.0,
    0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 1.0
  ),
  nrow = 3,
  byrow = TRUE
)

variable_count <- ncol(coefficient_matrix)
equation_count <- nrow(coefficient_matrix)
rank_value <- qr(coefficient_matrix)$rank
nullity_value <- variable_count - rank_value

likely_solution_structure <- ifelse(
  nullity_value == 0,
  "No free variables if the system is consistent; a unique solution may exist.",
  "Positive-dimensional solution space if the system is consistent."
)

audit_record <- data.frame(
  system_name = "four_variable_three_constraint_system",
  variable_count = variable_count,
  equation_count = equation_count,
  rank = rank_value,
  nullity = nullity_value,
  likely_solution_structure = likely_solution_structure,
  modeling_role = "Audit degrees of freedom in a constrained system representation.",
  interpretation_warning = paste(
    "Rank and nullity describe mathematical freedom.",
    "Feasibility and system meaning require separate review."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

write.csv(
  audit_record,
  "outputs/tables/r_solution_space_audit.csv",
  row.names = FALSE
)

print(audit_record)
