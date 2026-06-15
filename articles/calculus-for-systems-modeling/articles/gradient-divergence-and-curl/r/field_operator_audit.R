scalar_field <- function(x, y) {
  x^2 + y^2
}

vector_field <- function(x, y) {
  c(-y, x)
}

gradient_field <- function(x, y) {
  c(2 * x, 2 * y)
}

divergence_field <- function(x, y) {
  0
}

curl_2d <- function(x, y) {
  2
}

grid_values <- function(step) {
  seq(-1, 1, by = step)
}

audit_field_operators <- function(step, scenario) {
  values <- grid_values(step)
  grad_magnitudes <- c()
  divergences <- c()
  curls <- c()

  for (x in values) {
    for (y in values) {
      grad <- gradient_field(x, y)
      grad_magnitudes <- c(grad_magnitudes, sqrt(sum(grad^2)))
      divergences <- c(divergences, divergence_field(x, y))
      curls <- c(curls, curl_2d(x, y))
    }
  }

  warning <- ifelse(
    step > 0.5,
    "Grid step is coarse; local derivative structure may be undersampled.",
    "Synthetic field-operator audit; document field definitions, units, grid, and boundary rules."
  )

  data.frame(
    scenario = scenario,
    grid_step = step,
    point_count = length(values)^2,
    mean_gradient_magnitude = mean(grad_magnitudes),
    maximum_gradient_magnitude = max(grad_magnitudes),
    mean_divergence = mean(divergences),
    mean_curl = mean(curls),
    maximum_abs_curl = max(abs(curls)),
    field_description = "scalar f=x^2+y^2; vector F=<-y,x>",
    warning = warning
  )
}

results <- rbind(
  audit_field_operators(1.0, "coarse_grid"),
  audit_field_operators(0.5, "medium_grid"),
  audit_field_operators(0.25, "fine_grid")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_field_operator_audit.csv", row.names = FALSE)
print(results)
