logistic_solution <- function(t, x0, growth_rate, carrying_capacity) {
  carrying_capacity / (1 + ((carrying_capacity - x0) / x0) * exp(-growth_rate * t))
}

scenarios <- data.frame(
  parameter_name = c(
    "growth_rate", "growth_rate", "growth_rate",
    "carrying_capacity", "carrying_capacity", "carrying_capacity"
  ),
  scenario = c("low", "baseline", "high", "low", "baseline", "high"),
  growth_rate = c(0.20, 0.35, 0.50, 0.35, 0.35, 0.35),
  carrying_capacity = c(100, 100, 100, 75, 100, 125),
  initial_stock = c(10, 10, 10, 10, 10, 10),
  horizon = c(20, 20, 20, 20, 20, 20)
)

scenarios$final_stock <- mapply(
  logistic_solution,
  scenarios$horizon,
  scenarios$initial_stock,
  scenarios$growth_rate,
  scenarios$carrying_capacity
)

summary_table <- aggregate(final_stock ~ parameter_name, scenarios, function(x) max(x) - min(x))
names(summary_table)[2] <- "output_range"
summary_table$robustness_note <- ifelse(
  summary_table$output_range < 10,
  "stable across tested synthetic range",
  "sensitive across tested synthetic range"
)
summary_table$warning <- ifelse(
  summary_table$output_range < 10,
  "Output variation is limited across this range.",
  "Conclusion may depend strongly on this parameter."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenarios, "outputs/tables/r_parameter_scenarios.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_parameter_dependence_summary.csv", row.names = FALSE)

print(scenarios)
print(summary_table)
