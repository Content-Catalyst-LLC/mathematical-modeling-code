signal_function <- function(x) {
  sin(x) + 0.1 * x ^ 2
}

true_derivative <- function(x) {
  cos(x) + 0.2 * x
}

finite_difference_audit <- function(start, stop, step_size) {
  xs <- seq(start, stop, by = step_size)
  values <- signal_function(xs)
  records <- list()

  for (i in seq_along(xs)) {
    forward <- NA
    backward <- NA
    central <- NA
    central_error <- NA

    if (i < length(xs)) {
      forward <- (values[[i + 1]] - values[[i]]) / step_size
    }

    if (i > 1) {
      backward <- (values[[i]] - values[[i - 1]]) / step_size
    }

    if (i > 1 && i < length(xs)) {
      central <- (values[[i + 1]] - values[[i - 1]]) / (2 * step_size)
      central_error <- abs(central - true_derivative(xs[[i]]))
    }

    records[[length(records) + 1]] <- data.frame(
      index = i - 1,
      x = xs[[i]],
      value = values[[i]],
      true_derivative = true_derivative(xs[[i]]),
      forward_difference = forward,
      backward_difference = backward,
      central_difference = central,
      central_absolute_error = central_error,
      step_size = step_size,
      warning = "Numerical derivatives depend on step size, formula choice, boundary handling, smoothness, and noise."
    )
  }

  do.call(rbind, records)
}

results <- finite_difference_audit(
  start = 0,
  stop = 10,
  step_size = 0.1
)

valid_errors <- results$central_absolute_error[!is.na(results$central_absolute_error)]

summary_table <- data.frame(
  start = 0,
  stop = 10,
  step_size = 0.1,
  records = nrow(results),
  mean_central_absolute_error = mean(valid_errors),
  max_central_absolute_error = max(valid_errors),
  interpretation = "Central differences provide a useful derivative estimate for smooth synthetic data, but boundary and noise behavior require separate review."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_numerical_differentiation_audit.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_numerical_differentiation_summary.csv", row.names = FALSE)

print(head(results))
print(summary_table)
