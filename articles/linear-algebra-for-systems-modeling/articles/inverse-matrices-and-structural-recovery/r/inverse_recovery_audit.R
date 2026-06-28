A <- matrix(c(1,1,0, 0,1,1, 1,0,1), nrow = 3, byrow = TRUE)
b <- c(100, 80, 90)
tolerance <- 1e-10
det_value <- det(A)
rank_A <- qr(A)$rank
matrix_size <- nrow(A)
nullity_A <- ncol(A) - rank_A
invertible <- abs(det_value) > tolerance && rank_A == matrix_size
if (invertible) {
  recovered_solution <- solve(A, b)
  residual_norm <- sqrt(sum((A %*% recovered_solution - b)^2))
} else {
  recovered_solution <- rep(NA_real_, ncol(A))
  residual_norm <- NA_real_
}
audit_record <- data.frame(
  system_name = "three_constraint_structural_recovery_system",
  matrix_size = matrix_size,
  determinant = det_value,
  invertible = invertible,
  rank = rank_A,
  nullity = nullity_A,
  recovered_solution = paste(round(recovered_solution, 6), collapse = ","),
  residual_norm = residual_norm,
  condition_warning = "Inverse recovery should be paired with conditioning, sensitivity, units, and model review.",
  tolerance = tolerance,
  interpretation_warning = "Algebraic recovery does not guarantee practical recovery; data quality and model meaning remain decisive."
)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_inverse_recovery_audit.csv", row.names = FALSE)
print(audit_record)
