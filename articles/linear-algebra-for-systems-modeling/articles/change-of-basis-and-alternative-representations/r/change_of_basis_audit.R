P <- matrix(
  c(
    2, 1,
    1, 2
  ),
  nrow = 2,
  byrow = TRUE
)

x <- c(5, 4)

A <- matrix(
  c(
    1.2, 0.3,
    0.4, 0.9
  ),
  nrow = 2,
  byrow = TRUE
)

basis_coordinates <- solve(P, x)
reconstructed <- as.vector(P %*% basis_coordinates)
reconstruction_error <- sqrt(sum((x - reconstructed)^2))
transformed_matrix <- solve(P, A %*% P)
basis_determinant <- det(P)
basis_rank <- qr(P)$rank

condition_warning <- if (abs(basis_determinant) > 1e-8) {
  "basis is valid in this teaching example; serious workflows should compute a numerical condition number"
} else {
  "basis is near singular or unsafe for coordinate interpretation"
}

audit_record <- data.frame(
  system_name = "two_mode_representation_audit",
  basis_shape = paste(dim(P), collapse = "x"),
  basis_rank = basis_rank,
  basis_determinant = basis_determinant,
  basis_condition_warning = condition_warning,
  original_vector = paste(round(x, 6), collapse = ","),
  basis_coordinates = paste(round(basis_coordinates, 6), collapse = ","),
  reconstructed_vector = paste(round(reconstructed, 6), collapse = ","),
  reconstruction_error = reconstruction_error,
  transformed_matrix = paste(apply(round(transformed_matrix, 6), 1, paste, collapse = ","), collapse = ";"),
  invariant_warning = paste(
    "Similarity transformations preserve determinant, trace, rank, and eigenvalues,",
    "but individual entries and interpretability change."
  ),
  interpretation_warning = paste(
    "Changing basis requires basis meaning, units, scaling, conditioning,",
    "and translation back to system terms."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_change_of_basis_audit.csv", row.names = FALSE)
print(audit_record)
