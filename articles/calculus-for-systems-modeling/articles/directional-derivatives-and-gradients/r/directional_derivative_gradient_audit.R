f <- function(x, y) 3.0 * x + 2.0 * y + 0.5 * x * y
gradient <- function(x, y) c(3.0 + 0.5 * y, 2.0 + 0.5 * x)
normalize <- function(v) {
  norm_value <- sqrt(sum(v^2))
  if (norm_value == 0) stop("Direction vector must be nonzero.")
  v / norm_value
}
directional_derivative <- function(x, y, direction) {
  unit_direction <- normalize(direction)
  sum(gradient(x, y) * unit_direction)
}
feasible_direction <- function(x, y, unit_direction, step, budget = 10) {
  x >= 0 & y >= 0 & x + y <= budget &
    x + step * unit_direction[1] >= 0 &
    y + step * unit_direction[2] >= 0 &
    x + step * unit_direction[1] + y + step * unit_direction[2] <= budget
}
audit_direction <- function(x, y, direction_x, direction_y, step) {
  direction <- c(direction_x, direction_y)
  unit_direction <- normalize(direction)
  grad <- gradient(x, y)
  derivative <- sum(grad * unit_direction)
  baseline <- f(x, y)
  actual <- f(x + step * unit_direction[1], y + step * unit_direction[2])
  actual_change <- actual - baseline
  estimated_change <- step * derivative
  feasible <- feasible_direction(x, y, unit_direction, step)
  data.frame(
    x = x, y = y,
    direction_x = direction_x, direction_y = direction_y,
    unit_x = unit_direction[1], unit_y = unit_direction[2],
    gradient_x = grad[1], gradient_y = grad[2],
    directional_derivative = derivative,
    step_size = step,
    estimated_change = estimated_change,
    actual_change = actual_change,
    absolute_error = abs(actual_change - estimated_change),
    feasible_direction = feasible,
    warning = ifelse(feasible, "", "Direction and step move outside the feasible region.")
  )
}
results <- rbind(
  audit_direction(4.0, 3.0, 1.0, 1.0, 0.25),
  audit_direction(4.0, 3.0, 2.0, -1.0, 0.25),
  audit_direction(8.0, 1.0, 1.0, 1.0, 1.0)
)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_directional_derivative_gradient_audit.csv", row.names = FALSE)
print(results)
