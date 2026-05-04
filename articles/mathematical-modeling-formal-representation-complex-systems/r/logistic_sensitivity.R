# Mathematical Modeling: Logistic Sensitivity Analysis in R
# Educational example only.

library(tidyverse)

simulate_logistic <- function(initial_state, growth_rate, carrying_capacity, time_steps) {
  state <- numeric(time_steps)
  state[1] <- initial_state

  for (t in 2:time_steps) {
    state[t] <- state[t - 1] +
      growth_rate * state[t - 1] * (1 - state[t - 1] / carrying_capacity)
  }

  tibble(
    time = 1:time_steps,
    state = state,
    growth_rate = growth_rate,
    carrying_capacity = carrying_capacity
  )
}

parameter_grid <- read_csv("../data/model_parameter_grid.csv", show_col_types = FALSE)

simulation_results <- parameter_grid |>
  mutate(
    simulation = map2(
      growth_rate,
      carrying_capacity,
      ~ simulate_logistic(
        initial_state = 10,
        growth_rate = .x,
        carrying_capacity = .y,
        time_steps = 80
      )
    )
  ) |>
  unnest(simulation)

summary_results <- simulation_results |>
  group_by(growth_rate, carrying_capacity) |>
  summarise(
    final_state = state[time == max(time)],
    maximum_state = max(state),
    .groups = "drop"
  ) |>
  arrange(desc(final_state))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(simulation_results, "../outputs/r_logistic_sensitivity_results.csv")
write_csv(summary_results, "../outputs/r_logistic_sensitivity_summary.csv")

print(summary_results)
