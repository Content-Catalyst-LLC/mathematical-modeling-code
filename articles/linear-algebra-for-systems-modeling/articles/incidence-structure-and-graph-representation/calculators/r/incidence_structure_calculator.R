result <- data.frame(
  calculator = "incidence_structure_calculator",
  graph_name = "synthetic_infrastructure_incidence_graph",
  node_count = 4,
  edge_count = 5,
  signed_incidence = TRUE,
  nonzero_incidence_entries = 10,
  incidence_density = 0.5,
  max_absolute_node_balance = 9.0,
  laplacian_trace = 10.0,
  rank_estimate = 3,
  warning = "Incidence metrics depend on node definitions, edge definitions, sign conventions, weights, conservation assumptions, and data provenance."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_incidence_structure_calculator.csv", row.names = FALSE)
print(result)
