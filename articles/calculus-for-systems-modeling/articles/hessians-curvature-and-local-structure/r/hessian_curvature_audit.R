f_model <- function(x, y) {
  x^2 + x * y + 3 * y^2 + 0.2 * x^2 * y
}

gradient <- function(x, y) {
  c(2 * x + y + 0.4 * x * y, x + 6 * y + 0.2 * x^2)
}

hessian <- function(x, y) {
  matrix(c(2 + 0.4 * y, 1 + 0.4 * x, 1 + 0.4 * x, 6), nrow = 2, byrow = TRUE)
}

classify_hessian <- function(H) {
  det_value <- det(H)
  if (det_value > 0 && H[1, 1] > 0) return("positive definite")
  if (det_value > 0 && H[1, 1] < 0) return("negative definite")
  if (det_value < 0) return("indefinite")
  "semidefinite or inconclusive"
}

audit_case <- function(x, y, dx, dy) {
  g <- gradient(x, y)
  H <- hessian(x, y)
  baseline <- f_model(x, y)
  actual <- f_model(x + dx, y + dy)
  actual_change <- actual - baseline
  first_order_change <- sum(g * c(dx, dy))
  quadratic_term <- 0.5 * as.numeric(t(c(dx, dy)) %*% H %*% c(dx, dy))
  second_order_change <- first_order_change + quadratic_term
  classification <- classify_hessian(H)
  warning <- ifelse(classification == "indefinite", "Hessian is indefinite; local structure is saddle-like.", ifelse(abs(det(H)) < 1e-8, "Hessian is singular or nearly singular.", ""))

  data.frame(
    x = x, y = y, dx = dx, dy = dy,
    gradient_x = g[1], gradient_y = g[2],
    h11 = H[1, 1], h12 = H[1, 2], h21 = H[2, 1], h22 = H[2, 2],
    determinant = det(H), trace = sum(diag(H)), classification = classification,
    first_order_change = first_order_change, second_order_change = second_order_change,
    actual_change = actual_change,
    first_order_error = abs(actual_change - first_order_change),
    second_order_error = abs(actual_change - second_order_change),
    warning = warning
  )
}

results <- rbind(
  audit_case(2.0, 1.0, 0.1, -0.05),
  audit_case(2.0, 1.0, 0.5, 0.5),
  audit_case(-5.0, 0.0, 0.2, 0.1)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_hessian_curvature_audit.csv", row.names = FALSE)
print(results)
