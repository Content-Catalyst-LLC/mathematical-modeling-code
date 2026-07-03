result <- data.frame(
  calculator = "simulation_of_high_dimensional_systems_calculator",
  model_name = "synthetic_high_dimensional_simulation_audit",
  state_dimension = 24,
  time_steps = 40,
  ensemble_runs = 250,
  method = "sparse_linear_state_update_with_correlated_monte_carlo_shocks",
  random_seed = 20260629,
  transition_spectral_radius = 0.94,
  transition_density = 0.12,
  final_state_mean_norm = 4.8,
  final_state_mean_total = 24.6,
  final_state_95th_percentile_total = 26.0,
  threshold_exceedance_probability = 0.10,
  first_three_component_energy = 0.78,
  warning = "Simulation metrics depend on state representation, transition rules, uncertainty assumptions, covariance, random seed, ensemble size, dimensionality reduction, validation, and interpretation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_simulation_of_high_dimensional_systems_calculator.csv", row.names = FALSE)
print(result)
