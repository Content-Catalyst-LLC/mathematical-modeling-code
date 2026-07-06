nodes <- c("A", "B", "C", "D", "E")

edges <- data.frame(
  from = c("A", "A", "B", "B", "C", "D"),
  to = c("B", "C", "C", "D", "D", "E"),
  weight = c(4.0, 2.0, 3.0, 5.0, 1.0, 2.0)
)

build_adjacency <- function(nodes, edges) {
  A <- matrix(0, nrow = length(nodes), ncol = length(nodes))
  rownames(A) <- nodes
  colnames(A) <- nodes

  for (i in seq_len(nrow(edges))) {
    u <- edges$from[i]
    v <- edges$to[i]
    w <- edges$weight[i]
    A[u, v] <- w
    A[v, u] <- w
  }

  A
}

component_count <- function(A) {
  n <- nrow(A)
  visited <- rep(FALSE, n)

  dfs <- function(start) {
    stack <- c(start)
    while (length(stack) > 0) {
      node <- stack[length(stack)]
      stack <- stack[-length(stack)]
      if (!visited[node]) {
        visited[node] <<- TRUE
        neighbors <- which(A[node, ] > 0)
        stack <- c(stack, neighbors[!visited[neighbors]])
      }
    }
  }

  count <- 0
  for (i in seq_len(n)) {
    if (!visited[i]) {
      count <- count + 1
      dfs(i)
    }
  }

  count
}

A <- build_adjacency(nodes, edges)
degrees <- rowSums(A)
L <- diag(degrees) - A

stressed_edges <- subset(
  edges,
  !((from == "B" & to == "D") | (from == "D" & to == "B"))
)
A_stressed <- build_adjacency(nodes, stressed_edges)

audit_record <- data.frame(
  workflow_name = "network_system_modeling_audit",
  network_name = "synthetic_infrastructure_service_network",
  node_count = length(nodes),
  edge_count = nrow(edges),
  total_weight = sum(edges$weight),
  highest_weighted_degree_node = names(which.max(degrees)),
  highest_weighted_degree = max(degrees),
  laplacian_trace = sum(diag(L)),
  baseline_component_count = component_count(A),
  stressed_component_count = component_count(A_stressed),
  removed_edge = "B-D",
  vulnerability_warning = paste(
    "The edge-removal scenario changes network structure under one simplified stress test.",
    "It does not predict real failure behavior without capacity, timing, redundancy, and domain validation."
  ),
  interpretation_warning = paste(
    "Network metrics depend on node definitions, edge meanings, weights, directionality,",
    "boundary choices, and missing-edge assumptions."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_network_system_modeling_audit.csv", row.names = FALSE)
print(audit_record)
