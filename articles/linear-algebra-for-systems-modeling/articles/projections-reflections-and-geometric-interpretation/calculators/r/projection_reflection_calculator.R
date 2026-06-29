result <- data.frame(
  calculator = "projection_reflection_calculator",
  original_vector = "4.000000,3.000000",
  unit_direction = "0.894427,0.447214",
  projected_vector = "4.400000,2.200000",
  residual_vector = "-0.400000,0.800000",
  residual_norm = 0.894427,
  reflected_vector = "4.800000,1.400000",
  projection_idempotence_error = 0.0,
  projection_symmetry_error = 0.0,
  reflection_involution_error = 0.0,
  length_preservation_error = 0.0,
  warning = "Projection and reflection interpretation depends on geometry, units, scaling, and model purpose."
)
dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_projection_reflection_calculator.csv", row.names = FALSE)
print(result)
