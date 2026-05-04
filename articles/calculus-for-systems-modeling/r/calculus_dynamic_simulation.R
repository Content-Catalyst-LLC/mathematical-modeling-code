# Calculus for Systems Modeling:
# Simulating continuous change in R.
# Educational example only.

library(tidyverse)

simulate_logistic <- function(initial_state, rate, capacity, dt, steps) {
  state <- numeric(steps)
  time <- numeric(steps)
  derivative <- numeric(steps)

  state[1] <- initial_state
  time[1] <- 0

  for (i in 2:steps) {
    derivative[i - 1] <- rate * state[i - 1] * (1 - state[i - 1] / capacity)
    state[i] <- state[i - 1] + derivative[i - 1] * dt
    time[i] <- time[i - 1] + dt
  }

  derivative[steps] <- rate * state[steps] * (1 - state[steps] / capacity)

  tibble(
    time = time,
    state = state,
    derivative = derivative,
    rate = rate,
    capacity = capacity
  )
}

parameter_grid <- read_csv("../data/calculus_parameter_grid.csv", show_col_types = FALSE)

simulation_results <- parameter_grid |>
  mutate(
    simulation = pmap(
      list(initial_state, rate, capacity, dt, steps),
      simulate_logistic
    )
  ) |>
  unnest(simulation)

summary_results <- simulation_results |>
  group_by(rate, capacity) |>
  summarise(
    final_state = state[time == max(time)],
    maximum_state = max(state),
    maximum_derivative = max(derivative),
    .groups = "drop"
  ) |>
  arrange(desc(final_state))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(simulation_results, "../outputs/r_calculus_dynamic_simulation.csv")
write_csv(summary_results, "../outputs/r_calculus_sensitivity_summary.csv")

print(summary_results)
