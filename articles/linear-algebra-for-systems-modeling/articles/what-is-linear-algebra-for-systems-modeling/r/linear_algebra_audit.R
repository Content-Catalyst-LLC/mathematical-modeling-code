matrix_system <- matrix(
  c(
    0.80, 0.15,
    0.20, 0.90
  ),
  nrow = 2,
  byrow = TRUE
)

model_name <- "two_component_transition_model"
matrix_rank <- qr(matrix_system)$rank
matrix_determinant <- det(matrix_system)
matrix_eigenvalues <- eigen(matrix_system)$values
dominant_eigenvalue <- max(Mod(matrix_eigenvalues))

audit_record <- data.frame(
  model_name = model_name,
  rows = nrow(matrix_system),
  columns = ncol(matrix_system),
  rank = matrix_rank,
  determinant = matrix_determinant,
  dominant_eigenvalue = dominant_eigenvalue,
  matrix_meaning = "transition-like matrix connecting two system components across a modeling step",
  interpretation_warning = paste(
    "Matrix interpretation depends on what entries represent,",
    "how variables are scaled, and whether a linear transformation",
    "is appropriate for the modeled system."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_linear_algebra_matrix_audit.csv", row.names = FALSE)
print(audit_record)
