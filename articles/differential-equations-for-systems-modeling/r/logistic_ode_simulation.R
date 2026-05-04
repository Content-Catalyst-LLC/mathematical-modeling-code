# Differential Equations for Systems Modeling:
# Logistic ODE simulation and sensitivity analysis in R.
# Educational example only.

library(tidyverse)

simulate_logistic_ode <- function(initial_state, growth_rate, capacity, dt, steps) {
  time <- numeric(steps)
  state <- numeric(steps)
  derivative <- numeric(steps)

  state[1] <- initial_state
  time[1] <- 0

  for (i in 2:steps) {
    derivative[i - 1] <- growth_rate * state[i - 1] * (1 - state[i - 1] / capacity)
    state[i] <- state[i - 1] + derivative[i - 1] * dt
    time[i] <- time[i - 1] + dt
  }

  derivative[steps] <- growth_rate * state[steps] * (1 - state[steps] / capacity)

  tibble(
    time = time,
    state = state,
    derivative = derivative,
    growth_rate = growth_rate,
    capacity = capacity,
    dt = dt
  )
}

parameter_grid <- read_csv("../data/ode_parameter_grid.csv", show_col_types = FALSE)

simulation_results <- parameter_grid |>
  mutate(
    simulation = pmap(
      list(initial_state, growth_rate, capacity, dt, steps),
      simulate_logistic_ode
    )
  ) |>
  unnest(simulation)

summary_results <- simulation_results |>
  group_by(model_name, growth_rate, capacity, dt, steps) |>
  summarise(
    final_state = state[time == max(time)],
    maximum_state = max(state),
    maximum_derivative = max(derivative),
    .groups = "drop"
  ) |>
  arrange(desc(final_state))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(simulation_results, "../outputs/r_logistic_ode_simulation.csv")
write_csv(summary_results, "../outputs/r_logistic_ode_sensitivity.csv")

print(summary_results)
