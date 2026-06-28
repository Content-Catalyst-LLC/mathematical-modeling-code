matrix_system <- matrix(c(0.80, 0.15, 0.20, 0.90), nrow = 2, byrow = TRUE)
result <- data.frame(
  determinant = det(matrix_system),
  dominant_eigenvalue = max(Mod(eigen(matrix_system)$values)),
  warning = "Calculator outputs require matrix meaning, units, scale, and model context."
)
dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_matrix_calculator_results.csv", row.names = FALSE)
print(result)
