result <- data.frame(
  calculator = "large_scale_matrix_computation_calculator",
  model_name = "synthetic_large_scale_matrix_computation_audit",
  matrix_dimension = 200,
  nonzero_entries = 958,
  density = 0.02395,
  dense_storage_mb = 0.32,
  sparse_storage_mb_estimate = 0.015328,
  storage_reduction_factor = 20.8768,
  matrix_type = "banded_sparse_like_symmetric_system",
  dominant_eigenvalue_estimate = 1.95,
  matrix_vector_product_norm = 34.2,
  iterative_residual_initial = 14.1,
  iterative_residual_final = 0.08,
  iterations = 80,
  warning = "Large-scale matrix metrics depend on shape, density, storage, solver, residual tolerance, precision, conditioning, approximation, and validation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_large_scale_matrix_computation_calculator.csv", row.names = FALSE)
print(result)
