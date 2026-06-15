predator_prey_rates <- function(x, y, alpha, beta, delta, gamma) {
  dxdt <- alpha * x - beta * x * y
  dydt <- delta * x * y - gamma * y
  c(dxdt = dxdt, dydt = dydt)
}

alpha <- 0.7
beta <- 0.05
delta <- 0.02
gamma <- 0.5

grid <- expand.grid(
  x = seq(0, 60, by = 5),
  y = seq(0, 30, by = 3)
)

records <- list()

for (i in seq_len(nrow(grid))) {
  x <- grid$x[[i]]
  y <- grid$y[[i]]
  rates <- predator_prey_rates(x, y, alpha, beta, delta, gamma)
  records[[length(records) + 1]] <- data.frame(
    x = x,
    y = y,
    dxdt = rates[["dxdt"]],
    dydt = rates[["dydt"]],
    x_nullcline_residual = rates[["dxdt"]],
    y_nullcline_residual = rates[["dydt"]],
    speed = sqrt(rates[["dxdt"]]^2 + rates[["dydt"]]^2),
    warning = "Vector-field values depend on parameter values, state ranges, and the assumed interaction structure."
  )
}

results <- do.call(rbind, records)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_phase_portrait_audit.csv", row.names = FALSE)

equilibria <- data.frame(
  equilibrium = c("extinction", "coexistence"),
  x = c(0, gamma / delta),
  y = c(0, alpha / beta)
)

write.csv(equilibria, "outputs/tables/r_phase_portrait_equilibria.csv", row.names = FALSE)

print(head(results))
print(equilibria)
