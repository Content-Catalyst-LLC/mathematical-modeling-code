rate_function <- function(t, y, decay_rate) {
  -decay_rate * y
}

exact_solution <- function(t, y0, decay_rate) {
  y0 * exp(-decay_rate * t)
}

euler_audit <- function(y0, decay_rate, step_size, stop_time) {
  steps <- round(stop_time / step_size)
  y <- y0
  multiplier <- 1 - step_size * decay_rate
  stability_status <- ifelse(abs(multiplier) <= 1, "stable_for_simple_decay", "unstable_risk")
  records <- list()

  for (step in 0:steps) {
    t <- step * step_size
    exact <- exact_solution(t, y0, decay_rate)
    records[[length(records) + 1]] <- data.frame(
      step = step,
      time = t,
      euler_value = y,
      exact_value = exact,
      absolute_error = abs(y - exact),
      step_size = step_size,
      stability_multiplier = multiplier,
      stability_status = stability_status,
      warning = "Euler estimates depend on time step, rate function, initial condition, stability, and accumulated error."
    )
    y <- y + step_size * rate_function(t, y, decay_rate)
  }

  do.call(rbind, records)
}

step_sizes <- c(1, 0.5, 0.25, 0.1)
all_results <- do.call(rbind, lapply(step_sizes, function(h) euler_audit(100, 0.35, h, 20)))

summary_table <- aggregate(
  absolute_error ~ step_size,
  data = all_results,
  FUN = function(x) tail(x, 1)
)
names(summary_table)[[2]] <- "final_absolute_error"

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(all_results, "outputs/tables/r_euler_step_size_audit.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_euler_step_size_summary.csv", row.names = FALSE)

print(head(all_results))
print(summary_table)
