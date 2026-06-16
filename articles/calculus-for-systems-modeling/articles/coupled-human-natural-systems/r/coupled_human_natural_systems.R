regeneration <- function(stock, growth_rate, carrying_capacity) {
  growth_rate * stock * (1 - stock / carrying_capacity)
}

extraction <- function(efficiency, effort, stock) {
  efficiency * effort * stock
}

adaptive_effort_step <- function(effort, perceived_scarcity, governance_strength, adjustment_rate, dt) {
  target_reduction <- governance_strength * perceived_scarcity
  max(0, effort - adjustment_rate * target_reduction * dt)
}

natural_stock_step <- function(stock, growth_rate, carrying_capacity, extraction_amount, stress, dt) {
  change <- regeneration(stock, growth_rate, carrying_capacity) - extraction_amount - stress
  max(0, stock + change * dt)
}

distributional_burden <- function(exposure, vulnerability, adaptation) {
  max(0, exposure * vulnerability - adaptation)
}

simulate_coupled_system <- function(
  scenario_name, growth_rate, carrying_capacity, efficiency, initial_effort,
  governance_strength, adjustment_rate, stress, initial_stock, vulnerability,
  adaptation, dt, steps
) {
  stock <- initial_stock
  effort <- initial_effort
  cumulative_extraction <- 0
  cumulative_burden <- 0

  for (step in seq_len(steps)) {
    scarcity <- max(0, 1 - stock / carrying_capacity)
    harvest <- extraction(efficiency, effort, stock)
    stock <- natural_stock_step(stock, growth_rate, carrying_capacity, harvest, stress, dt)
    effort <- adaptive_effort_step(effort, scarcity, governance_strength, adjustment_rate, dt)
    burden <- distributional_burden(scarcity + stress, vulnerability, adaptation)
    cumulative_extraction <- cumulative_extraction + harvest * dt
    cumulative_burden <- cumulative_burden + burden * dt
  }

  data.frame(
    scenario_name = scenario_name,
    model_type = "resource_governance_feedback",
    final_human_pressure = effort,
    final_natural_stock = stock,
    cumulative_extraction = cumulative_extraction,
    cumulative_burden = cumulative_burden,
    warning = "Coupled outcome depends on regeneration extraction stress governance adaptation and vulnerability."
  )
}

dt <- 0.25
steps <- 160

scenario_records <- rbind(
  simulate_coupled_system("baseline_coupled_resource", 0.08, 100, 0.003, 12, 0.60, 0.20, 0.25, 80, 1.2, 0.10, dt, steps),
  simulate_coupled_system("high_extraction_low_governance", 0.08, 100, 0.004, 18, 0.20, 0.10, 0.35, 80, 1.6, 0.05, dt, steps),
  simulate_coupled_system("restoration_and_adaptation", 0.10, 110, 0.0025, 10, 0.85, 0.30, 0.15, 80, 1.0, 0.25, dt, steps)
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_coupled_human_natural_scenario_records.csv", row.names = FALSE)
print(scenario_records)
