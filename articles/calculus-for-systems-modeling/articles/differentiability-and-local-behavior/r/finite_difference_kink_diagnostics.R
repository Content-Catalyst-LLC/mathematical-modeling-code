# Differentiability and Local Behavior
# Base R finite-difference and kink diagnostic workflow.

smooth_response <- function(x) {
  exp(0.2 * x)
}

kink_response <- function(x) {
  abs(x)
}

forward_difference <- function(f, x, h) {
  (f(x + h) - f(x)) / h
}

backward_difference <- function(f, x, h) {
  (f(x) - f(x - h)) / h
}

central_difference <- function(f, x, h) {
  (f(x + h) - f(x - h)) / (2 * h)
}

h_values <- c(1, 0.5, 0.25, 0.125, 0.0625)

build_diagnostics <- function(name, f, x0) {
  data.frame(
    function_name = name,
    x0 = x0,
    h = h_values,
    forward = sapply(h_values, function(h) forward_difference(f, x0, h)),
    backward = sapply(h_values, function(h) backward_difference(f, x0, h)),
    central = sapply(h_values, function(h) central_difference(f, x0, h))
  )
}

smooth_results <- build_diagnostics("smooth_exp_response", smooth_response, 5.0)
kink_results <- build_diagnostics("kink_abs_response", kink_response, 0.0)

results <- rbind(smooth_results, kink_results)
results$one_sided_gap <- abs(results$forward - results$backward)
results$kink_flag <- results$one_sided_gap > 0.5

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_finite_difference_kink_diagnostics.csv", row.names = FALSE)

print(results)
