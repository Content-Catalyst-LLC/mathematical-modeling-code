taylor_exp_maclaurin <- function(x, order) {
  n <- 0:order
  sum((x^n) / factorial(n))
}

audit_exp <- function(x, order) {
  approximation <- taylor_exp_maclaurin(x, order)
  reference_value <- exp(x)
  absolute_error <- abs(reference_value - approximation)
  relative_error <- absolute_error / abs(reference_value)

  data.frame(
    method = "Maclaurin truncation",
    function_name = "exp(x)",
    center = 0,
    x_value = x,
    order = order,
    approximation = approximation,
    reference_value = reference_value,
    absolute_error = absolute_error,
    relative_error = relative_error,
    warning = ifelse(abs(x) <= 2, "", "Evaluation is far from the expansion center; review local validity.")
  )
}

cases <- rbind(
  audit_exp(0.5, 2),
  audit_exp(0.5, 5),
  audit_exp(1.0, 5),
  audit_exp(1.0, 10),
  audit_exp(3.0, 10)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(cases, "outputs/tables/r_approximation_error_audit.csv", row.names = FALSE)
print(cases)
