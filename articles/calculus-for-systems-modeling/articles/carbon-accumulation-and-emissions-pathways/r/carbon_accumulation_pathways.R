linear_decline <- function(e0, years) {
  pmax(0, e0 * (1 - seq(0, years) / years))
}

exponential_decline <- function(e0, rate, years) {
  e0 * exp(-rate * seq(0, years))
}

overshoot_pathway <- function(e0, decline_years, negative_years, removal_rate) {
  c(linear_decline(e0, decline_years), rep(-removal_rate, negative_years))
}

impulse_burden <- function(pathway, persistent = 0.2) {
  coefficients <- data.frame(weight = c(0.3, 0.25, 0.25), tau = c(4, 35, 200))
  burden <- 0
  horizon <- length(pathway)
  for (i in seq_along(pathway)) {
    age <- horizon - i
    response <- persistent + sum(coefficients$weight * exp(-age / coefficients$tau))
    burden <- burden + pathway[i] * response
  }
  burden
}

constant <- rep(40, 31)
linear <- linear_decline(40, 30)
exponential <- exponential_decline(40, 0.08, 30)
overshoot <- overshoot_pathway(40, 30, 20, 5)

scenario_records <- data.frame(
  scenario_name = c("constant_emissions", "linear_decline_to_zero", "exponential_decline", "overshoot_with_negative_emissions"),
  cumulative_emissions = c(sum(constant), sum(linear), sum(exponential), sum(overshoot)),
  atmospheric_burden = c(impulse_burden(constant), impulse_burden(linear), impulse_burden(exponential), impulse_burden(overshoot)),
  warning = c("constant emissions continue accumulation", "linear decline still accumulates until net zero", "early reductions reduce cumulative burden", "negative emissions require feasibility and permanence review")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_carbon_pathway_scenarios.csv", row.names = FALSE)
print(scenario_records)
