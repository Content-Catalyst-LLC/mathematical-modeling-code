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
  y + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
}

simulate_rk4 <- function(y0, decay_rate, h, stop_time) {
  steps <- round(stop_time / h)
  y <- y0
  for (step in 0:(steps - 1)) {
    t <- step * h
    y <- rk4_step(t, y, h, decay_rate)
  }
  y
}

y0 <- 100
decay_rate <- 0.35
stop_time <- 20
exact_final <- exact_solution(stop_time, y0, decay_rate)
step_sizes <- c(1, 0.5, 0.25, 0.125)

records <- data.frame()
for (h in step_sizes) {
  numeric_final <- simulate_rk4(y0, decay_rate, h, stop_time)
  records <- rbind(records, data.frame(
    step_size = h,
    steps = round(stop_time / h),
    solver_method = "fixed_step_rk4",
    final_numeric_value = numeric_final,
    final_exact_value = exact_final,
    final_absolute_error = abs(numeric_final - exact_final),
    warning = "Convergence evidence supports numerical reliability, not empirical validity."
  ))
}

records$error_ratio_to_previous <- c(NA, head(records$final_absolute_error, -1) / tail(records$final_absolute_error, -1))

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(records, "outputs/tables/r_step_size_refinement_audit.csv", row.names = FALSE)
print(records)
