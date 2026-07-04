result <- data.frame(
  calculator = c(
    "numerical_stability_and_conditioning_calculator",
    "numerical_stability_and_conditioning_calculator"
  ),
  matrix_case = c("well_conditioned_system", "ill_conditioned_system"),
  determinant = c(5.75, 0.00000001),
  condition_number_proxy = c(2.10, 399920000.0),
  residual_norm = c(0.0, 0.0),
  perturbation_size = c(0.00001, 0.00001),
  perturbed_solution_change = c(0.000004, 2000.0),
  stability_status = c("stable_under_demo_threshold", "review_required_ill_conditioned"),
  warning = c(
    "Residuals should be interpreted alongside conditioning, scaling, perturbation sensitivity, solver method, precision, and model purpose.",
    "Residuals should be interpreted alongside conditioning, scaling, perturbation sensitivity, solver method, precision, and model purpose."
  )
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_numerical_stability_and_conditioning_calculator.csv", row.names = FALSE)
print(result)
