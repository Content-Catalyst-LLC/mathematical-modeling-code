result <- data.frame(
  calculator = "stability_analysis_calculator",
  matrix_entries = "0.820000,0.120000;0.180000,0.760000",
  eigenvalue_1 = 0.94,
  eigenvalue_2 = 0.64,
  spectral_radius = 0.94,
  largest_real_part = 0.94,
  discrete_time_classification = "asymptotically_stable_discrete_time",
  continuous_time_classification = "unstable_continuous_time",
  warning = "Discrete-time stability uses eigenvalue magnitudes relative to one; continuous-time stability uses real parts relative to zero."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_stability_analysis_calculator.csv", row.names = FALSE)
print(result)
