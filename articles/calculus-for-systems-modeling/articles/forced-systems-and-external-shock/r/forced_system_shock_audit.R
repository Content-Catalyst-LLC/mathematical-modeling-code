restoring_rate <- function(x, equilibrium, recovery_rate) {
  -recovery_rate * (x - equilibrium)
}

impulse_shock <- function(time, shock_time, shock_magnitude, tolerance = 1e-12) {
  ifelse(abs(time - shock_time) < tolerance, shock_magnitude, 0)
}

simulate_forced_system <- function(
  initial_state,
  equilibrium,
  recovery_rate,
  shock_time,
  shock_magnitude,
  dt,
  steps
) {
  records <- list()
  baseline <- initial_state
  forced <- initial_state

  for (step in 0:steps) {
    time <- step * dt
    shock_value <- impulse_shock(time, shock_time, shock_magnitude)

    records[[length(records) + 1]] <- data.frame(
      step = step,
      time = time,
      baseline_state = baseline,
      forced_state = forced,
      shock_value = shock_value,
      absolute_deviation = abs(forced - baseline),
      warning = "Shock response depends on forcing form, timing, magnitude, recovery rate, and numerical step size."
    )

    baseline <- baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate)

    if (shock_value != 0) {
      forced <- forced + shock_value
    }

    forced <- forced + dt * restoring_rate(forced, equilibrium, recovery_rate)
  }

  do.call(rbind, records)
}

results <- simulate_forced_system(
  initial_state = 100,
  equilibrium = 100,
  recovery_rate = 0.15,
  shock_time = 10,
  shock_magnitude = -30,
  dt = 0.1,
  steps = 300
)

summary_table <- data.frame(
  max_deviation = max(results$absolute_deviation),
  cumulative_deviation = sum(results$absolute_deviation) * 0.1,
  shock_time = 10,
  shock_magnitude = -30,
  recovery_rate = 0.15,
  interpretation = "The same shock magnitude can produce different recovery paths under different internal dynamics."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_forced_system_shock_audit.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_shock_response_summary.csv", row.names = FALSE)

print(head(results))
print(summary_table)
