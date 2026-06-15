scalar_field <- function(x, y) {
  20 + 2 * sin(x) + 0.5 * y^2
}

vector_field <- function(x, y) {
  c(-y, x)
}

vector_magnitude <- function(vx, vy) {
  sqrt(vx^2 + vy^2)
}

audit_field <- function(step, scenario) {
  xs <- seq(-3, 3, by = step)
  ys <- seq(-3, 3, by = step)
  scalars <- c()
  magnitudes <- c()

  for (x in xs) {
    for (y in ys) {
      s <- scalar_field(x, y)
      v <- vector_field(x, y)
      scalars <- c(scalars, s)
      magnitudes <- c(magnitudes, vector_magnitude(v[1], v[2]))
    }
  }

  warning <- ifelse(
    step > 0.75,
    "Grid resolution is coarse; field structure may be undersampled.",
    "Synthetic field audit; document domain, units, and interpolation assumptions."
  )

  data.frame(
    scenario = scenario,
    grid_step = step,
    point_count = length(scalars),
    scalar_average = mean(scalars),
    scalar_minimum = min(scalars),
    scalar_maximum = max(scalars),
    vector_magnitude_average = mean(magnitudes),
    vector_magnitude_maximum = max(magnitudes),
    domain_description = "square domain [-3,3] x [-3,3]",
    warning = warning
  )
}

results <- rbind(
  audit_field(1.0, "coarse_grid"),
  audit_field(0.5, "medium_grid"),
  audit_field(0.25, "fine_grid")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_field_audit.csv", row.names = FALSE)
print(results)
