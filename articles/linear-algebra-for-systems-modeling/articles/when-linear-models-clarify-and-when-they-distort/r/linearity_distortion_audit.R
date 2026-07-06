x <- c(0, 1, 2, 3, 4)
y <- 1.0 + 0.7 * x + 0.35 * x^2

linear_fit <- lm(y ~ x)
fitted_values <- fitted(linear_fit)
residuals_linear <- residuals(linear_fit)

sign_pattern <- paste(
  ifelse(residuals_linear > 1e-9, "+",
    ifelse(residuals_linear < -1e-9, "-", "0")
  ),
  collapse = ""
)

audit_record <- data.frame(
  workflow_name = "linearity_distortion_audit",
  model_purpose = "baseline_linear_approximation_for_system_behavior",
  fitted_intercept = coef(linear_fit)[1],
  fitted_slope = coef(linear_fit)[2],
  residual_sum_squares = sum(residuals_linear^2),
  max_absolute_residual = max(abs(residuals_linear)),
  residual_sign_pattern = sign_pattern,
  curvature_warning = paste(
    "Residuals show a structured sign pattern consistent with curvature.",
    "The linear fit is useful as a baseline but risks distortion if interpreted",
    "as the system mechanism."
  ),
  extrapolation_warning = paste(
    "Do not extrapolate the fitted line beyond the observed operating range",
    "without additional validation."
  ),
  interpretation_warning = paste(
    "Linear models clarify first-order structure, but residuals, thresholds,",
    "interactions, feedback, aggregation, and causal assumptions must be reviewed",
    "before using results for decisions."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_linearity_distortion_audit.csv", row.names = FALSE)
print(audit_record)
