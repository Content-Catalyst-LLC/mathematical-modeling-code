result <- data.frame(
  calculator = "compression_noise_and_informational_tradeoffs_calculator",
  model_name = "synthetic_compression_noise_audit",
  rows = 9,
  columns = 6,
  method = "svd_low_rank_compression",
  preprocessing = "centered_and_standardized",
  retained_rank = 2,
  retained_energy_ratio = 0.962,
  discarded_energy_ratio = 0.038,
  compression_ratio = 1.6875,
  relative_reconstruction_error = 0.195,
  maximum_row_residual = 1.43,
  highest_residual_row = 8,
  warning = "Compression metrics depend on original representation, preprocessing, retained rank, noise definition, reconstruction error, residual review, weak-signal analysis, and validation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_compression_noise_and_informational_tradeoffs_calculator.csv", row.names = FALSE)
print(result)
