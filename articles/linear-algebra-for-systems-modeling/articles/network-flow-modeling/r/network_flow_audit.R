nodes <- c("source", "north_hub", "south_hub", "transfer", "sink")

edges <- data.frame(
  source = c("source", "source", "north_hub", "north_hub", "south_hub", "transfer"),
  target = c("north_hub", "south_hub", "transfer", "sink", "transfer", "sink"),
  capacity = c(12, 8, 7, 5, 6, 12),
  cost = c(2, 3, 1, 4, 2, 1),
  flow = c(10, 6, 6, 4, 6, 12)
)

edges$slack <- edges$capacity - edges$flow
edges$saturated <- abs(edges$slack) < 1e-12
edges$capacity_violation <- edges$flow < -1e-12 | edges$flow - edges$capacity > 1e-12
edges$flow_cost <- edges$cost * edges$flow

balances <- setNames(rep(0, length(nodes)), nodes)

for (i in seq_len(nrow(edges))) {
  balances[edges$source[i]] <- balances[edges$source[i]] - edges$flow[i]
  balances[edges$target[i]] <- balances[edges$target[i]] + edges$flow[i]
}

source_node <- "source"
sink_node <- "sink"
transshipment_nodes <- setdiff(nodes, c(source_node, sink_node))

audit_record <- data.frame(
  graph_name = "synthetic_capacitated_flow_network",
  node_count = length(nodes),
  edge_count = nrow(edges),
  source_node = source_node,
  sink_node = sink_node,
  total_source_outflow = -balances[source_node],
  total_sink_inflow = balances[sink_node],
  capacity_violations = sum(edges$capacity_violation),
  saturated_edge_count = sum(edges$saturated),
  max_absolute_transshipment_imbalance = max(abs(balances[transshipment_nodes])),
  total_flow_cost = sum(edges$flow_cost),
  interpretation_warning = paste(
    "Network flow results depend on node definitions, edge definitions, capacity units,",
    "flow units, cost semantics, source-sink choices, conservation assumptions,",
    "time scale, solver settings, uncertainty, and data provenance."
  )
)

balance_table <- data.frame(node = nodes, balance = as.numeric(balances[nodes]))

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_network_flow_audit.csv", row.names = FALSE)
write.csv(edges, "outputs/tables/r_edge_flow_table.csv", row.names = FALSE)
write.csv(balance_table, "outputs/tables/r_node_balance_table.csv", row.names = FALSE)
print(audit_record)
