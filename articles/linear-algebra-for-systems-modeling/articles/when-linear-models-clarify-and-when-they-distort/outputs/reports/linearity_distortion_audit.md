# Linearity Distortion Audit

- Workflow: linearity_distortion_audit
- Model purpose: baseline_linear_approximation_for_system_behavior
- Fitted intercept: 0.3
- Fitted slope: 2.1
- Residual sum of squares: 1.715
- Max absolute residual: 0.7
- Residual sign pattern: +---+

Residuals show a structured sign pattern consistent with curvature. The linear fit is useful as a baseline but risks distortion if interpreted as the system mechanism.

Do not extrapolate the fitted line beyond the observed operating range without additional validation.

Linear models clarify first-order structure, but residuals, thresholds, interactions, feedback, aggregation, and causal assumptions must be reviewed before using results for decisions.
