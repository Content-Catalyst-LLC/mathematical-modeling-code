# Infinity, Infinitesimals, and the Historical Problem of Change
# Base R difference-quotient convergence workflow.

system_response <- function(x) {
  exp(0.2 * x)
}

exact_derivative <- function(x) {
  0.2 * exp(0.2 * x)
}

difference_quotient <- function(x, h) {
  (system_response(x + h) - system_response(x)) / h
}

steps <- read.csv("data/step_sizes.csv")
x0 <- 5.0
estimate <- difference_quotient(x0, steps$h)
exact <- exact_derivative(x0)

results <- data.frame(
  function_name = "exp(0.2x)",
  x = x0,
  h = steps$h,
  estimate = estimate,
  exact_value = exact,
  absolute_error = abs(estimate - exact)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_difference_quotient_convergence.csv", row.names = FALSE)

print(results)
