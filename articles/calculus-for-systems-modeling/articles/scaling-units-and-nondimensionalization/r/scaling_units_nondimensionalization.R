logistic_solution <- function(t, x0, growth_rate, carrying_capacity) {
  carrying_capacity / (1 + ((carrying_capacity - x0) / x0) * exp(-growth_rate * t))
}

scenarios <- data.frame(
  scenario = c("low_stock", "baseline_stock", "high_stock"),
  initial_stock = c(5, 10, 20),
  carrying_capacity = c(100, 100, 100),
  growth_rate = c(0.35, 0.35, 0.35),
  time = c(20, 20, 20),
  unit_warning = c(
    "Synthetic teaching scenario; stock measured in state units.",
    "Synthetic teaching scenario; stock measured in state units.",
    "Synthetic teaching scenario; stock measured in state units."
  )
)

scenarios$final_stock <- mapply(
  logistic_solution,
  scenarios$time,
  scenarios$initial_stock,
  scenarios$growth_rate,
  scenarios$carrying_capacity
)

scenarios$scaled_initial_stock <- scenarios$initial_stock / scenarios$carrying_capacity
scenarios$scaled_final_stock <- scenarios$final_stock / scenarios$carrying_capacity
scenarios$scaled_time <- scenarios$growth_rate * scenarios$time

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenarios, "outputs/tables/r_nondimensional_scenarios.csv", row.names = FALSE)

print(scenarios)
