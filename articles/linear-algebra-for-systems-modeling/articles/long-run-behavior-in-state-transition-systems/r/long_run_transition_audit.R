states <- c("good", "fair", "poor")

P <- matrix(
  c(
    0.82, 0.16, 0.02,
    0.10, 0.76, 0.14,
    0.03, 0.22, 0.75
  ),
  nrow = 3,
  byrow = TRUE
)

pi_a <- c(0.80, 0.15, 0.05)
pi_b <- c(0.10, 0.25, 0.65)

step_distribution <- function(pi, P, steps) {
  current <- pi
  for (k in seq_len(steps)) {
    current <- current %*% P
  }
  as.numeric(current)
}

stationary <- rep(1 / length(states), length(states))
for (k in seq_len(1000)) {
  stationary <- step_distribution(stationary, P, 1)
}
stationary <- stationary / sum(stationary)

a25 <- step_distribution(pi_a, P, 25)
b25 <- step_distribution(pi_b, P, 25)

l1_distance <- function(x, y) {
  sum(abs(x - y))
}

eigen_values <- eigen(t(P))$values
sorted_magnitudes <- sort(Mod(eigen_values), decreasing = TRUE)
spectral_gap_proxy <- 1 - sorted_magnitudes[2]

audit_record <- data.frame(
  system_name = "long_run_infrastructure_condition_transition_audit",
  states = paste(states, collapse = "|"),
  orientation = "row_stochastic_row_vector_update_pi_next_equals_pi_P",
  stationary_estimate = paste(round(stationary, 6), collapse = ","),
  distribution_a_after_25_steps = paste(round(a25, 6), collapse = ","),
  distribution_b_after_25_steps = paste(round(b25, 6), collapse = ","),
  convergence_distance_a = l1_distance(a25, stationary),
  convergence_distance_b = l1_distance(b25, stationary),
  initial_condition_gap_after_25_steps = l1_distance(a25, b25),
  spectral_gap_proxy = spectral_gap_proxy,
  row_sum_error = max(abs(rowSums(P) - 1)),
  nonnegative = all(P >= 0),
  interpretation_warning = paste(
    "Long-run behavior depends on state definitions, time step, stationarity,",
    "convergence speed, closed classes, and transition-matrix validity."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_long_run_transition_audit.csv", row.names = FALSE)
print(audit_record)
