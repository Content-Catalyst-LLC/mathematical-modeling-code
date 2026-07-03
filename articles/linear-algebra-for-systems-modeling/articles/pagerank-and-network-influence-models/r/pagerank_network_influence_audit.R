nodes <- c("water", "power", "transport", "communications", "health")

edges <- data.frame(
  source = c("water", "power", "power", "transport", "communications", "health", "transport", "communications"),
  target = c("power", "transport", "communications", "communications", "health", "water", "water", "power")
)

n <- length(nodes)
node_index <- setNames(seq_along(nodes), nodes)

out_degree <- setNames(rep(0, n), nodes)
for (i in seq_len(nrow(edges))) {
  out_degree[edges$source[i]] <- out_degree[edges$source[i]] + 1
}

P <- matrix(0, nrow = n, ncol = n)
rownames(P) <- nodes
colnames(P) <- nodes

for (i in seq_len(nrow(edges))) {
  source <- edges$source[i]
  target <- edges$target[i]
  P[node_index[target], node_index[source]] <- P[node_index[target], node_index[source]] + 1 / out_degree[source]
}

dangling_nodes <- names(out_degree[out_degree == 0])
if (length(dangling_nodes) > 0) {
  for (node in dangling_nodes) {
    P[, node_index[node]] <- 1 / n
  }
}

damping <- 0.85
tolerance <- 1e-10
max_iterations <- 200

rank_vector <- rep(1 / n, n)
teleport <- rep(1 / n, n)
convergence_log <- data.frame(iteration = integer(), l1_residual = numeric())

for (iteration in seq_len(max_iterations)) {
  next_rank <- damping * (P %*% rank_vector) + (1 - damping) * teleport
  residual <- sum(abs(next_rank - rank_vector))
  convergence_log <- rbind(convergence_log, data.frame(iteration = iteration, l1_residual = residual))
  rank_vector <- as.numeric(next_rank)
  if (residual < tolerance) {
    break
  }
}

rank_table <- data.frame(node = nodes, rank = rank_vector)
rank_table <- rank_table[order(-rank_table$rank), ]

audit_record <- data.frame(
  graph_name = "synthetic_directed_network_influence_model",
  node_count = n,
  edge_count = nrow(edges),
  damping_factor = damping,
  tolerance = tolerance,
  iterations = nrow(convergence_log),
  converged = tail(convergence_log$l1_residual, 1) < tolerance,
  max_rank_node = rank_table$node[1],
  max_rank_score = rank_table$rank[1],
  min_rank_node = rank_table$node[nrow(rank_table)],
  min_rank_score = rank_table$rank[nrow(rank_table)],
  rank_sum = sum(rank_vector),
  dangling_node_count = length(dangling_nodes),
  interpretation_warning = paste(
    "PageRank scores depend on node definitions, directed-edge meaning,",
    "transition normalization, dangling-node handling, damping factor,",
    "teleportation vector, convergence tolerance, graph boundary, and data provenance."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_pagerank_audit.csv", row.names = FALSE)
write.csv(rank_table, "outputs/tables/r_pagerank_scores.csv", row.names = FALSE)
write.csv(convergence_log, "outputs/tables/r_pagerank_convergence_log.csv", row.names = FALSE)
write.csv(edges, "outputs/tables/r_directed_edge_list.csv", row.names = FALSE)
print(audit_record)
