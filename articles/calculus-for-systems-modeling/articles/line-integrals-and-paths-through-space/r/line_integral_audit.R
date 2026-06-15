path_point <- function(t) {
  c(t, sin(t))
}

scalar_field <- function(x, y) {
  1 + y^2
}

vector_field <- function(x, y) {
  c(1, x)
}

distance_between <- function(p, q) {
  sqrt((q[1] - p[1])^2 + (q[2] - p[2])^2)
}

dot_product <- function(a, b) {
  sum(a * b)
}

audit_line_integral <- function(step, scenario) {
  times <- seq(0, 2 * pi, by = step)
  points <- lapply(times, path_point)
  path_length <- 0
  scalar_total <- 0
  vector_total <- 0
  alignments <- c()
  segment_lengths <- c()

  for (i in seq_len(length(points) - 1)) {
    p <- points[[i]]
    q <- points[[i + 1]]
    displacement <- q - p
    segment_length <- distance_between(p, q)
    field_scalar <- scalar_field(p[1], p[2])
    field_vector <- vector_field(p[1], p[2])
    path_length <- path_length + segment_length
    scalar_total <- scalar_total + field_scalar * segment_length
    vector_total <- vector_total + dot_product(field_vector, displacement)
    alignments <- c(alignments, dot_product(field_vector, displacement) / max(segment_length, 1e-12))
    segment_lengths <- c(segment_lengths, segment_length)
  }

  warning <- ifelse(
    step > 0.5,
    "Time step is coarse; path turns and field variation may be undersampled.",
    "Synthetic line-integral audit; document path, field, units, and interpolation."
  )

  data.frame(
    scenario = scenario,
    time_step = step,
    point_count = length(points),
    path_length = path_length,
    scalar_line_integral = scalar_total,
    vector_line_integral = vector_total,
    average_alignment = mean(alignments),
    maximum_segment_length = max(segment_lengths),
    path_description = "path r(t) = <t, sin(t)> for 0 <= t <= 2pi",
    warning = warning
  )
}

results <- rbind(
  audit_line_integral(1.0, "coarse_path"),
  audit_line_integral(0.5, "medium_path"),
  audit_line_integral(0.25, "fine_path")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_line_integral_audit.csv", row.names = FALSE)
print(results)
