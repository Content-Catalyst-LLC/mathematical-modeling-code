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
symmetric_matrix <- isTRUE(all.equal(matrix_values, t(matrix_values)))

result <- data.frame(
  calculator = "matrix_structure_calculator",
  row_count = row_count,
  column_count = column_count,
  nonzero_entries = nonzero_entries,
  sparsity_ratio = round(1 - nonzero_entries / entry_count, 4),
  symmetric = symmetric_matrix,
  warning = "Matrix structure should be interpreted through row, column, and entry meaning."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_matrix_structure_calculator.csv", row.names = FALSE)
print(result)
