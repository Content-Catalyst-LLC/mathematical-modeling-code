rotation_field <- function(x, y) c(-y, x)
expansion_field <- function(x, y) c(x, y)
planar_curl <- function(x, y) 2
planar_divergence <- function(x, y) 2

square_boundary_points <- function(n) {
  points <- data.frame(x = numeric(), y = numeric())
  for (i in 0:(n - 1)) {
    t <- -1 + 2 * i / n
    points <- rbind(points, data.frame(x = t, y = -1))
  }
  for (i in 0:(n - 1)) {
    t <- -1 + 2 * i / n
    points <- rbind(points, data.frame(x = 1, y = t))
  }
  for (i in 0:(n - 1)) {
    t <- 1 - 2 * i / n
    points <- rbind(points, data.frame(x = t, y = 1))
  }
  for (i in 0:(n - 1)) {
    t <- 1 - 2 * i / n
    points <- rbind(points, data.frame(x = -1, y = t))
  }
  rbind(points, points[1, ])
}

boundary_circulation_square <- function(n) {
  pts <- square_boundary_points(n)
  total <- 0
  for (i in 1:(nrow(pts) - 1)) {
    x0 <- pts$x[i]; y0 <- pts$y[i]
    x1 <- pts$x[i + 1]; y1 <- pts$y[i + 1]
    xm <- 0.5 * (x0 + x1); ym <- 0.5 * (y0 + y1)
    dx <- x1 - x0; dy <- y1 - y0
    field <- rotation_field(xm, ym)
    total <- total + field[1] * dx + field[2] * dy
  }
  total
}

boundary_flux_square <- function(n) {
  pts <- square_boundary_points(n)
  total <- 0
  for (i in 1:(nrow(pts) - 1)) {
    x0 <- pts$x[i]; y0 <- pts$y[i]
    x1 <- pts$x[i + 1]; y1 <- pts$y[i + 1]
    xm <- 0.5 * (x0 + x1); ym <- 0.5 * (y0 + y1)
    dx <- x1 - x0; dy <- y1 - y0
    nxds <- dy; nyds <- -dx
    field <- expansion_field(xm, ym)
    total <- total + field[1] * nxds + field[2] * nyds
  }
  total
}

interior_integral <- function(step, value_fn) {
  values <- seq(-1, 1 - step, by = step)
  total <- 0
  for (x in values) {
    for (y in values) {
      total <- total + value_fn(x + 0.5 * step, y + 0.5 * step) * step * step
    }
  }
  total
}

audit_greens <- function(segments, step, scenario) {
  boundary_circ <- boundary_circulation_square(segments)
  interior_curl <- interior_integral(step, planar_curl)
  boundary_flux <- boundary_flux_square(segments)
  interior_div <- interior_integral(step, planar_divergence)
  warning <- ifelse(
    segments < 16 || step > 0.25,
    "Coarse boundary or interior sampling; refine before interpreting the theorem comparison.",
    "Synthetic Green's theorem audit; document field, region, orientation, units, and numerical method."
  )
  data.frame(
    scenario = scenario,
    boundary_segments_per_side = segments,
    interior_grid_step = step,
    boundary_circulation = boundary_circ,
    interior_curl_integral = interior_curl,
    boundary_flux = boundary_flux,
    interior_divergence_integral = interior_div,
    circulation_gap = abs(boundary_circ - interior_curl),
    flux_gap = abs(boundary_flux - interior_div),
    field_description = "circulation F=<-y,x>; flux G=<x,y>",
    region_description = "positively oriented square [-1,1] x [-1,1]",
    warning = warning
  )
}

results <- rbind(
  audit_greens(8, 0.5, "coarse_audit"),
  audit_greens(32, 0.25, "medium_audit"),
  audit_greens(128, 0.125, "fine_audit")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_greens_theorem_audit.csv", row.names = FALSE)
print(results)
