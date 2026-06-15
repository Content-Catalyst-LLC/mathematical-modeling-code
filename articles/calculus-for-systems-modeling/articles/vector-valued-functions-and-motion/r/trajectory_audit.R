position <- function(t) {
  c(t, sin(t))
}

distance_between <- function(p, q) {
  sqrt((q[1] - p[1])^2 + (q[2] - p[2])^2)
}

audit_trajectory <- function(step, scenario) {
  times <- seq(0, 2 * pi, by = step)
  points <- lapply(times, position)
  segment_lengths <- c()
  speeds <- c()

  for (i in seq_len(length(points) - 1)) {
    segment_length <- distance_between(points[[i]], points[[i + 1]])
    segment_lengths <- c(segment_lengths, segment_length)
    speeds <- c(speeds, segment_length / (times[i + 1] - times[i]))
  }

  arc_length <- sum(segment_lengths)
  displacement <- distance_between(points[[1]], points[[length(points)]])
  efficiency <- displacement / max(arc_length, 1e-12)

  warning <- ifelse(
    step > 0.5,
    "Time step is coarse; turns and speed variation may be undersampled.",
    "Synthetic trajectory audit; document units, parameter meaning, and sampling."
  )

  data.frame(
    scenario = scenario,
    time_step = step,
    point_count = length(points),
    approximate_arc_length = arc_length,
    displacement_magnitude = displacement,
    path_efficiency = efficiency,
    average_speed = mean(speeds),
    maximum_speed = max(speeds),
    domain_description = "trajectory r(t) = <t, sin(t)> for 0 <= t <= 2pi",
    warning = warning
  )
}

results <- rbind(
  audit_trajectory(1.0, "coarse_time_step"),
  audit_trajectory(0.5, "medium_time_step"),
  audit_trajectory(0.25, "fine_time_step")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_trajectory_audit.csv", row.names = FALSE)
print(results)
