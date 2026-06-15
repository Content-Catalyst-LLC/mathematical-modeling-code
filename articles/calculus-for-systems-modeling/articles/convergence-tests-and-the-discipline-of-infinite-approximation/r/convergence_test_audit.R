geometric_terms <- function(a, r, n_terms) {
  n <- 0:(n_terms - 1)
  a * r^n
}

p_series_terms <- function(p, n_terms) {
  1 / (seq_len(n_terms)^p)
}

audit_geometric <- function(a, r, n_terms) {
  terms <- geometric_terms(a, r, n_terms)
  partial_sum <- sum(terms)
  estimated_error <- NA
  result <- "diverges or lacks geometric convergence"
  warning <- "ratio magnitude is not below one"

  if (abs(r) < 1) {
    reference <- a / (1 - r)
    estimated_error <- reference - partial_sum
    result <- "converges by geometric-series test"
    warning <- ""
  }

  data.frame(
    series_name = paste0("geometric_r_", r),
    test_used = "geometric-series test",
    n_terms = n_terms,
    partial_sum = partial_sum,
    last_term = tail(terms, 1),
    test_result = result,
    estimated_error = estimated_error,
    stopping_rule = "fixed term count with geometric tail check",
    warning = warning
  )
}

audit_p_series <- function(p, n_terms) {
  terms <- p_series_terms(p, n_terms)
  converges <- p > 1

  data.frame(
    series_name = paste0("p_series_", p),
    test_used = "p-series test",
    n_terms = n_terms,
    partial_sum = sum(terms),
    last_term = tail(terms, 1),
    test_result = ifelse(converges, "converges", "diverges"),
    estimated_error = NA,
    stopping_rule = "fixed term count with p-series classification",
    warning = ifelse(converges, "", "p-series diverges for p less than or equal to one")
  )
}

result <- rbind(
  audit_geometric(10, 0.6, 25),
  audit_geometric(10, 1.05, 25),
  audit_p_series(1.25, 10000),
  audit_p_series(0.75, 10000),
  audit_p_series(1.0, 10000)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/tables/r_convergence_test_audit.csv", row.names = FALSE)
print(result)
