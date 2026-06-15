geometric_power_series <- function(x, n_terms) {
  n <- 0:(n_terms - 1)
  sum(x^n)
}

geometric_reference <- function(x) {
  if (x == 1) {
    return(NA)
  }
  1 / (1 - x)
}

audit_geometric_series <- function(x, n_terms) {
  partial_sum <- geometric_power_series(x, n_terms)
  converges <- abs(x) < 1
  reference_value <- ifelse(converges, geometric_reference(x), NA)
  absolute_error <- ifelse(converges, abs(reference_value - partial_sum), NA)

  data.frame(
    function_name = "1/(1-x)",
    center = 0,
    x_value = x,
    n_terms = n_terms,
    partial_sum = partial_sum,
    reference_value = reference_value,
    absolute_error = absolute_error,
    convergence_status = ifelse(converges, "inside radius of convergence", "outside radius of convergence"),
    warning = ifelse(converges, "", "Power series does not converge for this x value.")
  )
}

cases <- rbind(
  audit_geometric_series(0.25, 5),
  audit_geometric_series(0.25, 10),
  audit_geometric_series(0.75, 5),
  audit_geometric_series(0.75, 20),
  audit_geometric_series(1.25, 10)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(cases, "outputs/tables/r_power_series_approximation_audit.csv", row.names = FALSE)
print(cases)
