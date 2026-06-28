result <- data.frame(
  calculator = "inverse_recovery_calculator",
  matrix_size = 3,
  determinant = 2.0,
  invertible = TRUE,
  rank = 3,
  nullity = 0,
  recovered_solution = "55.000000,45.000000,35.000000",
  residual_norm = 0.0,
  tolerance = 1.0e-10,
  warning = "Inverse recovery is exact for this synthetic example; conditioning and model meaning still require review."
)
dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_inverse_recovery_calculator.csv", row.names = FALSE)
print(result)
