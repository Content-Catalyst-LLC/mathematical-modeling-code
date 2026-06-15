response_function <- function(x) {
  10 * sqrt(x + 1)
}

analytic_derivative <- function(x) {
  5 / sqrt(x + 1)
}

finite_difference_derivative <- function(x, h = 1e-5) {
  (response_function(x + h) - response_function(x - h)) / (2 * h)
}

classify_response <- function(elasticity) {
  if (is.na(elasticity)) {
    "elasticity undefined"
  } else if (abs(elasticity) < 1) {
    "inelastic local response"
  } else if (abs(elasticity) == 1) {
    "unit elastic local response"
  } else {
    "elastic local response"
  }
}

audit_point <- function(x) {
  y <- response_function(x)
  derivative <- analytic_derivative(x)
  finite_difference <- finite_difference_derivative(x)
  error <- abs(derivative - finite_difference)

  warnings <- c()
  elasticity <- NA_real_

  if (x == 0) {
    warnings <- c(warnings, "input is zero; proportional input change requires care")
  }

  if (y == 0) {
    warnings <- c(warnings, "output is zero; elasticity undefined")
  }

  if (x != 0 && y != 0) {
    elasticity <- (x / y) * derivative
  }

  if (error > 1e-5) {
    warnings <- c(warnings, "finite-difference check differs from analytic derivative")
  }

  if (x < 0.1) {
    warnings <- c(warnings, "near-zero baseline; normalize with caution")
  }

  data.frame(
    x = x,
    value = y,
    derivative = derivative,
    elasticity = elasticity,
    finite_difference_derivative = finite_difference,
    absolute_error = error,
    response_class = classify_response(elasticity),
    warning = paste(warnings, collapse = "; ")
  )
}

results <- do.call(rbind, lapply(c(0, 0.5, 1, 4, 9, 24), audit_point))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_elasticity_sensitivity_audit.csv", row.names = FALSE)
print(results)
