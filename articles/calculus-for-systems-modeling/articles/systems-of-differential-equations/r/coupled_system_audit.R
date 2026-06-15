predator_prey_rates <- function(prey, predator, alpha, beta, delta, gamma) {
  prey_rate <- alpha * prey - beta * prey * predator
  predator_rate <- delta * prey * predator - gamma * predator
  c(prey_rate = prey_rate, predator_rate = predator_rate)
}

simulate_predator_prey <- function(prey0, predator0, alpha, beta, delta, gamma, dt, steps) {
  prey <- prey0
  predator <- predator0
  rows <- list()

  for (n in 0:steps) {
    t <- n * dt
    rates <- predator_prey_rates(prey, predator, alpha, beta, delta, gamma)

    rows[[length(rows) + 1]] <- data.frame(
      scenario = "predator_prey_coupled_system",
      time = t,
      prey = prey,
      predator = predator,
      prey_rate = rates[["prey_rate"]],
      predator_rate = rates[["predator_rate"]],
      alpha = alpha,
      beta = beta,
      delta = delta,
      gamma = gamma,
      method = "explicit_euler",
      warning = "Predator-prey terms are illustrative and assume continuous well-mixed interaction."
    )

    prey <- max(0, prey + dt * rates[["prey_rate"]])
    predator <- max(0, predator + dt * rates[["predator_rate"]])
  }

  do.call(rbind, rows)
}

results <- simulate_predator_prey(
  prey0 = 40,
  predator0 = 9,
  alpha = 0.7,
  beta = 0.05,
  delta = 0.02,
  gamma = 0.5,
  dt = 0.01,
  steps = 2000
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_coupled_system_audit.csv", row.names = FALSE)
print(head(results))
print(tail(results))
