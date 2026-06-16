continuous_future_value <- function(v0, r, t) {
  v0 * exp(r * t)
}

continuous_present_value <- function(fv, r, t) {
  fv * exp(-r * t)
}

discrete_compound_value <- function(v0, r, n, t) {
  v0 * (1 + r / n)^(n * t)
}

real_rate <- function(nominal_rate, inflation_rate) {
  (1 + nominal_rate) / (1 + inflation_rate) - 1
}

simulate_debt <- function(balance0, rate, payment, dt, steps) {
  balance <- balance0
  for (i in seq_len(steps)) {
    balance <- max(0, balance + rate * balance * dt - payment * dt)
  }
  balance
}

continuous <- continuous_future_value(1000, 0.05, 30)
monthly <- discrete_compound_value(1000, 0.05, 12, 30)
discounted <- continuous_present_value(5000, 0.05, 30)
rr <- real_rate(0.06, 0.025)
real_growth <- continuous_future_value(1000, rr, 30)
debt <- simulate_debt(2000, 0.07, 120, 0.1, 300)

scenario_records <- data.frame(
  scenario_name = c(
    "continuous_compounding_case",
    "monthly_compounding_case",
    "discounted_future_value",
    "real_return_case",
    "debt_dynamics_case"
  ),
  final_value = c(
    continuous,
    monthly,
    5000,
    real_growth,
    debt
  ),
  present_value = c(
    1000,
    1000,
    discounted,
    1000,
    NA
  ),
  warning = c(
    "continuous compounding accumulates value exponentially",
    "discrete compounding depends on compounding frequency",
    "discounting translates future value into present value",
    "real growth adjusts nominal return for inflation",
    "debt balance depends on interest payments and time"
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_financial_scenario_records.csv", row.names = FALSE)
print(scenario_records)
