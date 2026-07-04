audit_case <- function(case_name, A, b) {
  solution <- solve(A, b)
  residual <- b - A %*% solution

  perturbation_size <- 1e-5
  b_perturbed <- c(b[1] + perturbation_size, b[2] - perturbation_size)
  solution_perturbed <- solve(A, b_perturbed)

  condition_number <- kappa(A, exact = TRUE)
  solution_change <- sqrt(sum((solution_perturbed - solution)^2))

  stability_status <- ifelse(
    condition_number > 1000,
    "review_required_ill_conditioned",
    "stable_under_demo_threshold"
  )

  data.frame(
    model_name = "numerical_stability_conditioning_audit",
    matrix_case = case_name,
    matrix_shape = paste(dim(A), collapse = "x"),
    determinant = det(A),
    condition_number = condition_number,
    solution_norm = sqrt(sum(solution^2)),
    residual_norm = sqrt(sum(residual^2)),
    relative_residual = sqrt(sum(residual^2)) / max(sqrt(sum(b^2)), 1e-15),
    perturbation_size = perturbation_size,
    perturbed_solution_change = solution_change,
    stability_status = stability_status,
    interpretation_warning = paste(
      "Residuals should be interpreted alongside conditioning, scaling,",
      "perturbation sensitivity, solver method, precision, and model purpose."
    )
  )
}

well_conditioned_A <- matrix(
  c(
    3.0, 0.5,
    0.5, 2.0
  ),
  nrow = 2,
  byrow = TRUE
)

ill_conditioned_A <- matrix(
  c(
    1.0, 0.9999,
    0.9999, 0.99980001
  ),
  nrow = 2,
  byrow = TRUE
)

b <- c(1.0, 0.5)

audit_record <- rbind(
  audit_case("well_conditioned_system", well_conditioned_A, b),
  audit_case("ill_conditioned_system", ill_conditioned_A, b)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_stability_conditioning_audit.csv", row.names = FALSE)

print(audit_record)
