forcing_function <- function(t, amplitude = 0, frequency = 1) {
  amplitude * cos(frequency * t)
}

acceleration <- function(position, velocity, time, damping_ratio,
                         natural_frequency, forcing_amplitude, forcing_frequency) {
  force <- forcing_function(time, forcing_amplitude, forcing_frequency)
  damping <- 2 * damping_ratio * natural_frequency * velocity
  restoring <- natural_frequency^2 * position
  force - damping - restoring
}

simulate_oscillator <- function(scenario, x0, v0, damping_ratio,
                                natural_frequency, forcing_amplitude,
                                forcing_frequency, dt, steps) {
  x <- x0
  v <- v0
  rows <- list()

  for (n in 0:steps) {
    t <- n * dt
    a <- acceleration(x, v, t, damping_ratio, natural_frequency, forcing_amplitude, forcing_frequency)

    rows[[length(rows) + 1]] <- data.frame(
      scenario = scenario,
      time = t,
      position = x,
      velocity = v,
      acceleration = a,
      damping_ratio = damping_ratio,
      natural_frequency = natural_frequency,
      forcing = forcing_function(t, forcing_amplitude, forcing_frequency),
      method = "explicit_euler_first_order_system",
      warning = "Explicit Euler is transparent but can distort oscillatory systems if the step size is too large."
    )

    v <- v + dt * a
    x <- x + dt * v
  }

  do.call(rbind, rows)
}

results <- rbind(
  simulate_oscillator("underdamped_unforced", 1, 0, 0.2, 1, 0, 1, 0.02, 500),
  simulate_oscillator("forced_near_resonance", 1, 0, 0.1, 1, 0.2, 1, 0.02, 500)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_second_order_oscillation_audit.csv", row.names = FALSE)
print(head(results))
print(tail(results))
