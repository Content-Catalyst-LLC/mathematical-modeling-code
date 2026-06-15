geometric_terms <- function(a, r, n_terms) {
  n <- 0:(n_terms - 1)
  a * r^n
}

harmonic_terms <- function(n_terms) {
  1 / seq_len(n_terms)
}

audit_geometric <- function(a, r, n_terms) {
  terms <- geometric_terms(a, r, n_terms)
  partial_sum <- sum(terms)

  reference_value <- NA
  estimated_error <- NA
  classification <- "divergent or inconclusive"
  warning <- ""

  if (abs(r) < 1) {
    reference_value <- a / (1 - r)
    estimated_error <- reference_value - partial_sum
    classification <- "convergent geometric series"
  } else {
    warning <- "geometric ratio does not support convergence"
  }

  data.frame(
    series_name = paste0("geometric_r_", r),
    n_terms = n_terms,
    last_term = tail(terms, 1),
    partial_sum = partial_sum,
    reference_value = reference_value,
    estimated_error = estimated_error,
    convergence_classification = classification,
    stopping_rule = "fixed term count with analytic tail check",
    warning = warning
  )
}

audit_harmonic <- function(n_terms) {
  terms <- harmonic_terms(n_terms)
  data.frame(
    series_name = "harmonic",
    n_terms = n_terms,
    last_term = tail(terms, 1),
    partial_sum = sum(terms),
    reference_value = NA,
    estimated_error = NA,
    convergence_classification = "divergent despite terms approaching zero",
    stopping_rule = "fixed term count; no finite limiting total",
    warning = "small last term does not imply finite accumulated total"
  )
}

result <- rbind(
  audit_geometric(a = 10, r = 0.6, n_terms = 25),
  audit_geometric(a = 10, r = 1.05, n_terms = 25),
  audit_harmonic(n_terms = 10000)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/tables/r_sequence_series_convergence_audit.csv", row.names = FALSE)

print(result)
