saddle_node_equilibria <- function(mu) {
  if (mu < 0) {
    numeric(0)
  } else if (abs(mu) < 1e-12) {
    c(0)
  } else {
    c(-sqrt(mu), sqrt(mu))
  }
}

saddle_node_derivative <- function(x) {
  -2 * x
}

classify_scalar_stability <- function(derivative_value, tolerance = 1e-8) {
  if (derivative_value < -tolerance) {
    "locally_stable"
  } else if (derivative_value > tolerance) {
    "locally_unstable"
  } else {
    "inconclusive_at_critical_value"
  }
}

records <- list()

for (mu in seq(-2, 4, by = 0.1)) {
  equilibria <- saddle_node_equilibria(mu)

  if (length(equilibria) == 0) {
    records[[length(records) + 1]] <- data.frame(
      model = "saddle_node_normal_form",
      parameter_mu = mu,
      equilibrium = NA,
      derivative_value = NA,
      stability = "no_real_equilibrium",
      branch_status = "equilibrium_absent",
      warning = "For mu below zero, the saddle-node normal form has no real equilibrium."
    )
  } else {
    for (eq in equilibria) {
      derivative_value <- saddle_node_derivative(eq)

      records[[length(records) + 1]] <- data.frame(
        model = "saddle_node_normal_form",
        parameter_mu = mu,
        equilibrium = eq,
        derivative_value = derivative_value,
        stability = classify_scalar_stability(derivative_value),
        branch_status = ifelse(abs(mu) < 1e-12, "critical_branch", "equilibrium_present"),
        warning = "Bifurcation interpretation depends on model form, parameter meaning, and domain validity."
      )
    }
  }
}

results <- do.call(rbind, records)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_bifurcation_audit.csv", row.names = FALSE)

print(head(results))
print(tail(results))
