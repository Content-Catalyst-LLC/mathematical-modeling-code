logistic_solution <- function(t, x0, r, k) {
  k / (1 + ((k - x0) / x0) * exp(-r * t))
}

times <- seq(0, 20, by = 0.25)

scenarios <- data.frame(
  scenario = c("low_growth", "baseline", "high_growth"),
  growth_rate = c(0.18, 0.35, 0.55),
  carrying_capacity = c(100, 100, 100)
)

records <- do.call(
  rbind,
  lapply(seq_len(nrow(scenarios)), function(i) {
    data.frame(
      scenario = scenarios$scenario[i],
      time = times,
      value = logistic_solution(times, x0 = 10, r = scenarios$growth_rate[i], k = scenarios$carrying_capacity[i]),
      growth_rate = scenarios$growth_rate[i],
      carrying_capacity = scenarios$carrying_capacity[i],
      warning = "Trajectory visualization depends on equation, initial condition, parameters, time horizon, axis scale, and scenario selection."
    )
  })
)

figure_audit <- data.frame(
  figure_id = c("logistic_growth_scenario_trajectories", "phase_portrait_review", "vector_field_review"),
  visual_type = c("trajectory_plot", "phase_portrait", "vector_field"),
  model_object = c("logistic_solution", "two_state_dynamic_system", "spatial_flow_field"),
  x_axis = c("time", "state x", "x coordinate"),
  y_axis = c("state value", "state y", "y coordinate"),
  scale_note = c("Linear axes; time horizon 0 to 20.", "State-space window should be documented.", "Arrow scaling should be documented."),
  uncertainty_note = c("Scenario lines are parameter contrasts, not probability intervals.", "Initial condition selection affects visible trajectories.", "Magnitude and direction can be distorted by normalization."),
  interpretation_warning = c("The figure shows model-implied trajectories under selected assumptions, not empirical forecasts.", "Phase portraits show local and geometric behavior, not automatic empirical validity.", "Vector fields require unit and boundary interpretation.")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

write.csv(records, "outputs/tables/r_continuous_model_trajectories.csv", row.names = FALSE)
write.csv(figure_audit, "outputs/tables/r_visualization_audit_records.csv", row.names = FALSE)

print(head(records))
print(figure_audit)
