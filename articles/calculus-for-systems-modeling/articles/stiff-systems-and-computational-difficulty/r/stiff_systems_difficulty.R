exact_solution <- function(t, y0, eigenvalue) {
  y0 * exp(eigenvalue * t)
}

explicit_euler <- function(y0, eigenvalue, h, stop_time) {
  steps <- round(stop_time / h)
  amplification <- 1 + h * eigenvalue
  y <- y0
  for (step in seq_len(steps)) {
    y <- amplification * y
  }
  list(value = y, amplification_factor = abs(amplification))
}

implicit_euler <- function(y0, eigenvalue, h, stop_time) {
  steps <- round(stop_time / h)
  amplification <- 1 / (1 - h * eigenvalue)
  y <- y0
  for (step in seq_len(steps)) {
    y <- amplification * y
  }
  list(value = y, amplification_factor = abs(amplification))
}

y0 <- 1
eigenvalue <- -50
stop_time <- 1
exact_final <- exact_solution(stop_time, y0, eigenvalue)
step_sizes <- c(0.1, 0.05, 0.025, 0.01)
records <- data.frame()

for (h in step_sizes) {
  explicit_result <- explicit_euler(y0, eigenvalue, h, stop_time)
  implicit_result <- implicit_euler(y0, eigenvalue, h, stop_time)

  records <- rbind(records, data.frame(
    step_size = h,
    eigenvalue = eigenvalue,
    method = "explicit_euler",
    amplification_factor = explicit_result$amplification_factor,
    stability_status = ifelse(explicit_result$amplification_factor <= 1, "stable_for_test_problem", "unstable_for_test_problem"),
    final_value = explicit_result$value,
    exact_final_value = exact_final,
    absolute_error = abs(explicit_result$value - exact_final),
    warning = "Explicit methods may require very small steps on stiff systems."
  ))

  records <- rbind(records, data.frame(
    step_size = h,
    eigenvalue = eigenvalue,
    method = "implicit_euler",
    amplification_factor = implicit_result$amplification_factor,
    stability_status = ifelse(implicit_result$amplification_factor <= 1, "stable_for_test_problem", "unstable_for_test_problem"),
    final_value = implicit_result$value,
    exact_final_value = exact_final,
    absolute_error = abs(implicit_result$value - exact_final),
    warning = "Implicit stability does not remove the need for accuracy and interpretation review."
  ))
}

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(records, "outputs/tables/r_stiffness_audit.csv", row.names = FALSE)
print(records)
