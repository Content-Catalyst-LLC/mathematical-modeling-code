forward_model <- function(x) {
  log1p(x)
}

forward_derivative <- function(x) {
  1 / (1 + x)
}

inverse_model <- function(y) {
  exp(y) - 1
}

inverse_audit <- function(target_output) {
  x <- inverse_model(target_output)
  y_check <- forward_model(x)
  residual <- y_check - target_output
  derivative <- forward_derivative(x)
  inverse_sensitivity <- 1 / derivative
  domain_valid <- x > -1

  warning <- ""
  if (!domain_valid) {
    warning <- "recovered input outside domain"
  } else if (abs(derivative) < 1e-6) {
    warning <- "small forward derivative; inverse may be unstable"
  } else if (abs(residual) > 1e-8) {
    warning <- "forward check does not reproduce target output"
  }

  data.frame(
    target_output = target_output,
    recovered_input = x,
    forward_check = y_check,
    residual = residual,
    forward_derivative = derivative,
    inverse_sensitivity = inverse_sensitivity,
    domain_valid = domain_valid,
    warning = warning
  )
}

results <- do.call(rbind, lapply(c(0, 0.5, 1, 1.5, 2), inverse_audit))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_inverse_interpretation_audit.csv", row.names = FALSE)
print(results)
