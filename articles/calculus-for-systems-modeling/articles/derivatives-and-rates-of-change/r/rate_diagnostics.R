system_response <- function(x) exp(0.2 * x)
exact_derivative <- function(x) 0.2 * exp(0.2 * x)
average_rate <- function(a, b) (system_response(b) - system_response(a)) / (b - a)
forward_difference <- function(x, h) (system_response(x + h) - system_response(x)) / h
backward_difference <- function(x, h) (system_response(x) - system_response(x - h)) / h
central_difference <- function(x, h) (system_response(x + h) - system_response(x - h)) / (2 * h)
elasticity <- function(d, x) (x / system_response(x)) * d

x0 <- 5.0
h_values <- c(1, 0.5, 0.25, 0.125, 0.0625)
exact <- exact_derivative(x0)

results <- data.frame(
  x0 = x0,
  h = h_values,
  average_rate_right = sapply(h_values, function(h) average_rate(x0, x0 + h)),
  forward_difference = sapply(h_values, function(h) forward_difference(x0, h)),
  backward_difference = sapply(h_values, function(h) backward_difference(x0, h)),
  central_difference = sapply(h_values, function(h) central_difference(x0, h)),
  exact_derivative = exact
)
results$central_absolute_error <- abs(results$central_difference - results$exact_derivative)
results$elasticity_estimate <- sapply(results$central_difference, function(d) elasticity(d, x0))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_rate_diagnostics.csv", row.names = FALSE)
print(results)
