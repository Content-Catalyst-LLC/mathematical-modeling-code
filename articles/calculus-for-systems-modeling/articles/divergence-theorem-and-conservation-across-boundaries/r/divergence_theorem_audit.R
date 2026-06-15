vector_field <- function(x, y, z) {
  c(x, y, z)
}

divergence <- function(x, y, z) {
  3
}

boundary_flux_unit_cube <- function(grid_steps) {
  step <- 1 / grid_steps
  area <- step * step
  total <- 0

  for (i in 0:(grid_steps - 1)) {
    for (j in 0:(grid_steps - 1)) {
      y <- (i + 0.5) * step
      z <- (j + 0.5) * step

      field <- vector_field(0, y, z)
      total <- total + field[1] * (-1) * area

      field <- vector_field(1, y, z)
      total <- total + field[1] * 1 * area

      x <- (i + 0.5) * step
      z <- (j + 0.5) * step

      field <- vector_field(x, 0, z)
      total <- total + field[2] * (-1) * area

      field <- vector_field(x, 1, z)
      total <- total + field[2] * 1 * area

      x <- (i + 0.5) * step
      y <- (j + 0.5) * step

      field <- vector_field(x, y, 0)
      total <- total + field[3] * (-1) * area

      field <- vector_field(x, y, 1)
      total <- total + field[3] * 1 * area
    }
  }

  total
}

volume_divergence_unit_cube <- function(grid_steps) {
  step <- 1 / grid_steps
  cell_volume <- step^3
  total <- 0

  for (i in 0:(grid_steps - 1)) {
    for (j in 0:(grid_steps - 1)) {
      for (k in 0:(grid_steps - 1)) {
        x <- (i + 0.5) * step
        y <- (j + 0.5) * step
        z <- (k + 0.5) * step
        total <- total + divergence(x, y, z) * cell_volume
      }
    }
  }

  total
}

audit_divergence_theorem <- function(grid_steps, scenario) {
  flux <- boundary_flux_unit_cube(grid_steps)
  div_integral <- volume_divergence_unit_cube(grid_steps)
  warning <- ifelse(
    grid_steps < 8,
    "Coarse grid; refine before interpreting the boundary-volume comparison.",
    "Synthetic divergence theorem audit; document field, volume, boundary, normals, units, and numerical method."
  )
  data.frame(
    scenario = scenario,
    grid_steps = grid_steps,
    boundary_flux = flux,
    volume_divergence_integral = div_integral,
    absolute_gap = abs(flux - div_integral),
    field_description = "F=<x,y,z>; divergence = 3",
    volume_description = "unit cube [0,1] x [0,1] x [0,1]",
    normal_note = "all six cube faces use outward normals",
    warning = warning
  )
}

results <- rbind(
  audit_divergence_theorem(4, "coarse_audit"),
  audit_divergence_theorem(16, "medium_audit"),
  audit_divergence_theorem(64, "fine_audit")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_divergence_theorem_audit.csv", row.names = FALSE)
print(results)
