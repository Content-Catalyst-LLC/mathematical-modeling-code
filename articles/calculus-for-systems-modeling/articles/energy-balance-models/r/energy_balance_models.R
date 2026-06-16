equilibrium_temperature <- function(forcing, feedback) forcing / feedback
adjustment_time <- function(heat_capacity, feedback) heat_capacity / feedback
one_layer_response <- function(forcing, feedback, heat_capacity, initial_temperature, dt, steps) {
  temperature <- initial_temperature
  for (step in seq_len(steps)) {
    imbalance <- forcing - feedback * temperature
    temperature <- temperature + (imbalance / heat_capacity) * dt
  }
  temperature
}
two_layer_response <- function(forcing, feedback, exchange, c_upper, c_deep, t_upper0, t_deep0, dt, steps) {
  t_upper <- t_upper0
  t_deep <- t_deep0
  for (step in seq_len(steps)) {
    exchange_flux <- exchange * (t_upper - t_deep)
    t_upper <- t_upper + ((forcing - feedback * t_upper - exchange_flux) / c_upper) * dt
    t_deep <- t_deep + (exchange_flux / c_deep) * dt
  }
  c(upper = t_upper, deep = t_deep)
}
years <- 150; dt <- 0.1; steps <- as.integer(years / dt)
baseline <- one_layer_response(3.7, 1.2, 10, 0, dt, steps)
stronger_feedback <- one_layer_response(3.7, 1.8, 10, 0, dt, steps)
larger_capacity <- one_layer_response(3.7, 1.2, 40, 0, dt, steps)
two_layer <- two_layer_response(3.7, 1.2, 0.7, 10, 100, 0, 0, dt, steps)
scenario_records <- data.frame(
  scenario_name = c("baseline_one_layer", "stronger_feedback", "larger_heat_capacity", "two_layer_heat_uptake"),
  model_type = c("one_layer", "one_layer", "one_layer", "two_layer"),
  final_temperature = c(baseline, stronger_feedback, larger_capacity, two_layer["upper"]),
  equilibrium_temperature = c(equilibrium_temperature(3.7, 1.2), equilibrium_temperature(3.7, 1.8), equilibrium_temperature(3.7, 1.2), equilibrium_temperature(3.7, 1.2)),
  adjustment_time = c(adjustment_time(10, 1.2), adjustment_time(10, 1.8), adjustment_time(40, 1.2), adjustment_time(10, 1.2)),
  warning = c("baseline depends on forcing feedback and heat capacity", "feedback strength changes equilibrium response", "larger heat capacity slows transient response", "two-layer structure stores heat in a slower reservoir")
)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_energy_balance_scenario_records.csv", row.names = FALSE)
print(scenario_records)
