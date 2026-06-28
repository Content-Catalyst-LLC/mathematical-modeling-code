matrix_values <- matrix(
  c(
    0.0, 2.0, 0.0, 1.0,
    2.0, 0.0, 3.0, 0.0,
    0.0, 3.0, 0.0, 4.0,
    1.0, 0.0, 4.0, 0.0
  ),
  nrow = 4,
  byrow = TRUE
)

row_count <- nrow(matrix_values)
column_count <- ncol(matrix_values)
entry_count <- row_count * column_count
nonzero_entries <- sum(matrix_values != 0)
sparsity_ratio <- 1 - (nonzero_entries / entry_count)
symmetric_matrix <- isTRUE(all.equal(matrix_values, t(matrix_values)))
rank_value <- qr(matrix_values)$rank

audit_record <- data.frame(
  matrix_name = "infrastructure_interdependency_matrix",
  matrix_role = "weighted adjacency matrix",
  row_meaning = "infrastructure subsystem receiving or indexed by relationship",
  column_meaning = "infrastructure subsystem sending or paired by relationship",
  row_count = row_count,
  column_count = column_count,
  nonzero_entries = nonzero_entries,
  sparsity_ratio = round(sparsity_ratio, 4),
  symmetric = symmetric_matrix,
  rank = rank_value,
  interpretation_warning = paste(
    "Symmetry suggests reciprocal relationships in this example,",
    "but real system dependencies may be directional."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_matrix_structure_audit.csv", row.names = FALSE)
print(audit_record)
