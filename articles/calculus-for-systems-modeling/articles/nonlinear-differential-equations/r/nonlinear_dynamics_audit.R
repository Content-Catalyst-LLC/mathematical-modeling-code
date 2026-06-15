logistic_rate <- function(x, growth_rate, carrying_capacity) {
  growth_rate * x * (1 - x / carrying_capacity)
}

bistable_rate <- function(x, threshold) {
  x * (1 - x) * (x - threshold)
}

simulate_scalar <- function(scenario, x0, dt, steps, rate_function,
                            parameter_a, parameter_b, parameter_c, warning) {
  x <- x0
  rows <- list()

  for (n in 0:steps) {
    t <- n * dt
    rate <- rate_function(x)

    rows[[length(rows) + 1]] <- data.frame(
      scenario = scenario,
      time = t,
      state = x,
      rate = rate,
      parameter_a = parameter_a,
      parameter_b = parameter_b,
      parameter_c = parameter_c,
      method = "explicit_euler",
      warning = warning
    )

    x <- x + dt * rate
  }

  do.call(rbind, rows)
}

logistic_results <- simulate_scalar(
  scenario = "logistic_growth",
  x0 = 10,
  dt = 0.05,
  steps = 300,
  rate_function = function(x) logistic_rate(x, growth_rate = 0.6, carrying_capacity = 100),
  parameter_a = 0.6,
  parameter_b = 100,
  parameter_c = 0,
  warning = "Logistic growth assumes a fixed carrying capacity and smooth density limitation."
)

threshold_results <- simulate_scalar(
  scenario = "bistable_threshold",
  x0 = 0.35,
  dt = 0.05,
  steps = 300,
  rate_function = function(x) bistable_rate(x, threshold = 0.4),
  parameter_a = 0.4,
  parameter_b = 0,
  parameter_c = 0,
  warning = "Threshold behavior is illustrative and should not be interpreted without evidence for the threshold."
)

results <- rbind(logistic_results, threshold_results)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_nonlinear_dynamics_audit.csv", row.names = FALSE)

print(head(results))
print(tail(results))
