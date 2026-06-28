baseline <- matrix(c(10,2,0,1,12,3,0,4,8), nrow = 3, byrow = TRUE)
intervention <- matrix(c(1,0.5,0,0.2,1.5,0.4,0,0.7,1.2), nrow = 3, byrow = TRUE)
stress <- matrix(c(-0.5,-0.2,0,-0.1,-0.8,-0.3,0,-0.4,-0.9), nrow = 3, byrow = TRUE)

combined_change <- intervention + 0.5 * stress
future <- baseline + combined_change

result <- data.frame(
  calculator = "matrix_arithmetic_calculator",
  shape = "3x3",
  intervention_weight = 1.0,
  stress_weight = 0.5,
  combined_change_total = round(sum(combined_change), 4),
  future_total = round(sum(future), 4),
  warning = "Shape compatibility does not prove semantic compatibility."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_matrix_arithmetic_calculator.csv", row.names = FALSE)
print(result)
