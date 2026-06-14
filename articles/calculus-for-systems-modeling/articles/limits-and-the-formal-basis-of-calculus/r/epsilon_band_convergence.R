# Limits and the Formal Basis of Calculus
# Base R epsilon-band and convergence workflow.

f <- function(x) {
  exp(0.2 * x)
}

exact_derivative <- function(x) {
  0.2 * exp(0.2 * x)
}

forward_difference <- function(x, h) {
  (f(x + h) - f(x)) / h
}

central_difference <- function(x, h) {
  (f(x + h) - f(x - h)) / (2 * h)
}

steps <- read.csv("data/step_sizes.csv")
epsilons <- read.csv("data/epsilon_bands.csv")

x0 <- 5.0
exact <- exact_derivative(x0)

results <- data.frame(
  h = steps$h,
  forward = forward_difference(x0, steps$h),
  central = central_difference(x0, steps$h)
)

results$forward_error <- abs(results$forward - exact)
results$central_error <- abs(results$central - exact)

epsilon_rows <- list()
k <- 1
for (i in seq_len(nrow(results))) {
  for (j in seq_len(nrow(epsilons))) {
    epsilon_rows[[k]] <- data.frame(
      h = results$h[i],
      epsilon = epsilons$epsilon[j],
      forward_inside = results$forward_error[i] < epsilons$epsilon[j],
      central_inside = results$central_error[i] < epsilons$epsilon[j]
    )
    k <- k + 1
  }
}

epsilon_review <- do.call(rbind, epsilon_rows)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_epsilon_band_convergence.csv", row.names = FALSE)
write.csv(epsilon_review, "outputs/tables/r_epsilon_review.csv", row.names = FALSE)

print(results)
