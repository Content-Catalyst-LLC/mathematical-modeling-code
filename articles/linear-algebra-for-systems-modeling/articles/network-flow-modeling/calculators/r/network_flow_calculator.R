result <- data.frame(
  calculator = "network_flow_modeling_calculator",
  graph_name = "synthetic_capacitated_flow_network",
  node_count = 5,
  edge_count = 6,
  source_node = "source",
  sink_node = "sink",
  total_source_outflow = 16.0,
  total_sink_inflow = 16.0,
  capacity_violations = 0,
  saturated_edge_count = 2,
  max_absolute_transshipment_imbalance = 0.0,
  total_flow_cost = 82.0,
  warning = "Network flow metrics depend on flow units, capacities, costs, conservation assumptions, source-sink choices, time scale, and data provenance."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_network_flow_modeling_calculator.csv", row.names = FALSE)
print(result)
