result <- data.frame(
  calculator = "case_study_state_transition_and_markov_dynamics_calculator",
  workflow_name = "state_transition_markov_audit",
  scenario_name = "synthetic_infrastructure_condition_transition_model",
  state_count = 4,
  time_steps = 5,
  stochastic_check_passed = TRUE,
  highest_probability_state_after_horizon = "normal",
  highest_probability_after_horizon = 0.42833125,
  stationary_highest_probability_state = "normal",
  stationary_highest_probability = 0.40602189781,
  baseline_disrupted_probability_after_horizon = 0.1756128125,
  stress_disrupted_probability_after_horizon = 0.41016825,
  warning = "State transition results depend on state definitions, transition estimates, time-step choices, uncertainty, validation, and memoryless-assumption limits."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_case_study_state_transition_and_markov_dynamics_calculator.csv", row.names = FALSE)
print(result)
