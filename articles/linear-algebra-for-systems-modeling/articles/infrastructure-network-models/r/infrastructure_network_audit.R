assets <- data.frame(
  node = c("power_substation", "water_pump", "hospital", "road_bridge", "communications_hub", "warehouse"),
  layer = c("energy", "water", "health", "transportation", "communication", "logistics"),
  service_role = c("electric service", "water pressure", "critical care", "access corridor", "control and coordination", "supply distribution"),
  critical = c(TRUE, TRUE, TRUE, TRUE, TRUE, FALSE),
  baseline_capacity = c(100, 60, 80, 70, 50, 40)
)

edges <- data.frame(
  source = c("power_substation", "power_substation", "communications_hub", "road_bridge", "road_bridge", "warehouse", "communications_hub"),
  target = c("water_pump", "hospital", "power_substation", "hospital", "warehouse", "hospital", "hospital"),
  edge_type = c("functional_dependency", "functional_dependency", "control_dependency", "access_link", "logistics_link", "supply_link", "coordination_link"),
  capacity = c(60, 80, 40, 70, 40, 35, 35),
  dependency_strength = c(0.95, 0.90, 0.70, 0.80, 0.75, 0.65, 0.60)
)

disrupted_asset <- "power_substation"
direct_impacts <- edges$target[edges$source == disrupted_asset & edges$dependency_strength >= 0.80]
impacted_nodes <- unique(c(disrupted_asset, direct_impacts))

baseline_capacity <- sum(assets$baseline_capacity)
lost_capacity <- sum(assets$baseline_capacity[assets$node %in% impacted_nodes])
remaining_capacity <- baseline_capacity - lost_capacity

audit_record <- data.frame(
  network_name = "synthetic_multilayer_infrastructure_network",
  node_count = nrow(assets),
  edge_count = nrow(edges),
  layer_count = length(unique(assets$layer)),
  critical_asset_count = sum(assets$critical),
  interdependency_edge_count = sum(grepl("dependency", edges$edge_type)),
  total_baseline_capacity = baseline_capacity,
  disrupted_asset = disrupted_asset,
  remaining_capacity_after_disruption = remaining_capacity,
  capacity_loss_fraction = lost_capacity / baseline_capacity,
  governance_warning = paste(
    "Infrastructure network results depend on asset definitions, edge definitions, layer boundaries,",
    "capacity units, dependency rules, hazard scenarios, operating conditions, data provenance,",
    "security constraints, and social vulnerability interpretation."
  )
)

layer_summary <- aggregate(baseline_capacity ~ layer, data = assets, FUN = sum)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_infrastructure_network_audit.csv", row.names = FALSE)
write.csv(assets, "outputs/tables/r_infrastructure_assets.csv", row.names = FALSE)
write.csv(edges, "outputs/tables/r_infrastructure_edges.csv", row.names = FALSE)
write.csv(layer_summary, "outputs/tables/r_infrastructure_layer_summary.csv", row.names = FALSE)
print(audit_record)
