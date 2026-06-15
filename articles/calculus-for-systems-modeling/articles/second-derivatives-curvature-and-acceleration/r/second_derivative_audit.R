logistic <- function(x) {
  1 / (1 + exp(-x))
}

first_derivative <- function(x) {
  y <- logistic(x)
  y * (1 - y)
}

second_derivative <- function(x) {
  y <- logistic(x)
  y * (1 - y) * (1 - 2 * y)
}

curvature <- function(x) {
  fp <- first_derivative(x)
  fpp <- second_derivative(x)
  abs(fpp) / ((1 + fp^2)^(3 / 2))
}

finite_difference_second <- function(x, h = 1e-4) {
  (logistic(x + h) - 2 * logistic(x) + logistic(x - h)) / h^2
}

classify_concavity <- function(value, threshold = 1e-8) {
  if (value > threshold) {
    "concave up"
  } else if (value < -threshold) {
    "concave down"
  } else {
    "near zero curvature candidate"
  }
}

audit_point <- function(x) {
  y <- logistic(x)
  fp <- first_derivative(x)
  fpp <- second_derivative(x)
  kappa <- curvature(x)
  fd <- finite_difference_second(x)
  error <- abs(fpp - fd)

  warning <- ""
  if (abs(fpp) < 1e-8) {
    warning <- "possible inflection candidate; verify concavity sign change"
  } else if (error > 1e-5) {
    warning <- "finite-difference second derivative differs from analytic value"
  }

  data.frame(
    x = x,
    value = y,
    first_derivative = fp,
    second_derivative = fpp,
    curvature = kappa,
    concavity = classify_concavity(fpp),
    finite_difference_second = fd,
    absolute_error = error,
    warning = warning
  )
}

results <- do.call(rbind, lapply(c(-4, -2, -1, 0, 1, 2, 4), audit_point))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_second_derivative_audit.csv", row.names = FALSE)
print(results)
