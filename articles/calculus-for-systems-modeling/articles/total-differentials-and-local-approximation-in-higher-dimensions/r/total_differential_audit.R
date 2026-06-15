f <- function(x, y) 3.0 * x + 2.0 * y + 0.5 * x * y
fx <- function(x, y) 3.0 + 0.5 * y
fy <- function(x, y) 2.0 + 0.5 * x
total_differential <- function(x, y, dx, dy) fx(x, y) * dx + fy(x, y) * dy
feasible_displacement <- function(x, y, dx, dy, budget = 10) {
  x >= 0 & y >= 0 & x + y <= budget & x + dx >= 0 & y + dy >= 0 & x + dx + y + dy <= budget
}
audit_case <- function(x, y, dx, dy) {
  baseline_output <- f(x, y)
  actual_output <- f(x + dx, y + dy)
  actual_change <- actual_output - baseline_output
  differential_estimate <- total_differential(x, y, dx, dy)
  feasible <- feasible_displacement(x, y, dx, dy)
  data.frame(
    x = x, y = y, dx = dx, dy = dy,
    baseline_output = baseline_output,
    actual_output = actual_output,
    actual_change = actual_change,
    differential_estimate = differential_estimate,
    absolute_error = abs(actual_change - differential_estimate),
    feasible_displacement = feasible,
    warning = ifelse(feasible, "", "Displacement is outside the feasible region.")
  )
}
results <- rbind(
  audit_case(4.0, 3.0, 0.2, -0.1),
  audit_case(4.0, 3.0, 1.0, 1.0),
  audit_case(8.0, 1.0, 1.0, 1.0)
)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_total_differential_audit.csv", row.names = FALSE)
print(results)
