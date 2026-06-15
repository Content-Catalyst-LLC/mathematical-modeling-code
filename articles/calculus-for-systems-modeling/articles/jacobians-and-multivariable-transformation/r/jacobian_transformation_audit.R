F_model <- function(x, y) c(x^2 + y, x * y + 3 * y)

jacobian <- function(x, y) {
  matrix(c(2 * x, y, 1, x + 3), nrow = 2, byrow = FALSE)
}

audit_case <- function(x, y, dx, dy) {
  J <- jacobian(x, y)
  baseline <- F_model(x, y)
  actual <- F_model(x + dx, y + dy)
  approximate_change <- J %*% c(dx, dy)
  actual_change <- actual - baseline
  det_value <- det(J)
  error_norm <- sqrt(sum((actual_change - approximate_change)^2))
  data.frame(
    x = x, y = y, dx = dx, dy = dy,
    j11 = J[1, 1], j12 = J[1, 2], j21 = J[2, 1], j22 = J[2, 2],
    determinant = det_value,
    approximate_change_1 = approximate_change[1],
    approximate_change_2 = approximate_change[2],
    actual_change_1 = actual_change[1],
    actual_change_2 = actual_change[2],
    error_norm = error_norm,
    warning = ifelse(abs(det_value) > 1e-8, "", "Jacobian is singular or near singular.")
  )
}

results <- rbind(
  audit_case(2.0, 1.0, 0.1, -0.05),
  audit_case(2.0, 1.0, 0.5, 0.5),
  audit_case(0.0, 0.0, 0.1, 0.1)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_jacobian_transformation_audit.csv", row.names = FALSE)
print(results)
