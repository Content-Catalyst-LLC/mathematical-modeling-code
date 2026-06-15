history_function <- function(time, initial_value) {
  initial_value
}

delayed_lookup <- function(states, step, delay_steps, initial_value) {
  delayed_index <- step - delay_steps
  if (delayed_index < 1) {
    return(history_function(0, initial_value))
  }
  states[[delayed_index]]
}

simulate_delayed_adjustment <- function(
  initial_state,
  target,
  adjustment_rate,
  delay,
  dt,
  steps
) {
  delay_steps <- round(delay / dt)
  states <- c(initial_state)
  records <- list()

  for (step in 0:steps) {
    time <- step * dt
    current_state <- states[[length(states)]]
    delayed_state <- delayed_lookup(states, step + 1, delay_steps, initial_state)
    derivative_value <- adjustment_rate * (target - delayed_state)

    records[[length(records) + 1]] <- data.frame(
      step = step,
      time = time,
      current_state = current_state,
      delayed_state = delayed_state,
      derivative_value = derivative_value,
      target = target,
      absolute_gap = abs(current_state - target),
      warning = "Delayed adjustment depends on delay length, history function, time step, and feedback strength."
    )

    next_state <- current_state + dt * derivative_value
    states <- c(states, next_state)
  }

  do.call(rbind, records)
}

results <- simulate_delayed_adjustment(
  initial_state = 80,
  target = 100,
  adjustment_rate = 0.2,
  delay = 5,
  dt = 0.1,
  steps = 300
)

summary_table <- data.frame(
  initial_state = 80,
  target = 100,
  adjustment_rate = 0.2,
  delay = 5,
  dt = 0.1,
  delay_steps = round(5 / 0.1),
  max_gap = max(results$absolute_gap),
  final_gap = tail(results$absolute_gap, 1),
  interpretation = "Delayed adjustment can generate overshoot or oscillation when feedback responds to old information."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_delay_memory_audit.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_delay_memory_summary.csv", row.names = FALSE)

print(head(results))
print(summary_table)
