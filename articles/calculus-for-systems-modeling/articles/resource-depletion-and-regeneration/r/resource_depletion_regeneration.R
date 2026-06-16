logistic_regeneration <- function(stock, r, k) {
  pmax(0, r * stock * (1 - stock / k))
}

threshold_regeneration <- function(stock, r, k, threshold) {
  r * stock * (1 - stock / k) * (stock / threshold - 1)
}

simulate_resource <- function(stock0, regeneration, harvest, dt, steps, loss_rate = 0) {
  stock <- stock0
  cumulative_extraction <- 0
  for (i in seq_len(steps)) {
    extraction <- min(stock, harvest * dt)
    growth <- regeneration(stock) * dt
    loss <- max(0, loss_rate * stock * dt)
    stock <- max(0, stock + growth - extraction - loss)
    cumulative_extraction <- cumulative_extraction + extraction
  }
  c(final_stock = stock, cumulative_extraction = cumulative_extraction)
}

dt <- 0.1
steps <- as.integer(80 / dt)

baseline <- simulate_resource(600, function(stock) logistic_regeneration(stock, 0.18, 1000), 35, dt, steps)
high_harvest <- simulate_resource(600, function(stock) logistic_regeneration(stock, 0.18, 1000), 60, dt, steps)
threshold_case <- simulate_resource(600, function(stock) threshold_regeneration(stock, 0.18, 1000, 180), 45, dt, steps)
degraded <- simulate_resource(600, function(stock) logistic_regeneration(stock, 0.18, 1000), 45, dt, steps, loss_rate = 0.02)

scenario_records <- data.frame(
  scenario_name = c("renewable_precautionary_harvest", "renewable_high_harvest", "threshold_recovery_risk", "degradation_loss_case"),
  final_stock = c(baseline["final_stock"], high_harvest["final_stock"], threshold_case["final_stock"], degraded["final_stock"]),
  cumulative_extraction = c(baseline["cumulative_extraction"], high_harvest["cumulative_extraction"], threshold_case["cumulative_extraction"], degraded["cumulative_extraction"]),
  warning = c(
    "harvest below idealized maximum yield allows persistence under baseline assumptions",
    "higher harvest pressure can push stock downward",
    "threshold-dependent recovery can slow or fail under depletion",
    "additional loss or degradation can undermine apparent sustainability"
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_resource_scenario_records.csv", row.names = FALSE)
print(scenario_records)
