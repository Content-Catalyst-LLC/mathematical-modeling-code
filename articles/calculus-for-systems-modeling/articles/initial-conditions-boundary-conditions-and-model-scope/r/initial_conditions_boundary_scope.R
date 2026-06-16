logistic_solution <- function(t, x0, growth_rate, carrying_capacity) {
  carrying_capacity / (1 + ((carrying_capacity - x0) / x0) * exp(-growth_rate * t))
}

scenarios <- data.frame(
  scenario = c("low_initial_stock", "baseline_initial_stock", "high_initial_stock"),
  initial_stock = c(5, 10, 20),
  growth_rate = c(0.35, 0.35, 0.35),
  carrying_capacity = c(100, 100, 100),
  horizon = c(20, 20, 20),
  scope_warning = c(
    "Synthetic teaching scenario; do not treat as empirical forecast.",
    "Synthetic teaching scenario; do not treat as empirical forecast.",
    "Synthetic teaching scenario; do not treat as empirical forecast."
  )
)

scenarios$final_stock <- mapply(
  logistic_solution,
  scenarios$horizon,
  scenarios$initial_stock,
  scenarios$growth_rate,
  scenarios$carrying_capacity
)

baseline <- scenarios$final_stock[scenarios$scenario == "baseline_initial_stock"]
scenarios$initial_condition_effect <- scenarios$final_stock - baseline

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenarios, "outputs/tables/r_initial_condition_scenarios.csv", row.names = FALSE)

print(scenarios)
