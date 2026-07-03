nodes <- c("water", "power", "transport", "communications", "health")

edges <- data.frame(
  source = c("water", "power", "power", "transport", "communications", "water"),
  target = c("power", "transport", "communications", "communications", "health", "health"),
  weight = c(1.0, 1.5, 0.8, 1.2, 1.0, 2.5)
)

degree_table <- data.frame(
  node = nodes,
  degree = integer(length(nodes)),
  weighted_degree = numeric(length(nodes))
)

for (i in seq_len(nrow(edges))) {
  s <- edges$source[i]
  t <- edges$target[i]
  w <- edges$weight[i]

  degree_table$degree[degree_table$node == s] <- degree_table$degree[degree_table$node == s] + 1
  degree_table$degree[degree_table$node == t] <- degree_table$degree[degree_table$node == t] + 1

  degree_table$weighted_degree[degree_table$node == s] <- degree_table$weighted_degree[degree_table$node == s] + w
  degree_table$weighted_degree[degree_table$node == t] <- degree_table$weighted_degree[degree_table$node == t] + w
}

node_count <- length(nodes)
edge_count <- nrow(edges)
graph_density <- edge_count / (node_count * (node_count - 1) / 2)

audit_record <- data.frame(
  graph_name = "synthetic_infrastructure_graph_foundations",
  node_count = node_count,
  edge_count = edge_count,
  directed = FALSE,
  weighted = TRUE,
  component_count = 1,
  max_degree = max(degree_table$degree),
  min_degree = min(degree_table$degree),
  average_degree = mean(degree_table$degree),
  has_cycle = TRUE,
  shortest_path_water_to_health = 2.5,
  graph_density = graph_density,
  representation_warning = paste(
    "Graph conclusions depend on node definitions, edge definitions, graph boundary,",
    "direction conventions, weight semantics, missing edges, time period, and data provenance."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_graph_structure_audit.csv", row.names = FALSE)
write.csv(edges, "outputs/tables/r_graph_edge_list.csv", row.names = FALSE)
write.csv(degree_table, "outputs/tables/r_graph_degree_table.csv", row.names = FALSE)
print(audit_record)
