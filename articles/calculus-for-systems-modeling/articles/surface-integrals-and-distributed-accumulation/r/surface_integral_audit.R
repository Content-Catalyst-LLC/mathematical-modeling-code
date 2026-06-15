height <- function(x, y) {
  0.1 * x^2 + 0.05 * y^2
}

scalar_field <- function(x, y, z) {
  1 + 0.2 * z
}

vector_field <- function(x, y, z) {
  c(0.1 * x, 0.1 * y, 1)
}

normal_area_vector <- function(x, y, dx, dy) {
  dz_dx <- 0.2 * x
  dz_dy <- 0.1 * y
  c(-dz_dx * dx * dy, -dz_dy * dx * dy, dx * dy)
}

vector_norm <- function(v) {
  sqrt(sum(v^2))
}

audit_surface <- function(step, scenario) {
  xs <- seq(-1, 1 - step, by = step)
  ys <- seq(-1, 1 - step, by = step)

  surface_area <- 0
  scalar_total <- 0
  flux_total <- 0
  patch_areas <- c()
  flux_densities <- c()

  for (x in xs) {
    for (y in ys) {
      z <- height(x, y)
      area_vector <- normal_area_vector(x, y, step, step)
      patch_area <- vector_norm(area_vector)
      scalar_value <- scalar_field(x, y, z)
      vector_value <- vector_field(x, y, z)
      flux <- sum(vector_value * area_vector)

      surface_area <- surface_area + patch_area
      scalar_total <- scalar_total + scalar_value * patch_area
      flux_total <- flux_total + flux
      patch_areas <- c(patch_areas, patch_area)
      flux_densities <- c(flux_densities, flux / max(patch_area, 1e-12))
    }
  }

  warning <- ifelse(
    step > 0.5,
    "Grid step is coarse; curvature and field variation may be undersampled.",
    "Synthetic surface-integral audit; document surface, normal, units, and mesh."
  )

  data.frame(
    scenario = scenario,
    grid_step = step,
    patch_count = length(patch_areas),
    approximate_surface_area = surface_area,
    scalar_surface_integral = scalar_total,
    vector_flux_integral = flux_total,
    average_flux_density = mean(flux_densities),
    maximum_patch_area = max(patch_areas),
    surface_description = "graph z = 0.1x^2 + 0.05y^2 over [-1,1] x [-1,1]",
    warning = warning
  )
}

results <- rbind(
  audit_surface(1.0, "coarse_surface_mesh"),
  audit_surface(0.5, "medium_surface_mesh"),
  audit_surface(0.25, "fine_surface_mesh")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_surface_integral_audit.csv", row.names = FALSE)
print(results)
