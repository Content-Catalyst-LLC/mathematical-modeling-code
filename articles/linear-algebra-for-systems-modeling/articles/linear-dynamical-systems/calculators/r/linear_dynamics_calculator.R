result <- data.frame(
  calculator = "linear_dynamics_calculator",
  state_names = "infrastructure_stress|service_delay",
  update_matrix = "0.820000,0.120000;0.180000,0.760000",
  initial_state = "10.000000,4.000000",
  horizon = 20,
  final_state = "3.626170,3.452104",
  spectral_radius = 0.94,
  stability_classification = "asymptotically_stable_discrete_time",
  warning = "Linear dynamics depend on state definitions, units, scaling, time step, matrix validity, and whether linearity is structural or approximate."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_linear_dynamics_calculator.csv", row.names = FALSE)
print(result)
