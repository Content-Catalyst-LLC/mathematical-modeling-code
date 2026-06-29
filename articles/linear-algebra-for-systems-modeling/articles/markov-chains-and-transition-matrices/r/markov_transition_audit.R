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

pi0 <- c(0.60, 0.30, 0.10)

row_sum_error <- max(abs(rowSums(P) - 1))
nonnegative <- all(P >= 0)

step_distribution <- function(pi, P, steps) {
  current <- pi
  for (k in seq_len(steps)) {
    current <- current %*% P
  }
  as.numeric(current)
}

pi1 <- step_distribution(pi0, P, 1)
pi10 <- step_distribution(pi0, P, 10)

steady <- rep(1 / length(states), length(states))
for (k in seq_len(500)) {
  steady <- step_distribution(steady, P, 1)
}
steady <- steady / sum(steady)

eigen_result <- eigen(t(P))
eigenvalues <- eigen_result$values

audit_record <- data.frame(
  system_name = "infrastructure_condition_transition_audit",
  states = paste(states, collapse = "|"),
  orientation = "row_stochastic_row_vector_update_pi_next_equals_pi_P",
  row_sum_error = row_sum_error,
  nonnegative = nonnegative,
  initial_distribution = paste(round(pi0, 6), collapse = ","),
  one_step_distribution = paste(round(pi1, 6), collapse = ","),
  ten_step_distribution = paste(round(pi10, 6), collapse = ","),
  steady_state_estimate = paste(round(steady, 6), collapse = ","),
  leading_eigenvalues = paste(round(Re(eigenvalues), 6), collapse = ","),
  interpretation_warning = paste(
    "Transition matrices depend on state definitions, time step, stationarity, and the Markov assumption.",
    "A steady state is model-implied, not automatically desirable."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_markov_transition_audit.csv", row.names = FALSE)
print(audit_record)
