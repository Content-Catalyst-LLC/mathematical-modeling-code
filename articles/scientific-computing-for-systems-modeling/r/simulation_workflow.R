# Scientific Computing for Systems Modeling:
# Reproducible simulation workflow in R.
# Educational example only.

library(tidyverse)

simulate_logistic <- function(initial_state, growth_rate, capacity, dt, steps) {
  time <- numeric(steps)
  state <- numeric(steps)

  state[1] <- initial_state
  time[1] <- 0

  for (i in 2:steps) {
    derivative <- growth_rate * state[i - 1] * (1 - state[i - 1] / capacity)
    state[i] <- state[i - 1] + derivative * dt
    time[i] <- time[i - 1] + dt
  }

  tibble(
    time = time,
    state = state,
    growth_rate = growth_rate,
    capacity = capacity,
    dt = dt
  )
}

parameter_grid <- read_csv("../data/simulation_parameter_grid.csv", show_col_types = FALSE)

simulation_results <- parameter_grid |>
  mutate(
    simulation = pmap(
      list(initial_state, growth_rate, capacity, dt, steps),
      simulate_logistic
    )
  ) |>
  unnest(simulation)

summary_results <- simulation_results |>
  group_by(scenario_id, growth_rate, capacity, dt) |>
  summarise(
    final_state = state[time == max(time)],
    maximum_state = max(state),
    mean_state = mean(state),
    .groups = "drop"
  ) |>
  arrange(desc(final_state))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(simulation_results, "../outputs/r_simulation_results.csv")
write_csv(summary_results, "../outputs/r_simulation_summary.csv")

print(summary_results)
