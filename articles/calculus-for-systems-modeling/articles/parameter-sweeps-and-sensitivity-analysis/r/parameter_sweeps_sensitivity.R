logistic_solution <- function(t, x0, growth_rate, carrying_capacity) {
  carrying_capacity / (1 + ((carrying_capacity - x0) / x0) * exp(-growth_rate * t))
}

final_output <- function(growth_rate, carrying_capacity, x0 = 10, stop_time = 20) {
  logistic_solution(stop_time, x0, growth_rate, carrying_capacity)
}

growth_rates <- c(0.18, 0.25, 0.35, 0.45, 0.55)
carrying_capacities <- c(80, 100, 125, 150)

sweep_grid <- expand.grid(
  growth_rate = growth_rates,
  carrying_capacity = carrying_capacities
)

sweep_grid$initial_value <- 10
sweep_grid$stop_time <- 20
sweep_grid$final_value <- mapply(final_output, sweep_grid$growth_rate, sweep_grid$carrying_capacity)
sweep_grid$output_metric <- "final_state_value"
sweep_grid$warning <- "Sweep results depend on tested ranges, baseline assumptions, and model structure."

local_sensitivity <- function(parameter, baseline_r = 0.35, baseline_k = 100) {
  h <- ifelse(parameter == "growth_rate", 0.01, 1)
  baseline <- final_output(baseline_r, baseline_k)

  if (parameter == "growth_rate") {
    forward <- final_output(baseline_r + h, baseline_k)
    backward <- final_output(baseline_r - h, baseline_k)
    baseline_value <- baseline_r
  } else {
    forward <- final_output(baseline_r, baseline_k + h)
    backward <- final_output(baseline_r, baseline_k - h)
    baseline_value <- baseline_k
  }

  sensitivity <- (forward - backward) / (2 * h)
  elasticity <- sensitivity * baseline_value / baseline

  data.frame(
    parameter = parameter,
    baseline_value = baseline_value,
    perturbation = h,
    baseline_output = baseline,
    forward_output = forward,
    backward_output = backward,
    finite_difference_sensitivity = sensitivity,
    elasticity_estimate = elasticity,
    warning = "Local sensitivity depends on baseline and perturbation size."
  )
}

sensitivity_records <- rbind(
  local_sensitivity("growth_rate"),
  local_sensitivity("carrying_capacity")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(sweep_grid, "outputs/tables/r_parameter_sweep_grid.csv", row.names = FALSE)
write.csv(sensitivity_records, "outputs/tables/r_local_sensitivity_audit.csv", row.names = FALSE)

print(sweep_grid)
print(sensitivity_records)
