result <- data.frame(
  calculator = "orthogonality_calculator",
  vector_a = "3.000000,1.000000,2.000000",
  vector_b = "1.000000,-1.000000,-1.000000",
  dot_product = 0.0,
  orthogonal_under_tolerance = TRUE,
  unit_a = "0.801784,0.267261,0.534522",
  unit_b = "0.577350,-0.577350,-0.577350",
  projection_of_a_onto_b = "0.000000,0.000000,0.000000",
  residual_vector = "3.000000,1.000000,2.000000",
  residual_norm = 3.741657,
  orthonormality_error = 0.0,
  warning = "Orthogonality depends on geometry, scaling, units, tolerance, and domain interpretation."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_orthogonality_calculator.csv", row.names = FALSE)
print(result)
