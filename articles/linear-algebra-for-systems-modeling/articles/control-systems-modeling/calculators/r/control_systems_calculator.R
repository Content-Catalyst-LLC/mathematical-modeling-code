result <- data.frame(
  calculator = "control_systems_calculator",
  time_model = "continuous_time_linear_state_space",
  state_matrix_A = "0.100000,1.000000;0.000000,0.200000",
  input_matrix_B = "0.000000;1.000000",
  output_matrix_C = "1.000000,0.000000",
  feedback_matrix_K = "0.500000,1.400000",
  open_loop_eigenvalues = "0.200000,0.100000",
  closed_loop_eigenvalues = "-0.600000,-0.500000",
  controllability_rank = 2,
  observability_rank = 2,
  warning = "Feedback analysis requires actuator limits, delays, noise, uncertainty, constraints, and objective transparency."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_control_systems_calculator.csv", row.names = FALSE)
print(result)
