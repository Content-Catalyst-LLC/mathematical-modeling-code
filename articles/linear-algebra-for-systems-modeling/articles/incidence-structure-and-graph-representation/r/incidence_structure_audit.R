node_names <- c("water", "power", "transport", "communications")

edges <- data.frame(
  source = c("water", "power", "power", "transport", "communications"),
  target = c("power", "transport", "communications", "communications", "water"),
  weight = c(0.75, 0.60, 0.80, 0.45, 0.30)
)

edge_names <- paste0("e", seq_len(nrow(edges)), "_", edges$source, "_to_", edges$target)

B <- matrix(0, nrow = length(node_names), ncol = nrow(edges))
rownames(B) <- node_names
colnames(B) <- edge_names

for (e in seq_len(nrow(edges))) {
  B[edges$source[e], e] <- -1
  B[edges$target[e], e] <- 1
}

flows <- c(12, 9, 5, 4, 3)
names(flows) <- edge_names
balances <- B %*% flows
L <- B %*% t(B)

audit_record <- data.frame(
  graph_name = "synthetic_infrastructure_incidence_graph",
  node_count = length(node_names),
  edge_count = nrow(edges),
  directed_convention = "B[v,e] = -1 at source/tail and +1 at target/head.",
  signed_incidence = TRUE,
  nonzero_incidence_entries = sum(B != 0),
  incidence_density = sum(B != 0) / (nrow(B) * ncol(B)),
  max_absolute_node_balance = max(abs(balances)),
  laplacian_trace = sum(diag(L)),
  rank_estimate = qr(B)$rank,
  representation_warning = paste(
    "Incidence structure depends on node definitions, edge definitions,",
    "sign convention, edge direction, weights, data provenance, and conservation assumptions."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_incidence_structure_audit.csv", row.names = FALSE)
write.csv(B, "outputs/tables/r_oriented_incidence_matrix.csv")
write.csv(L, "outputs/tables/r_graph_laplacian_from_incidence.csv")
write.csv(data.frame(node = node_names, balance = as.numeric(balances)), "outputs/tables/r_node_balance_from_edge_flows.csv", row.names = FALSE)
print(audit_record)
