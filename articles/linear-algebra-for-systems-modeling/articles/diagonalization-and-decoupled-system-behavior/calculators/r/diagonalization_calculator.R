result <- data.frame(
  calculator = "diagonalization_calculator",
  matrix_entries = "0.796667,0.123333;0.246667,0.673333",
  eigenvector_matrix = "1.000000,1.000000;1.000000,-2.000000",
  diagonal_matrix = "0.920000,0.000000;0.000000,0.550000",
  reconstruction_error_frobenius = 0.0,
  spectral_radius = 0.92,
  dominant_eigenvalue = 0.92,
  stability_classification = "all_modes_decay_discrete_time",
  warning = "Diagonalization decouples representation, not necessarily real-world independence."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_diagonalization_calculator.csv", row.names = FALSE)
print(result)
