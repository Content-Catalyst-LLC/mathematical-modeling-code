# Functions, Variables, and Mathematical Representation
# Base R functional-form comparison.

linear_model <- function(x, a = 10, b = 2) {
  a + b * x
}

exponential_model <- function(x, a = 10, b = 0.18) {
  a * exp(b * x)
}

logistic_model <- function(x, capacity = 100, rate = 0.75, midpoint = 5) {
  capacity / (1 + exp(-rate * (x - midpoint)))
}

threshold_model <- function(x, threshold = 5, low = 20, high = 80) {
  ifelse(x < threshold, low, high)
}

x_values <- seq(0, 10, by = 0.5)

results <- data.frame(
  x = rep(x_values, times = 4),
  model = rep(
    c("linear_growth", "exponential_growth", "logistic_growth", "threshold_response"),
    each = length(x_values)
  ),
  value = c(
    linear_model(x_values),
    exponential_model(x_values),
    logistic_model(x_values),
    threshold_model(x_values)
  )
)

summary <- aggregate(
  value ~ model,
  data = results,
  FUN = function(z) c(minimum = min(z), maximum = max(z), final = tail(z, 1))
)

summary_table <- data.frame(
  model = summary$model,
  minimum_value = summary$value[, "minimum"],
  maximum_value = summary$value[, "maximum"],
  final_value = summary$value[, "final"]
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_functional_form_results.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_functional_form_summary.csv", row.names = FALSE)

print(summary_table)
