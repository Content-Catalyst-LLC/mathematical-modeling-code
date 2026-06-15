equilibrium <- function(input_rate, loss_rate) {
  input_rate / loss_rate
}

analytical_solution <- function(t, y0, input_rate, loss_rate) {
  eq <- equilibrium(input_rate, loss_rate)
  eq + (y0 - eq) * exp(-loss_rate * t)
}

rate_law <- function(y, input_rate, loss_rate) {
  input_rate - loss_rate * y
}

simulate_linear_input_loss <- function(y0, input_rate, loss_rate, dt, steps) {
  y <- y0
  eq <- equilibrium(input_rate, loss_rate)
  rows <- list()

  for (n in 0:steps) {
    t <- n * dt
    analytical <- analytical_solution(t, y0, input_rate, loss_rate)

    rows[[length(rows) + 1]] <- data.frame(
      scenario = "input_loss_balance",
      time = t,
      analytical_state = analytical,
      euler_state = y,
      absolute_error = abs(analytical - y),
      input_rate = input_rate,
      loss_rate = loss_rate,
      equilibrium = eq,
      initial_state = y0,
      method = "analytical_vs_explicit_euler",
      warning = "Assumes constant input and proportional loss."
    )

    y <- y + dt * rate_law(y, input_rate, loss_rate)
  }

  do.call(rbind, rows)
}

results <- simulate_linear_input_loss(
  y0 = 20,
  input_rate = 12,
  loss_rate = 0.4,
  dt = 0.1,
  steps = 100
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_linear_first_order_audit.csv", row.names = FALSE)
print(head(results))
print(tail(results))
