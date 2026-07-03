result <- data.frame(
  calculator = "infrastructure_network_models_calculator",
  network_name = "synthetic_multilayer_infrastructure_network",
  node_count = 6,
  edge_count = 7,
  layer_count = 6,
  critical_asset_count = 5,
  interdependency_edge_count = 3,
  total_baseline_capacity = 400.0,
  disrupted_asset = "power_substation",
  remaining_capacity_after_disruption = 160.0,
  capacity_loss_fraction = 0.6,
  warning = "Infrastructure network metrics depend on asset definitions, edge meanings, layer boundaries, capacity semantics, dependency rules, scenarios, provenance, security, and vulnerability interpretation."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_infrastructure_network_models_calculator.csv", row.names = FALSE)
print(result)
