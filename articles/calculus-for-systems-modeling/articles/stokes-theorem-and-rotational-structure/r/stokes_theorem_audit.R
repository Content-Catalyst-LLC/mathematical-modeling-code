vector_field <- function(x, y, z = 0) {
  c(-y, x, 0)
}

curl_field <- function(x, y, z = 0) {
  c(0, 0, 2)
}

dot_product <- function(a, b) {
  sum(a * b)
}

boundary_circulation_circle <- function(radius, segments) {
  total <- 0
  for (i in 0:(segments - 1)) {
    theta0 <- 2 * pi * i / segments
    theta1 <- 2 * pi * (i + 1) / segments
    x0 <- radius * cos(theta0)
    y0 <- radius * sin(theta0)
    x1 <- radius * cos(theta1)
    y1 <- radius * sin(theta1)
    xm <- 0.5 * (x0 + x1)
    ym <- 0.5 * (y0 + y1)
    dx <- x1 - x0
    dy <- y1 - y0
    total <- total + dot_product(vector_field(xm, ym), c(dx, dy, 0))
  }
  total
}

surface_curl_flux_disk <- function(radius, radial_steps) {
  total <- 0
  normal <- c(0, 0, 1)
  for (i in 0:(radial_steps - 1)) {
    r0 <- radius * i / radial_steps
    r1 <- radius * (i + 1) / radial_steps
    ring_area <- pi * (r1^2 - r0^2)
    rm <- 0.5 * (r0 + r1)
    total <- total + dot_product(curl_field(rm, 0, 0), normal) * ring_area
  }
  total
}

audit_stokes <- function(radius, segments, radial_steps, scenario) {
  circulation <- boundary_circulation_circle(radius, segments)
  curl_flux <- surface_curl_flux_disk(radius, radial_steps)
  warning <- ifelse(
    segments < 64 || radial_steps < 16,
    "Coarse boundary or surface sampling; refine before interpreting the theorem comparison.",
    "Synthetic Stokes theorem audit; document field, surface, boundary, orientation, units, and numerical method."
  )
  data.frame(
    scenario = scenario,
    radius = radius,
    boundary_segments = segments,
    radial_steps = radial_steps,
    boundary_circulation = circulation,
    surface_curl_flux = curl_flux,
    absolute_gap = abs(circulation - curl_flux),
    field_description = "F=<-y,x,0>; curl F=<0,0,2>",
    surface_description = "horizontal disk with upward normal",
    orientation_note = "counterclockwise boundary orientation viewed from positive z",
    warning = warning
  )
}

results <- rbind(
  audit_stokes(1, 32, 8, "coarse_audit"),
  audit_stokes(1, 128, 32, "medium_audit"),
  audit_stokes(1, 512, 128, "fine_audit")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_stokes_theorem_audit.csv", row.names = FALSE)
print(results)
