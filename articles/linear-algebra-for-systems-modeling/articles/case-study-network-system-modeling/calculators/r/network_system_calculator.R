result <- data.frame(
  calculator = "case_study_network_system_modeling_calculator",
  workflow_name = "network_system_modeling_audit",
  network_name = "synthetic_infrastructure_service_network",
  node_count = 5,
  edge_count = 6,
  total_weight = 17.0,
  highest_weighted_degree_node = "B",
  highest_weighted_degree = 12.0,
  laplacian_trace = 34.0,
  baseline_component_count = 1,
  stressed_component_count = 1,
  removed_edge = "B-D",
  warning = "Network metrics depend on node definitions, edge meanings, weights, directionality, boundary choices, and missing-edge assumptions."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_case_study_network_system_modeling_calculator.csv", row.names = FALSE)
print(result)
