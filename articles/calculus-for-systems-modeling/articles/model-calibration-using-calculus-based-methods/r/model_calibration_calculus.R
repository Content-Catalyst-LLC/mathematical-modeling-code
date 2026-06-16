logistic_solution <- function(t, x0, growth_rate, carrying_capacity) {
  carrying_capacity / (1 + ((carrying_capacity - x0) / x0) * exp(-growth_rate * t))
}

data <- data.frame(
  time = c(0, 2, 4, 6, 8, 10, 12),
  observed_value = c(10.0, 17.5, 29.2, 44.1, 60.5, 74.0, 83.2)
)

evaluate_candidate <- function(growth_rate, carrying_capacity, x0 = 10) {
  predicted <- logistic_solution(data$time, x0, growth_rate, carrying_capacity)
  residual <- data$observed_value - predicted
  squared_residual <- residual^2
  data.frame(
    growth_rate = growth_rate,
    carrying_capacity = carrying_capacity,
    loss = sum(squared_residual),
    mean_absolute_residual = mean(abs(residual)),
    max_absolute_residual = max(abs(residual)),
    warning = "Calibration fit does not prove model validity; validation and sensitivity review remain required."
  )
}

growth_rates <- c(0.22, 0.26, 0.30, 0.34, 0.38, 0.42)
capacities <- c(85, 95, 105, 115, 125)

candidates <- data.frame()
for (r in growth_rates) {
  for (k in capacities) {
    candidates <- rbind(candidates, evaluate_candidate(r, k))
  }
}

candidates <- candidates[order(candidates$loss), ]
best <- candidates[1, ]

best_predicted <- logistic_solution(data$time, 10, best$growth_rate, best$carrying_capacity)
best_residuals <- data.frame(
  time = data$time,
  observed_value = data$observed_value,
  predicted_value = best_predicted,
  residual = data$observed_value - best_predicted,
  squared_residual = (data$observed_value - best_predicted)^2
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(candidates, "outputs/tables/r_calibration_candidates.csv", row.names = FALSE)
write.csv(best_residuals, "outputs/tables/r_best_fit_residuals.csv", row.names = FALSE)

print(best)
print(best_residuals)
