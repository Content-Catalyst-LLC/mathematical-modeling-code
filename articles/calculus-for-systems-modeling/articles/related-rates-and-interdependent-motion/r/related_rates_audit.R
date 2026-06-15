volume <- function(height, shape_coefficient = 12) {
  shape_coefficient * height^2
}

d_volume_d_height <- function(height, shape_coefficient = 12) {
  2 * shape_coefficient * height
}

height_path <- function(time) {
  2 + 0.08 * time
}

height_rate <- function(time) {
  0.08
}

finite_difference_volume_rate <- function(time, h = 1e-4) {
  (volume(height_path(time + h)) - volume(height_path(time - h))) / (2 * h)
}

audit_time <- function(time) {
  current_height <- height_path(time)
  current_height_rate <- height_rate(time)
  current_volume <- volume(current_height)
  structural <- d_volume_d_height(current_height)
  inferred_rate <- structural * current_height_rate
  fd <- finite_difference_volume_rate(time)
  error <- abs(inferred_rate - fd)

  warning <- ""
  if (current_height <= 0) {
    warning <- "height outside physical domain"
  } else if (error > 1e-5) {
    warning <- "finite-difference check differs from related-rate calculation"
  }

  data.frame(
    time = time,
    height = current_height,
    height_rate = current_height_rate,
    volume = current_volume,
    structural_derivative = structural,
    inferred_volume_rate = inferred_rate,
    finite_difference_check = fd,
    absolute_error = error,
    warning = warning
  )
}

results <- do.call(rbind, lapply(c(0, 5, 10, 20, 40), audit_time))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_related_rates_audit.csv", row.names = FALSE)
print(results)
