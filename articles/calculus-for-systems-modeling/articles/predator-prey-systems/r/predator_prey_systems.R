simulate_pair <- function(x0, y0, derivative, dt, steps) {
  x <- x0
  y <- y0
  for (i in seq_len(steps)) {
    d <- derivative(x, y)
    x <- max(0, x + dt * d[1])
    y <- max(0, y + dt * d[2])
  }
  c(x = x, y = y)
}

lotka_volterra <- function(alpha, beta, gamma, delta) {
  function(x, y) {
    c(alpha * x - beta * x * y, delta * x * y - gamma * y)
  }
}

logistic_prey <- function(r, k, beta, gamma, delta) {
  function(x, y) {
    c(r * x * (1 - x / k) - beta * x * y, delta * x * y - gamma * y)
  }
}

harvesting_model <- function(alpha, beta, gamma, delta, hx, hy) {
  function(x, y) {
    c(alpha * x - beta * x * y - hx, delta * x * y - gamma * y - hy)
  }
}

x0 <- 40
y0 <- 9
dt <- 0.02
steps <- 4000

classic <- simulate_pair(x0, y0, lotka_volterra(0.6, 0.02, 0.5, 0.01), dt, steps)
limited <- simulate_pair(x0, y0, logistic_prey(0.6, 500, 0.02, 0.5, 0.01), dt, steps)
harvested <- simulate_pair(x0, y0, harvesting_model(0.6, 0.02, 0.5, 0.01, 1.0, 0.05), dt, steps)

scenario_records <- data.frame(
  scenario_name = c("classic_lotka_volterra", "logistic_prey_limit", "harvesting_pressure"),
  model_type = c("lotka_volterra", "logistic_prey", "harvesting"),
  final_prey = c(classic["x"], limited["x"], harvested["x"]),
  final_predator = c(classic["y"], limited["y"], harvested["y"]),
  warning = c("mass-action baseline", "prey capacity included", "management term changes dynamics")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_predator_prey_scenarios.csv", row.names = FALSE)
print(scenario_records)
