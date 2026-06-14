# What Is Calculus for Systems Modeling?
# Base R sensitivity workflow.

simulate_logistic <- function(initial_state, rate, capacity, dt, steps) {
  time <- numeric(steps + 1)
  state <- numeric(steps + 1)

  state[1] <- initial_state
  time[1] <- 0

  for (i in 2:(steps + 1)) {
    derivative <- rate * state[i - 1] * (1 - state[i - 1] / capacity)
    state[i] <- state[i - 1] + derivative * dt
    time[i] <- time[i - 1] + dt
  }

  data.frame(time = time, state = state, rate = rate, capacity = capacity)
}

rates <- c(0.10, 0.15, 0.20, 0.25)
capacities <- c(80, 100, 120)

rows <- list()
index <- 1

for (rate in rates) {
  for (capacity in capacities) {
    run <- simulate_logistic(10, rate, capacity, 0.1, 300)
    rows[[index]] <- data.frame(
      rate = rate,
      capacity = capacity,
      final_state = tail(run$state, 1),
      maximum_state = max(run$state)
    )
    index <- index + 1
  }
}

summary <- do.call(rbind, rows)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(summary, "outputs/tables/r_sensitivity_summary.csv", row.names = FALSE)
print(summary)
