result <- data.frame(
  calculator = "when_linear_models_clarify_and_when_they_distort_calculator",
  workflow_name = "linearity_distortion_audit",
  model_purpose = "baseline_linear_approximation_for_system_behavior",
  fitted_intercept = 0.3,
  fitted_slope = 2.1,
  residual_sum_squares = 0.98,
  max_absolute_residual = 0.7,
  residual_sign_pattern = "+--0+",
  warning = "Linear models clarify first-order structure, but residuals, thresholds, interactions, feedback, aggregation, and causal assumptions must be reviewed before using results for decisions."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_when_linear_models_clarify_and_when_they_distort_calculator.csv", row.names = FALSE)
print(result)
