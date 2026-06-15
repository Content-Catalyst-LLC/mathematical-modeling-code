logistic_derivative <- function(x, growth_rate, carrying_capacity) {
  growth_rate * (1 - 2 * x / carrying_capacity)
}

bistable_rate <- function(x, threshold) {
  x * (1 - x) * (x - threshold)
}

numerical_derivative <- function(rate_function, x, h = 1e-5) {
  (rate_function(x + h) - rate_function(x - h)) / (2 * h)
}

classify_scalar_stability <- function(derivative_value, tolerance = 1e-8) {
  if (derivative_value < -tolerance) {
    "locally_stable"
  } else if (derivative_value > tolerance) {
    "locally_unstable"
  } else {
    "inconclusive_by_linearization"
  }
}

records <- list()

for (eq in c(0, 100)) {
  derivative_value <- logistic_derivative(eq, growth_rate = 0.6, carrying_capacity = 100)
  records[[length(records) + 1]] <- data.frame(
    scenario = "logistic_growth",
    equilibrium = eq,
    derivative_value = derivative_value,
    stability = classify_scalar_stability(derivative_value),
    domain_min = 0,
    domain_max = 100,
    warning = "Logistic stability assumes fixed carrying capacity and smooth density limitation."
  )
}

threshold <- 0.4

for (eq in c(0, threshold, 1)) {
  derivative_value <- numerical_derivative(
    function(x) bistable_rate(x, threshold),
    eq
  )
  records[[length(records) + 1]] <- data.frame(
    scenario = "bistable_threshold",
    equilibrium = eq,
    derivative_value = derivative_value,
    stability = classify_scalar_stability(derivative_value),
    domain_min = 0,
    domain_max = 1,
    warning = "Threshold stability depends on the assumed threshold and domain."
  )
}

results <- do.call(rbind, records)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_equilibrium_stability_audit.csv", row.names = FALSE)
print(results)
