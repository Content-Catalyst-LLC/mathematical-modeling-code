A <- matrix(
  c(
    1, 1, 0,
    0, 1, 1,
    1, 0, 1
  ),
  nrow = 3,
  byrow = TRUE
)

rank_A <- qr(A)$rank
column_count <- ncol(A)
row_count <- nrow(A)
nullity_A <- column_count - rank_A
maximum_rank <- min(row_count, column_count)
rank_deficient <- rank_A < maximum_rank

audit_record <- data.frame(
  system_name = "three_constraint_resource_balance_matrix",
  row_count = row_count,
  column_count = column_count,
  rank = rank_A,
  nullity = nullity_A,
  rank_deficient = rank_deficient,
  interpretation_warning = paste(
    "Rank and nullity reveal algebraic structure;",
    "model meaning depends on row definitions, column definitions, units, and purpose."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_rank_nullity_audit.csv", row.names = FALSE)
print(audit_record)
