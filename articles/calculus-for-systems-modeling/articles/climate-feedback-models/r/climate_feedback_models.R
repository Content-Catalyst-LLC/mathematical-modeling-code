co2_forcing <- function(concentration, baseline = 280) {
  5.35 * log(concentration / baseline)
}

one_box_temperature <- function(forcing, feedback, heat_capacity, time, initial = 0) {
  equilibrium <- forcing / feedback
  equilibrium + (initial - equilibrium) * exp(-(feedback / heat_capacity) * time)
}

forcing <- 3.7
heat_capacity <- 8.0
times <- seq(0, 100, by = 5)

scenario_records <- data.frame(
  time = times,
  weak_feedback = one_box_temperature(forcing, 0.9, heat_capacity, times),
  baseline_feedback = one_box_temperature(forcing, 1.2, heat_capacity, times),
  strong_feedback = one_box_temperature(forcing, 1.6, heat_capacity, times)
)

parameter_records <- data.frame(
  parameter_name = c("F", "lambda_low", "lambda_baseline", "lambda_high", "C"),
  value = c(forcing, 0.9, 1.2, 1.6, heat_capacity),
  unit = c("W m^-2", "W m^-2 K^-1", "W m^-2 K^-1", "W m^-2 K^-1", "W yr m^-2 K^-1"),
  warning = c(
    "Forcing depends on the forcing agent and scenario.",
    "Weak restoring feedback produces larger response.",
    "Sign convention must be documented.",
    "Strong restoring feedback produces smaller response.",
    "Heat capacity controls time scale."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_climate_feedback_scenarios.csv", row.names = FALSE)
write.csv(parameter_records, "outputs/tables/r_climate_feedback_parameter_records.csv", row.names = FALSE)

print(head(scenario_records))
print(parameter_records)
