values <- c(72.0, 68.0, 0.91, 0.96, 125000.0)
result <- data.frame(
  dimension = length(values),
  raw_l1_norm = sum(abs(values)),
  raw_euclidean_norm = sqrt(sum(values^2)),
  warning = "Calculator outputs require unit, scale, component, and interpretation review."
)
dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_state_vector_calculator_results.csv", row.names = FALSE)
print(result)
