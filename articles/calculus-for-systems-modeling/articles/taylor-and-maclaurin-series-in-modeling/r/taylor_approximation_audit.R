taylor_exp_maclaurin <- function(x, order) {
  n <- 0:order
  sum((x^n) / factorial(n))
}

taylor_sin_maclaurin <- function(x, order) {
  n <- 0:order
  sum(((-1)^n) * (x^(2*n + 1)) / factorial(2*n + 1))
}

audit_exp <- function(x, order) {
  approximation <- taylor_exp_maclaurin(x, order)
  reference_value <- exp(x)
  data.frame(
    function_name = "exp(x)",
    center = 0,
    x_value = x,
    order = order,
    approximation = approximation,
    reference_value = reference_value,
    absolute_error = abs(reference_value - approximation),
    warning = ifelse(abs(x) <= 2, "", "Evaluation is far from the Maclaurin center; review truncation error carefully.")
  )
}

audit_sin <- function(x, order) {
  approximation <- taylor_sin_maclaurin(x, order)
  reference_value <- sin(x)
  data.frame(
    function_name = "sin(x)",
    center = 0,
    x_value = x,
    order = order,
    approximation = approximation,
    reference_value = reference_value,
    absolute_error = abs(reference_value - approximation),
    warning = ifelse(abs(x) <= 2, "", "Evaluation is far from the Maclaurin center; review truncation error carefully.")
  )
}

cases <- rbind(
  audit_exp(0.5, 2),
  audit_exp(0.5, 5),
  audit_exp(1.0, 5),
  audit_exp(1.0, 10),
  audit_exp(3.0, 10),
  audit_sin(1.0, 5),
  audit_sin(3.0, 10)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(cases, "outputs/tables/r_taylor_approximation_audit.csv", row.names = FALSE)
print(cases)
