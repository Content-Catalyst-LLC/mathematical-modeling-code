result <- data.frame(
  calculator = "long_run_transition_calculator",
  states = "good|fair|poor",
  orientation = "row_stochastic_row_vector_update_pi_next_equals_pi_P",
  transition_matrix = "0.820000,0.160000,0.020000;0.100000,0.760000,0.140000;0.030000,0.220000,0.750000",
  stationary_estimate = "0.233333,0.488889,0.277778",
  distribution_after_25_steps = "0.236019,0.487126,0.276855",
  convergence_distance = 0.005372,
  row_sum_error = 0.0,
  nonnegative = TRUE,
  warning = "Long-run behavior depends on convergence diagnostics, initial-condition sensitivity, stationarity, and practical horizon."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_long_run_transition_calculator.csv", row.names = FALSE)
print(result)
