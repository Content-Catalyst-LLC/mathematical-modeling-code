exponential_output <- function(y0, g, t) {
  y0 * exp(g * t)
}

logistic_output <- function(y0, r, k, dt, steps) {
  y <- y0
  for (i in seq_len(steps)) {
    y <- max(0, y + r * y * (1 - y / k) * dt)
  }
  y
}

simulate_capital <- function(k0, y0, savings_rate, depreciation, productivity_growth, dt, steps) {
  capital <- k0
  output <- y0

  for (i in seq_len(steps)) {
    investment <- savings_rate * output
    capital <- max(0, capital + (investment - depreciation * capital) * dt)
    output <- output * exp(productivity_growth * dt) * (1 + 0.0005 * (capital - k0) * dt)
  }

  c(final_output = output, final_capital = capital)
}

years <- 40
dt <- 0.1
steps <- as.integer(years / dt)

exponential <- exponential_output(100, 0.025, years)
constrained <- logistic_output(100, 0.06, 240, dt, steps)
capital_case <- simulate_capital(300, 100, 0.22, 0.05, 0.012, dt, steps)

scenario_records <- data.frame(
  scenario_name = c("constant_growth_projection", "capacity_constrained_growth", "capital_accumulation_case"),
  final_output = c(exponential, constrained, capital_case["final_output"]),
  final_capital = c(NA, NA, capital_case["final_capital"]),
  warning = c(
    "constant proportional growth compounds over time",
    "growth slows near a defined capacity or saturation limit",
    "investment and depreciation shape long-run output capacity"
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_economic_growth_scenario_records.csv", row.names = FALSE)
print(scenario_records)
