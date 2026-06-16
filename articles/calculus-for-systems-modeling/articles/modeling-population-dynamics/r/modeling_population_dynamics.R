exponential_population <- function(n0, r, t) {
  n0 * exp(r * t)
}

logistic_population <- function(n0, r, k, t) {
  k / (1 + ((k - n0) / n0) * exp(-r * t))
}

times <- seq(0, 40, by = 1)
n0 <- 100
r <- 0.08
k <- 1000

scenario_records <- data.frame(
  time = times,
  exponential = exponential_population(n0, r, times),
  logistic = logistic_population(n0, r, k, times)
)

parameter_records <- data.frame(
  parameter_name = c("N0", "r", "K"),
  value = c(n0, r, k),
  unit = c("individuals", "per year", "individuals"),
  source_status = c(
    "synthetic teaching value",
    "synthetic teaching value",
    "synthetic teaching value"
  ),
  warning = c(
    "Initial values should be measured or estimated with uncertainty in empirical use.",
    "Growth rates may vary over time and across conditions.",
    "Carrying capacity is assumption-bearing and may change over time."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_population_growth_scenarios.csv", row.names = FALSE)
write.csv(parameter_records, "outputs/tables/r_population_parameter_records.csv", row.names = FALSE)

print(head(scenario_records))
print(parameter_records)
