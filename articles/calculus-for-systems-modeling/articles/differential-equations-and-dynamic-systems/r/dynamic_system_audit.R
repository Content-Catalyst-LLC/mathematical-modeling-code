exponential_rate <- function(x, r) {
  r * x
}

logistic_rate <- function(x, r, capacity) {
  r * x * (1 - x / capacity)
}

simulate_exponential <- function(x0, r, dt, steps) {
  x <- x0
  rows <- list()
  for (n in 0:steps) {
    t <- n * dt
    rate <- exponential_rate(x, r)
    rows[[length(rows) + 1]] <- data.frame(
      scenario = "exponential_growth",
      model_type = "dx_dt_equals_r_x",
      time = t,
      state = x,
      rate = rate,
      growth_rate = r,
      carrying_capacity = NA,
      method = "explicit_euler",
      warning = "Exponential growth assumes no capacity constraint."
    )
    x <- x + dt * rate
  }
  do.call(rbind, rows)
}

simulate_logistic <- function(x0, r, capacity, dt, steps) {
  x <- x0
  rows <- list()
  for (n in 0:steps) {
    t <- n * dt
    rate <- logistic_rate(x, r, capacity)
    rows[[length(rows) + 1]] <- data.frame(
      scenario = "logistic_growth",
      model_type = "dx_dt_equals_r_x_one_minus_x_over_K",
      time = t,
      state = x,
      rate = rate,
      growth_rate = r,
      carrying_capacity = capacity,
      method = "explicit_euler",
      warning = "Logistic growth assumes a fixed carrying capacity."
    )
    x <- x + dt * rate
  }
  do.call(rbind, rows)
}

results <- rbind(
  simulate_exponential(x0 = 10, r = 0.35, dt = 0.1, steps = 100),
  simulate_logistic(x0 = 10, r = 0.35, capacity = 100, dt = 0.1, steps = 100)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_dynamic_system_audit.csv", row.names = FALSE)
print(head(results))
print(tail(results))
