states <- c("normal", "strained", "disrupted", "recovered")

P <- matrix(
  c(
    0.70, 0.20, 0.05, 0.05,
    0.20, 0.50, 0.20, 0.10,
    0.05, 0.25, 0.55, 0.15,
    0.50, 0.20, 0.05, 0.25
  ),
  nrow = length(states),
  byrow = TRUE
)

P_stress <- matrix(
  c(
    0.55, 0.30, 0.10, 0.05,
    0.10, 0.45, 0.35, 0.10,
    0.03, 0.17, 0.70, 0.10,
    0.35, 0.30, 0.15, 0.20
  ),
  nrow = length(states),
  byrow = TRUE
)

rownames(P) <- states
colnames(P) <- states
rownames(P_stress) <- states
colnames(P_stress) <- states

row_stochastic <- function(M, tolerance = 1e-10) {
  all(M >= -tolerance) && all(abs(rowSums(M) - 1.0) <= tolerance)
}

evolve <- function(M, initial, steps) {
  state <- initial
  for (i in seq_len(steps)) {
    state <- t(M) %*% state
  }
  as.vector(state / sum(state))
}

stationary_distribution <- function(M, iterations = 1000, tolerance = 1e-12) {
  n <- nrow(M)
  state <- rep(1 / n, n)
  for (i in seq_len(iterations)) {
    nxt <- as.vector(t(M) %*% state)
    if (max(abs(nxt - state)) < tolerance) {
      state <- nxt
      break
    }
    state <- nxt
  }
  state / sum(state)
}

initial <- c(1.0, 0.0, 0.0, 0.0)
names(initial) <- states

steps <- 5
baseline <- evolve(P, initial, steps)
stress <- evolve(P_stress, initial, steps)
stationary <- stationary_distribution(P)

audit_record <- data.frame(
  workflow_name = "state_transition_markov_audit",
  scenario_name = "synthetic_infrastructure_condition_transition_model",
  state_count = length(states),
  time_steps = steps,
  stochastic_check_passed = row_stochastic(P) && row_stochastic(P_stress),
  initial_primary_state = "normal",
  highest_probability_state_after_horizon = states[which.max(baseline)],
  highest_probability_after_horizon = max(baseline),
  stationary_highest_probability_state = states[which.max(stationary)],
  stationary_highest_probability = max(stationary),
  stress_disrupted_probability_after_horizon = stress[which(states == "disrupted")],
  baseline_disrupted_probability_after_horizon = baseline[which(states == "disrupted")],
  memoryless_warning = paste(
    "The Markov assumption treats the current state as sufficient for predicting the next state.",
    "If cumulative stress, repeated disruption, policy intervention, repair history, or hidden subgroups matter,",
    "the model should be expanded or treated as exploratory."
  ),
  interpretation_warning = paste(
    "State transition results depend on state definitions, transition estimation, time-step choice,",
    "matrix orientation, sparse data, uncertainty, validation evidence, and scenario assumptions."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_state_transition_markov_audit.csv", row.names = FALSE)
print(audit_record)
