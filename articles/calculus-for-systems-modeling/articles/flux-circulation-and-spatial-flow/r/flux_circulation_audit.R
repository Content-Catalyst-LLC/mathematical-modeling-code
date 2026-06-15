vector_field <- function(x, y) {
  c(-y, x)
}

dot_product <- function(a, b) {
  sum(a * b)
}

circle_points <- function(radius, segments) {
  theta <- seq(0, 2 * pi, length.out = segments + 1)
  data.frame(x = radius * cos(theta), y = radius * sin(theta))
}

audit_circle_flow <- function(radius, segments, scenario) {
  pts <- circle_points(radius, segments)
  flux_total <- 0
  circulation_total <- 0
  tangential_alignments <- c()
  normal_alignments <- c()

  for (i in 1:segments) {
    x0 <- pts$x[i]; y0 <- pts$y[i]
    x1 <- pts$x[i + 1]; y1 <- pts$y[i + 1]
    xm <- 0.5 * (x0 + x1); ym <- 0.5 * (y0 + y1)
    dx <- x1 - x0; dy <- y1 - y0
    segment_length <- sqrt(dx^2 + dy^2)
    tangent <- c(dx / segment_length, dy / segment_length)
    normal <- c(xm / radius, ym / radius)
    field <- vector_field(xm, ym)

    circulation_total <- circulation_total + dot_product(field, c(dx, dy))
    flux_total <- flux_total + dot_product(field, normal) * segment_length
    tangential_alignments <- c(tangential_alignments, dot_product(field, tangent))
    normal_alignments <- c(normal_alignments, dot_product(field, normal))
  }

  warning <- ifelse(
    segments < 32,
    "Coarse path sampling; circulation and flux should be checked with more segments.",
    "Synthetic flow audit; document field meaning, orientation, units, and boundary choice."
  )

  data.frame(
    scenario = scenario,
    segment_count = segments,
    approximate_flux = flux_total,
    approximate_circulation = circulation_total,
    mean_tangential_alignment = mean(tangential_alignments),
    mean_normal_alignment = mean(normal_alignments),
    field_description = "rotating field F=<-y,x>",
    geometry_description = paste("counterclockwise circle with radius", radius),
    warning = warning
  )
}

results <- rbind(
  audit_circle_flow(1, 16, "coarse_circle"),
  audit_circle_flow(1, 64, "medium_circle"),
  audit_circle_flow(1, 256, "fine_circle")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_flux_circulation_audit.csv", row.names = FALSE)
print(results)
