result <- data.frame(
  calculator = "eigenstructure_calculator",
  matrix_entries = "0.820000,0.120000;0.180000,0.760000",
  trace = 1.58,
  determinant = 0.6016,
  eigenvalue_1 = 0.94,
  eigenvalue_2 = 0.64,
  spectral_radius = 0.94,
  dominant_eigenvalue = 0.94,
  stability_classification = "asymptotically_damped_discrete_time",
  warning = "Eigenvalues describe modes of the specified matrix, not automatic causal mechanisms."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_eigenstructure_calculator.csv", row.names = FALSE)
print(result)
