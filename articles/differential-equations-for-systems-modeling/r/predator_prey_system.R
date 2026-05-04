# Differential Equations for Systems Modeling:
# Predator-prey coupled ODE system in R.
# Educational example only.

library(tidyverse)

simulate_predator_prey <- function(alpha, beta, delta, gamma, initial_prey, initial_predator, dt, steps) {
  time <- numeric(steps)
  prey <- numeric(steps)
  predator <- numeric(steps)

  prey[1] <- initial_prey
  predator[1] <- initial_predator
  time[1] <- 0

  for (i in 2:steps) {
    dx <- alpha * prey[i - 1] - beta * prey[i - 1] * predator[i - 1]
    dy <- delta * prey[i - 1] * predator[i - 1] - gamma * predator[i - 1]

    prey[i] <- max(prey[i - 1] + dx * dt, 0)
    predator[i] <- max(predator[i - 1] + dy * dt, 0)
    time[i] <- time[i - 1] + dt
  }

  tibble(
    time = time,
    prey = prey,
    predator = predator
  )
}

params <- read_csv("../data/predator_prey_parameters.csv", show_col_types = FALSE) |>
  select(parameter, value) |>
  deframe()

simulation <- simulate_predator_prey(
  alpha = params[["alpha"]],
  beta = params[["beta"]],
  delta = params[["delta"]],
  gamma = params[["gamma"]],
  initial_prey = params[["initial_prey"]],
  initial_predator = params[["initial_predator"]],
  dt = params[["dt"]],
  steps = params[["steps"]]
)

summary_results <- tibble(
  metric = c("final_prey", "final_predator", "max_prey", "max_predator"),
  value = c(
    last(simulation$prey),
    last(simulation$predator),
    max(simulation$prey),
    max(simulation$predator)
  )
)

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(simulation, "../outputs/r_predator_prey_simulation.csv")
write_csv(summary_results, "../outputs/r_predator_prey_summary.csv")

print(summary_results)
