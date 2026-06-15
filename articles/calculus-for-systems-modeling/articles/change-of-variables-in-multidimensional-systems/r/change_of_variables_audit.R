exposure_cartesian <- function(x, y) {
  r <- sqrt(x^2 + y^2)
  20 * exp(-0.4 * r)
}

exposure_polar <- function(r, theta) {
  20 * exp(-0.4 * r)
}

polar_total <- function(radius, radial_step, angular_step) {
  total <- 0
  r_values <- seq(radial_step / 2, radius, by = radial_step)
  theta_values <- seq(angular_step / 2, 2 * pi, by = angular_step)

  for (r in r_values) {
    for (theta in theta_values) {
      total <- total + exposure_polar(r, theta) * r * radial_step * angular_step
    }
  }

  total
}

cartesian_grid_total <- function(radius, step) {
  total <- 0
  xs <- seq(-radius, radius, by = step)
  ys <- seq(-radius, radius, by = step)

  for (x in xs) {
    for (y in ys) {
      if (x^2 + y^2 <= radius^2) {
        total <- total + exposure_cartesian(x, y) * step^2
      }
    }
  }

  total
}

audit_change_of_variables <- function(radius, radial_step, angular_step, scenario) {
  p_total <- polar_total(radius, radial_step, angular_step)
  c_total <- cartesian_grid_total(radius, radial_step)
  absolute_difference <- abs(p_total - c_total)
  relative_difference <- absolute_difference / max(abs(p_total), 1e-12)

  warning <- ifelse(
    radial_step > 0.5,
    "Resolution is coarse; transformed and Cartesian approximations may differ.",
    "Polar Jacobian factor r included; compare domain and resolution assumptions."
  )

  data.frame(
    scenario = scenario,
    radius = radius,
    radial_step = radial_step,
    angular_step = angular_step,
    polar_total = p_total,
    cartesian_grid_total = c_total,
    absolute_difference = absolute_difference,
    relative_difference = relative_difference,
    jacobian_rule = "dA = r dr dtheta",
    warning = warning
  )
}

results <- rbind(
  audit_change_of_variables(3.0, 0.5, pi / 24, "medium_polar_grid"),
  audit_change_of_variables(3.0, 0.25, pi / 48, "fine_polar_grid"),
  audit_change_of_variables(3.0, 0.125, pi / 96, "very_fine_polar_grid")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_change_of_variables_audit.csv", row.names = FALSE)
print(results)
