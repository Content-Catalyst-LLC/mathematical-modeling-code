logistic_map <- function(x, r) {
  r * x * (1 - x)
}

logistic_derivative <- function(x, r) {
  r * (1 - 2 * x)
}

simulate_pair <- function(x0, perturbation, r, steps) {
  records <- list()
  x_reference <- x0
  x_perturbed <- x0 + perturbation

  for (step in 0:steps) {
    difference <- abs(x_reference - x_perturbed)
    log_difference <- ifelse(difference > 0, log(difference), NA)

    records[[length(records) + 1]] <- data.frame(
      step = step,
      x_reference = x_reference,
      x_perturbed = x_perturbed,
      absolute_difference = difference,
      log_difference = log_difference,
      warning = "Trajectory divergence depends on parameter value, initial uncertainty, numerical precision, and iteration count."
    )

    x_reference <- logistic_map(x_reference, r)
    x_perturbed <- logistic_map(x_perturbed, r)
  }

  do.call(rbind, records)
}

estimate_lyapunov <- function(x0, r, burn_in, sample_steps) {
  x <- x0

  for (i in seq_len(burn_in)) {
    x <- logistic_map(x, r)
  }

  values <- numeric(sample_steps)

  for (i in seq_len(sample_steps)) {
    derivative_value <- abs(logistic_derivative(x, r))
    values[[i]] <- log(derivative_value)
    x <- logistic_map(x, r)
  }

  mean(values)
}

results <- simulate_pair(
  x0 = 0.2,
  perturbation = 1e-8,
  r = 3.9,
  steps = 100
)

lyapunov_estimate <- estimate_lyapunov(
  x0 = 0.2,
  r = 3.9,
  burn_in = 100,
  sample_steps = 1000
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_chaos_sensitivity_audit.csv", row.names = FALSE)

summary_table <- data.frame(
  model = "logistic_map",
  r = 3.9,
  x0 = 0.2,
  burn_in = 100,
  sample_steps = 1000,
  lyapunov_estimate = lyapunov_estimate,
  interpretation = "Positive values suggest sensitive dependence on initial conditions."
)

write.csv(summary_table, "outputs/tables/r_lyapunov_estimate.csv", row.names = FALSE)

print(head(results))
print(summary_table)
