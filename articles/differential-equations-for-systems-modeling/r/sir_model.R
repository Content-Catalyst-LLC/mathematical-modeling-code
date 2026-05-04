# Differential Equations for Systems Modeling:
# SIR epidemiological model in R.
# Educational example only.

library(tidyverse)

simulate_sir <- function(beta, gamma, initial_susceptible, initial_infected, initial_recovered, dt, steps) {
  time <- numeric(steps)
  susceptible <- numeric(steps)
  infected <- numeric(steps)
  recovered <- numeric(steps)

  susceptible[1] <- initial_susceptible
  infected[1] <- initial_infected
  recovered[1] <- initial_recovered
  time[1] <- 0

  population <- initial_susceptible + initial_infected + initial_recovered

  for (i in 2:steps) {
    d_s <- -beta * susceptible[i - 1] * infected[i - 1] / population
    d_i <- beta * susceptible[i - 1] * infected[i - 1] / population - gamma * infected[i - 1]
    d_r <- gamma * infected[i - 1]

    susceptible[i] <- max(susceptible[i - 1] + d_s * dt, 0)
    infected[i] <- max(infected[i - 1] + d_i * dt, 0)
    recovered[i] <- max(recovered[i - 1] + d_r * dt, 0)
    time[i] <- time[i - 1] + dt
  }

  tibble(
    time = time,
    susceptible = susceptible,
    infected = infected,
    recovered = recovered
  )
}

params <- read_csv("../data/sir_parameters.csv", show_col_types = FALSE) |>
  select(parameter, value) |>
  deframe()

simulation <- simulate_sir(
  beta = params[["beta"]],
  gamma = params[["gamma"]],
  initial_susceptible = params[["initial_susceptible"]],
  initial_infected = params[["initial_infected"]],
  initial_recovered = params[["initial_recovered"]],
  dt = params[["dt"]],
  steps = params[["steps"]]
)

summary_results <- tibble(
  metric = c("peak_infected", "time_of_peak", "final_susceptible", "final_recovered"),
  value = c(
    max(simulation$infected),
    simulation$time[which.max(simulation$infected)],
    last(simulation$susceptible),
    last(simulation$recovered)
  )
)

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(simulation, "../outputs/r_sir_simulation.csv")
write_csv(summary_results, "../outputs/r_sir_summary.csv")

print(summary_results)
