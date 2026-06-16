rate_function <- function(t, y, decay_rate) {
  -decay_rate * y
}

exact_solution <- function(t, y0, decay_rate) {
  y0 * exp(-decay_rate * t)
}

rk4_step <- function(t, y, h, decay_rate) {
  k1 <- rate_function(t, y, decay_rate)
  k2 <- rate_function(t + h / 2, y + h * k1 / 2, decay_rate)
  k3 <- rate_function(t + h / 2, y + h * k2 / 2, decay_rate)
  k4 <- rate_function(t + h, y + h * k3, decay_rate)
  y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
}

solver_audit <- function(y0, decay_rate, step_size, stop_time) {
  steps <- round(stop_time / step_size)
  y <- y0
  records <- list()

  for (step in 0:steps) {
    t <- step * step_size
    exact <- exact_solution(t, y0, decay_rate)

    records[[length(records) + 1]] <- data.frame(
      step = step,
      time = t,
      solver_value = y,
      exact_value = exact,
      absolute_error = abs(y - exact),
      solver_method = "fixed_step_rk4",
      step_size = step_size,
      warning = "ODE solver outputs depend on equation, initial condition, method, tolerances, step size, stiffness, and diagnostics."
    )

    y <- rk4_step(t, y, step_size, decay_rate)
  }

  do.call(rbind, records)
}

step_sizes <- c(1, 0.5, 0.25, 0.1)
all_results <- do.call(rbind, lapply(step_sizes, function(h) solver_audit(100, 0.35, h, 20)))

summary_table <- aggregate(
  absolute_error ~ step_size,
  data = all_results,
  FUN = function(x) tail(x, 1)
)
names(summary_table)[[2]] <- "final_absolute_error"

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(all_results, "outputs/tables/r_ode_solver_step_size_audit.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_ode_solver_step_size_summary.csv", row.names = FALSE)

print(head(all_results))
print(summary_table)
