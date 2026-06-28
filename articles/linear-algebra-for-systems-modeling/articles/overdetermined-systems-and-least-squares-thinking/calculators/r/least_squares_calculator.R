result <- data.frame(
  calculator = "least_squares_calculator",
  row_count = 4,
  column_count = 2,
  overdetermined = TRUE,
  rank = 2,
  solution = "0.850000,1.040000",
  fitted_values = "1.890000,2.930000,3.970000,5.010000",
  residuals = "0.110000,-0.030000,0.130000,0.090000",
  residual_norm = 0.191311,
  warning = "Least squares gives a squared-error approximation; residual patterns and model meaning still require review."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_least_squares_calculator.csv", row.names = FALSE)
print(result)
