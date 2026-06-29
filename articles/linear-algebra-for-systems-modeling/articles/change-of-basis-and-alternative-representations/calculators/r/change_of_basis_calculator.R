result <- data.frame(
  calculator = "change_of_basis_calculator",
  basis_shape = "2x2",
  basis_rank = 2,
  basis_determinant = 3.0,
  original_vector = "5.000000,4.000000",
  basis_coordinates = "2.000000,1.500000",
  reconstructed_vector = "5.000000,4.000000",
  reconstruction_error = 0.0,
  transformed_matrix = "1.133333,0.033333;0.333333,0.966667",
  warning = "Coordinate changes require basis meaning, units, conditioning, and translation back to system terms."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_change_of_basis_calculator.csv", row.names = FALSE)
print(result)
